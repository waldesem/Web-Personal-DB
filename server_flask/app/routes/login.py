"""Login routes."""

from datetime import datetime, timedelta

import jwt
from flask import Blueprint, Response, current_app, jsonify
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash

from app.depends.depend import current_user, jwt_required, validate
from app.model.models import Login
from app.model.tables import Users, db_session

bp = Blueprint("auth", __name__, url_prefix="/auth")

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
    try:
        user = db_session.execute(
            select(Users).filter(func.lower(Users.username) == json_data.username),
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
            user.pswd_create = datetime.now()
            user.change_pswd = False
            user.attempt = 0
            db_session.commit()
            return jsonify({"message": "Updated"})

        delta_change = datetime.now() - user.pswd_create
        if not user.change_pswd and delta_change.days < DELTA_CHANGE_DAYS:
            user.attempt = 0
            db_session.commit()
            return jsonify(
                {
                    "message": "Success",
                    "access_token": "Bearer "
                    + jwt.encode(
                        {
                            "id": user.id,
                            "fullname": user.fullname,
                            "username": user.username,
                            "email": user.email,
                            "region": user.region,
                            "role": user.role,
                            "exp": datetime.now() + timedelta(hours=12),
                        },
                        current_app.config["JWT_SECRET_KEY"],
                        algorithm="HS256",
                    ),
                },
            )
        return jsonify({"message": "Denied"})
    except SQLAlchemyError:
        current_app.logger.exception("Database error")
        db_session.rollback()
        return jsonify({"message": "Invalid"}), 200


@bp.post("/refresh")
@jwt_required(verify_exp=False)
def post_refresh() -> Response:
    """Refresh the access token.

    Returns:
        The function returns a tuple containing a JSON object and a status code.

    """
    return jsonify(
        {
            "message": "Success",
            "access_token": "Bearer "
            + jwt.encode(
                {
                    "id": current_user.id,
                    "fullname": current_user.fullname,
                    "username": current_user.username,
                    "email": current_user.email,
                    "region": current_user.region,
                    "role": current_user.role,
                    "exp": datetime.now() + timedelta(hours=12),
                },
                current_app.config["JWT_SECRET_KEY"],
                algorithm="HS256",
            ),
        },
    ), 200
