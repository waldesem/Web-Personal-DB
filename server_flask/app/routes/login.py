from datetime import datetime

from flask import Blueprint, current_app, jsonify
from sqlalchemy import func, select
from werkzeug.security import check_password_hash, generate_password_hash

from ..depends.depend import create_token, validate
from ..model.models import Login, User
from ..model.tables import Users, db_session


bp = Blueprint("login", __name__, url_prefix="/login")


@bp.post("/<action>")
@validate()
def post_login(action, json_data: Login):
    """
    A function that handles the login process.

    Parameters:
        action (str): The action to be performed during the login process.

    Returns:
        The function returns a tuple containing an empty string and a status code.
        The status code is either 204, or 205, depending on the outcome of the login process.

    """
    user = db_session.execute(
        select(Users).filter(func.lower(Users.username) == json_data.username.lower())
    ).scalar_one_or_none()
    if not user or user.blocked or user.deleted:
        return {"message": "Invalid"}

    if not check_password_hash(user.passhash, json_data.password):
        if user.attempt < 5:
            user.attempt += 1
        else:
            user.blocked = True
        db_session.commit()
        return {"message": "Invalid"}

    if action == "update":
        user.passhash = generate_password_hash(json_data.new_pswd)
        user.change_pswd = False
        user.attempt = 0
        db_session.commit()
        return {"message": "Updated"}

    delta_change = datetime.now() - user.pswd_create
    if not user.change_pswd and delta_change.days < 365:
        user.attempt = 0
        db_session.commit()
        try:
            user_validated = User(**user.to_dict())
            token = create_token(user_validated.dict())
            if token:
                return jsonify(
                    {
                        "message": "Success",
                        "access_token": token,
                    }
                )
        except Exception as e:
            current_app.logger.exception(e)
    return {"message": "Denied"}
