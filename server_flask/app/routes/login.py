"""Login routes."""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from threading import Thread

import jwt
from flask import Blueprint, current_app
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash

from app import auth, db
from app.decorators.depend import auth_required
from app.decorators.validate import serialize, validate
from app.models.models import Login, Token
from app.tables.tables import Users

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/<action>")
@serialize()
@validate
def post_login(action: str, json_data: Login) -> tuple[str | dict, int]:
    """Handle the login process.

    Args:
        action (str): The action to be performed during the login process.
        json_data (Login): The login data.

    Returns:
        The function returns a tuple containing an empty string and a status code.

    """
    try:
        user = db.session.execute(
            select(Users).filter_by(username=json_data.username),
        ).scalar_one_or_none()
        if not user or user.blocked or user.deleted:
            return "Invalid", 200

        if not check_password_hash(user.passhash, json_data.password):
            if user.attempt < 5:
                user.attempt += 1
            else:
                user.blocked = True
            db.session.commit()
            return "Invalid", 200

        if action == "update":
            user.passhash = generate_password_hash(json_data.new_pswd)
            user.pswd_create = datetime.now()
            user.change_pswd = False
            user.attempt = 0
            db.session.commit()
            return "Updated", 201

        delta_change = datetime.now() - user.pswd_create
        if (
            not user.change_pswd
            and delta_change.days < current_app.config["JWT_SECRET_KEY_LIVE"]
        ):
            user.attempt = 0
            db.session.commit()
            token = Token(
                id=user.id,
                fullname=user.fullname,
                username=user.username,
                email=user.email,
                region=user.region,
                role=user.role,
                exp=datetime.now() + timedelta(hours=12),
                jti=secrets.token_hex(16),
            )
            return {
                "message": "Success",
                "access_token": "Bearer "
                + jwt.encode(
                    token.dict(),
                    current_app.config["JWT_SECRET_KEY"],
                    algorithm="HS256",
                ),
            }, 200
        return "Denied", 200  # noqa: TRY300

    except (SQLAlchemyError, ValueError, ValidationError):
        current_app.logger.exception("Error occurred in login route")
        db.session.rollback()
        return "Invalid", 200


@bp.get("/logout")
#@serialize()
@auth_required()
def get_logout() -> tuple[str, int]:
    """Logout the user.

    Returns:
        The function returns a tuple containing an empty string and a status code.

    """
    auth.jwt_revoked_db.set(auth.token.jti, auth.token.exp)

    def revoke_token() -> None:
        for key, value in auth.jwt_revoked_db.data.items():
            if value < datetime.now(tz=timezone.utc):
                auth.jwt_revoked_db.delete(key)

    thread = Thread(target=revoke_token)
    thread.start()

    return "", 200
