"""Login routes."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from flask import Blueprint, current_app, g
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, revoked
from app.decorators.depend import auth_required
from app.decorators.validize import pydantify
from app.models.models import AuthResponse, Login
from app.tables.tables import Users
from app.utils.utilities import create_access_token, create_refresh_token

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/<action>")
@pydantify(AuthResponse)
def post_login(
    action: Literal["login", "update"],
    json_data: Login,
) -> tuple[str | dict, int]:
    """Handle the login process."""
    try:
        user = db.session.execute(
            select(Users).filter_by(username=json_data.username),
        ).scalar_one_or_none()
        if not user or user.blocked or user.deleted:
            return {"message": "invalid"}, 200

        if not check_password_hash(user.passhash, json_data.password):
            if user.attempt < 5:
                user.attempt += 1
            else:
                user.blocked = True
            db.session.commit()
            return {"message": "invalid"}, 200

        if action == "update" and json_data.new_pswd:
            user.passhash = generate_password_hash(json_data.new_pswd)
            user.pswd_create = datetime.now(tz=timezone.utc)  # noqa: UP017
            user.change_pswd = False
            user.attempt = 0
            db.session.commit()
            return {"message": "updated"}, 201

        delta_change = datetime.now() - user.pswd_create
        if not user.change_pswd and delta_change.days < 365:
            user.attempt = 0
            db.session.commit()
            return {
                "message": "success",
                "access_token": "Bearer " + create_access_token(user),
                "refresh_token": "Bearer " + create_refresh_token(user),
            }, 200
        return {"message": "denied"}, 200  # noqa: TRY300

    except (SQLAlchemyError, ValueError, ValidationError):
        current_app.logger.exception("Error occurred in login route")
        db.session.rollback()
        return {"message": "invalid"}, 200


@bp.post("/logout")
@pydantify()
def logout(json_data: AuthResponse) -> tuple[dict, int]:
    """Logout the user."""
    if not json_data.access_token or not json_data.refresh_token:
        current_app.logger.warning("Invalid token")
        return {"message": "invalid"}, 200
    try:
        revoked.set(json_data.access_token.split(".")[-1])
        revoked.set(json_data.refresh_token.split(".")[-1])
        revoked.revoke()
    except (ValueError, IndexError):
        current_app.logger.exception("Error occurred in logout route")
    return {"message": ""}, 200


@bp.post("/refresh")
@pydantify(AuthResponse)
@auth_required(refresh=True)
def refresh_token() -> tuple[dict, int]:
    """Refresh the access token."""
    try:
        return {
            "message": "success",
            "access_token": "Bearer " + create_access_token(g.user),
        }, 201
    except (ValueError, ValidationError):
        return {"message": "invalid"}, 200
