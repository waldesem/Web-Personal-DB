"""Manage dependencies."""

from __future__ import annotations

from datetime import datetime, timedelta
from functools import lru_cache, wraps
from typing import Callable

from flask import Response, abort, g
from werkzeug.local import LocalProxy

from app import db
from app.tables.tables import Users

current_user: Users = LocalProxy(lambda: get_current_user(g.token.get("id")))


@lru_cache(maxsize=2)
def get_current_user(user_id: int) -> Users | Response:
    """Retrieve the current user stored in the global variable.

    Args:
        user_id (int): The ID of the user.

    Returns:
        Returns the user object or a 401 HTTP status code.

    """
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


def auth_required(roles: tuple | None = None) -> Callable:
    """Decorate a function that checks a valid JWT token and the user has roles.

    Args:
        roles (str): The roles to check for (optional).

    Returns:
        function: The decorated function.

    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Response | Callable:
            # User validation
            if ("token" not in g) or not current_user:
                return abort(401)

            # Role validation
            if roles and current_user.role not in roles:
                return abort(403)

            return func(*args, **kwargs)

        return wrapper

    return decorator
