"""Login routes."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from flask import Blueprint, g
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.decorators.depend import auth_required
from app.decorators.pydantify import serialize, validize
from app.models.models import AuthResponse, Login, Session
from app.tables.tables import Users
from app.utils.utilities import create_token

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/<action>")
@serialize(AuthResponse)
@validize()
def post_login(
    action: Literal["login", "update"],
    json_data: Login,
) -> tuple[str | dict, int]:
    """Handle the login process."""
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
            "access_token": create_token(user.id),
            "refresh_token": create_token(user.id, "REFRESH"),
        }, 201
    return {"message": "denied"}, 200


@bp.post("/refresh")
@serialize(AuthResponse)
@auth_required(refresh=True)
def refresh_token() -> tuple[dict, int]:
    """Refresh the access token."""
    return {
        "message": "success",
        "access_token": create_token(g.user.id),
    }, 201


@bp.get("/session")
@serialize(Session)
@auth_required()
def get_session() -> tuple[dict, int]:
    """Retrieve an item from the database based on the provided item ID."""
    return g.user.model_dump(), 200
