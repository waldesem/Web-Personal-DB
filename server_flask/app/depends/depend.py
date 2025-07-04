"""Manage dependencies."""

from __future__ import annotations

from datetime import datetime, timedelta
from functools import lru_cache, wraps
from typing import Callable

import jwt
from flask import Response, abort, current_app, g, request
from werkzeug.local import LocalProxy

from app import db
from app.structures.tables import Users

current_user: Users = LocalProxy(lambda: get_current_user(g.user_id))


@lru_cache(maxsize=2)
def get_current_user(user_id: int) -> Users | Response:
    """Retrieve the current user stored in the global variable 'g.user_id'.

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


def encode_jwt(**kwargs: dict) -> str:
    """Encode jwt."""
    return jwt.encode(kwargs, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")


def decode_jwt(header: str) -> int | Response:
    """Decode jwt."""
    try:
        # JWT validation
        user: dict = jwt.decode(
            header[7:],
            current_app.config["JWT_SECRET_KEY"],
            algorithms=["HS256"],
            options={"verify_exp": True},
        )
        identity = user.get("identity")
    except (ValueError, jwt.exceptions.PyJWTError):
        return abort(401)
    else:
        if user_id := user.get("id"):
            return user_id
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
            header = request.headers.get("Authorization")
            # JWT validation
            g.user_id = decode_jwt(header)

            # Role validation
            if roles and current_user.role not in roles:
                return abort(403)

            return func(*args, **kwargs)

        return wrapper

    return decorator
