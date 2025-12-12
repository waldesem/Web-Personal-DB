"""Login routes."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from flask import Blueprint, Response, g, jsonify
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.decorators.depend import auth_required
from app.decorators.pydantify import validize
from app.models.models import Login  # noqa: TC001
from app.tables.tables import Users
from app.utils.utilities import create_token

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/<action>")
@validize()
def post_login(action: Literal["login", "update"], json_data: Login) -> Response:
    """Handle the login process."""
    user = db.session.execute(
        select(Users).filter_by(username=json_data.username),
    ).scalar_one_or_none()

    if not user or user.blocked or user.deleted:
        return jsonify({"message": "invalid"}), 200

    if not check_password_hash(user.passhash, json_data.password):
        if user.attempt < 5:
            user.attempt += 1
        else:
            user.blocked = True
        db.session.commit()
        return jsonify({"message": "invalid"}), 200

    if action == "update" and json_data.new_pswd:
        user.passhash = generate_password_hash(json_data.new_pswd)
        user.pswd_create = datetime.now(tz=timezone.utc)  # noqa: UP017
        user.change_pswd = False
        user.attempt = 0
        db.session.commit()
        return jsonify({"message": "updated"}), 201

    delta_change = datetime.now() - user.pswd_create
    if not user.change_pswd and delta_change.days < 365:
        user.attempt = 0
        db.session.commit()
        return jsonify(
            {
                "message": "success",
                "access_token": create_token(user.id),
                "refresh_token": create_token(user.id, "REFRESH"),
            },
        ), 201
    return jsonify({"message": "denied"}), 200


@bp.post("/refresh")
@auth_required(refresh=True)
def refresh_token() -> Response:
    """Refresh the access token."""
    return jsonify(
        {
            "message": "success",
            "access_token": create_token(g.user.id),
        },
    ), 201


@bp.get("/session")
@auth_required()
def get_session() -> Response:
    """Retrieve an item from the database based on the provided item ID."""
    return jsonify(g.user.dict()), 200
