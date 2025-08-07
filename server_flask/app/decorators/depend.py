"""Manage dependencies."""

from __future__ import annotations

from collections.abc import Callable  # noqa: TC003
from datetime import datetime, timedelta
from functools import lru_cache, wraps

import jwt
from flask import Response, abort, current_app, g, request
from pydantic import ValidationError
from werkzeug.local import LocalProxy

from app import db
from app.extensions.revoking import RevokeDB
from app.models.models import Refresh, Token
from app.tables.tables import Users

current_user: Users = LocalProxy(lambda: get_current_user(g.token.get("id")))
jwt_revoked_db = RevokeDB()


@lru_cache(maxsize=2)
def get_current_user(user_id: int) -> Users | Response:
    """Retrieve the current user stored in the global variable."""
    if user_id:
        user = db.session.get(Users, user_id)
        if (
            user
            and not user.blocked
            and not user.deleted
            and not user.change_pswd
            and user.pswd_create + timedelta(days=365) > datetime.now()
        ):
            return user
    return abort(401)


def auth_required(roles: tuple | None = None, refresh: bool = False) -> Callable:  # noqa: FBT001, FBT002
    """Decorate a function that checks a valid JWT token and the user has roles."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Response | Callable:
            if (
                (header := request.headers.get("Authorization"))
                and (token := decode_token(header[7:], refresh))
                and token.jti not in jwt_revoked_db.data
            ):
                g.token = token.dict()
            if ("token" not in g) or not current_user:
                return abort(401)

            # Role validation
            if roles and current_user.role not in roles:
                return abort(403)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def decode_token(payload: str, refresh: bool = False) -> Token | Refresh | None:  # noqa: FBT001, FBT002
    """Decode JWT token and return payload."""
    try:
        decoded = jwt.decode(
            payload,
            current_app.config["JWT_SECRET_KEY"]
            if not refresh
            else current_app.config["REFRESH_SECRET_KEY"],
            algorithms=["HS256"],
            options={"verify_exp": True},
        )
        token = Token(**decoded) if not refresh else Refresh(**decoded)
    except (jwt.exceptions.PyJWTError, ValidationError):
        current_app.logger.exception("JWT decode failed")
        return None
    else:
        return token
