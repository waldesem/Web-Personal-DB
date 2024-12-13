"""Login routes."""

from datetime import datetime

from flask import Blueprint, Response, current_app, jsonify
from sqlalchemy import func, select
from werkzeug.security import check_password_hash, generate_password_hash

from app.depends.depend import create_token, validate
from app.model.models import Login, User
from app.model.tables import Users, db_session

bp = Blueprint("login", __name__, url_prefix="/login")

DELTA_CHANGE_DAYS = 365
ATTEMPT_LIMIT = 5


@bp.post("/<action>")
@validate()
def post_login(action: str, json_data: Login) -> Response:
    """Handle the login process.

    Args:
        action (str): The action to be performed during the login process.
        json_data (Login): The login data.

    Returns:
        The function returns a tuple containing an empty string and a status code.

    """
    user = db_session.execute(
        select(Users).filter(func.lower(Users.username) == json_data.username.lower()),
    ).scalar_one_or_none()
    if not user or user.blocked or user.deleted:
        return jsonify({"message": "Invalid"})

    if not check_password_hash(user.passhash, json_data.password):
        if user.attempt < ATTEMPT_LIMIT:
            user.attempt += 1
        else:
            user.blocked = True
        db_session.commit()
        return jsonify({"message": "Invalid"})

    if action == "update":
        user.passhash = generate_password_hash(json_data.new_pswd)
        user.change_pswd = False
        user.attempt = 0
        db_session.commit()
        return jsonify({"message": "Updated"})

    delta_change = datetime.now() - user.pswd_create  # noqa: DTZ005
    if not user.change_pswd and delta_change.days < DELTA_CHANGE_DAYS:
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
                    },
                )
        except Exception:
            current_app.logger.exception("Error creating token")
    return jsonify({"message": "Denied"})
