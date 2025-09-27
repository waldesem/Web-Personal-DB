"""Manage dependencies."""

from __future__ import annotations

from datetime import datetime, timedelta
from functools import lru_cache, wraps
from typing import TYPE_CHECKING

from flask import Response, abort, current_app, g, request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.models import User
from app.tables.tables import Users
from app.utils.utilities import decode_token

if TYPE_CHECKING:
    from collections.abc import Callable


@lru_cache(maxsize=2)
def get_current_user(user_id: int) -> User:
    """Retrieve the current user stored in the global variable."""
    if user_id:
        try:
            if (
                (user := db.session.get(Users, user_id))
                and not user.blocked
                and not user.deleted
                and not user.change_pswd
                and user.pswd_create + timedelta(days=365) > datetime.now()
            ):
                return User.from_orm(user)
        except (SQLAlchemyError, ValidationError):
            current_app.logger.exception("Database error.")
    return abort(401)


def auth_required(roles: tuple | None = None, *, refresh: bool = False) -> Callable:
    """Decorate a function that checks a valid JWT token and the user has roles."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Response | Callable:
            if (header := request.headers.get("Authorization")) and (
                decoded := decode_token(header, refresh=refresh)
            ):
                g.user = get_current_user(decoded.get("id"))
            else:
                return abort(401)

            if roles and g.user.role not in roles:
                return abort(403)

            return func(*args, **kwargs)

        return wrapper

    return decorator
