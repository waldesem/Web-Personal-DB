"""Manage dependencies."""

from __future__ import annotations

from datetime import datetime, timedelta
from functools import lru_cache, wraps
from typing import TYPE_CHECKING

from flask import Response, abort, g, request

from app import db
from app.models.models import User
from app.tables.tables import Users
from app.utils.utilities import decode_token

if TYPE_CHECKING:
    from collections.abc import Callable

    from app.classes.classes import Roles


@lru_cache(maxsize=2)
def get_current_user(user_id: int) -> User:
    """Retrieve the current user stored in the global variable."""
    if (
        (user := db.session.get(Users, user_id))
        and not user.blocked
        and not user.deleted
        and not user.change_pswd
        and user.pswd_create + timedelta(days=365) > datetime.now()
    ):
        return User.model_validate(user)
    return abort(401)


def auth_required(role: Roles | None = None, *, refresh: bool = False) -> Callable:
    """Decorate a function that checks a valid JWT token and the user has roles."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Response | Callable:
            try:
                token = (
                    request.get_json()["refresh_token"]
                    if refresh
                    else request.headers["Authorization"]
                )
                if decoded := decode_token(token, refresh=refresh):
                    g.user = get_current_user(decoded["id"])
                else:
                    return abort(401)

                if role and g.user.role != role:
                    return abort(403)

                return func(*args, **kwargs)
            except KeyError:
                return abort(400)

        return wrapper

    return decorator
