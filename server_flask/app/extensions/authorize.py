from __future__ import annotations

from datetime import datetime, timedelta
from functools import lru_cache, wraps
from typing import Callable

import jwt
from flask import Response, abort, current_app, g, jsonify, make_response, request
from pydantic import ValidationError
from werkzeug.local import LocalProxy

from app import db
from app.structures.models import Model
from app.structures.tables import Users

current_user: Users = LocalProxy(lambda: get_current_user(g.user_id))


@lru_cache(maxsize=2)
def get_current_user(user_id: int) -> Users | Response:
    """Retrieve the current user stored in the global variable 'g.user_id'.

    Args:
        user_id (int): The ID of the user.

    Returns:
        If the user is found, returns the user object. Otherwise, returns a 401 HTTP
        status code.

    """
    user = db.session.get(Users, user_id)
    if all(
        (
            user,
            not user.blocked,
            not user.deleted,
            not user.change_pswd,
            user.pswd_create + timedelta(days=365) > datetime.now(),
        ),
    ):
        return user
    return abort(401)


def auth_required(roles: tuple | None = None) -> Callable:
    """Decorate a function that checks a valid JWT token and the user has roles.

    The decorated function checks if the request contains a valid JWT token in the
    'Authorization' header. If the token is valid, the decorated function is executed.
    Otherwise, a 401 HTTP status code is returned.

    Else decorated function checks if the user has one of the specified roles in
    the 'Authorization' header. If the user has the specified role, the decorated
    function is executed. Otherwise, a 403 HTTP status code is returned.

    Args:
        roles (str): The roles to check for (optional).

    Returns:
        function: The decorated function.

    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Response | Callable:
            # JWT validation
            try:
                header = request.headers.get("Authorization", type=str)
                user: dict = jwt.decode(
                    header[7:],
                    current_app.config["JWT_SECRET_KEY"],
                    algorithms=["HS256"],
                    options={"verify_exp": True},
                )
                if not user.get("id"):
                    return abort(401)
                g.user_id = user["id"]
            except (ValueError, jwt.exceptions.PyJWTError):
                return abort(401)

            # Role validation
            if roles and current_user.role not in roles:
                return abort(403)

            return func(*args, **kwargs)

        return wrapper

    return decorator