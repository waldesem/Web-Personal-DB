"""Login routes."""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta
from typing import Literal

import jwt
from flask import Blueprint, current_app, g
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, revoked
from app.decorators.depend import auth_required, current_user
from app.decorators.validize import pydantify
from app.models.models import AuthResponse, Login, Refresh, Token
from app.tables.tables import Users

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

        if action == "update":
            user.passhash = generate_password_hash(json_data.new_pswd)
            user.pswd_create = datetime.now()
            user.change_pswd = False
            user.attempt = 0
            db.session.commit()
            return {"message": "updated"}, 201

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
                role=user.role,
                exp=datetime.now() + timedelta(hours=12),
                jti=secrets.token_hex(16),
            )
            refresh = Refresh(
                id=user.id,
                exp=datetime.now() + timedelta(days=30),
                jti=secrets.token_hex(16),
            )
            return {
                "message": "success",
                "access_token": "Bearer "
                + jwt.encode(
                    token.dict(),
                    current_app.config["JWT_SECRET_KEY"],
                    algorithm="HS256",
                ),
                "refresh_token": "Bearer "
                + jwt.encode(
                    refresh.dict(),
                    current_app.config["REFRESH_SECRET_KEY"],
                    algorithm="HS256",
                ),
            }, 200
        return {"message": "denied"}, 200  # noqa: TRY300

    except (SQLAlchemyError, ValueError, ValidationError):
        current_app.logger.exception("Error occurred in login route")
        db.session.rollback()
        return {"message": "invalid"}, 400


@bp.get("/logout")
@pydantify()
@auth_required()
def get_logout() -> tuple[str, int]:
    """Logout the user."""
    revoked.revoke()
    return {"message": "success"}, 200


@bp.post("/refresh")
@pydantify(AuthResponse)
@auth_required(refresh=True)
def get_refresh() -> tuple[str, int]:
    """Refresh the access token."""
    if "token" in g:
        token = Token(
            id=current_user.id,
            fullname=current_user.fullname,
            username=current_user.username,
            email=current_user.email,
            role=current_user.role,
            exp=datetime.now() + timedelta(hours=12),
            jti=secrets.token_hex(16),
        )
        return (
            {
                "message": "success",
                "access_token": "Bearer "
                + jwt.encode(
                    token.dict(),
                    current_app.config["JWT_SECRET_KEY"],
                    algorithm="HS256",
                ),
            },
        ), 200
    return {"message": "invalid"}, 400
