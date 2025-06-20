"""Authorization extension."""

from __future__ import annotations

from datetime import datetime, timedelta
from functools import lru_cache, wraps
from typing import Callable

import jwt
from flask import Flask, Response, abort, current_app, g, request
from werkzeug.local import LocalProxy

from app.structures.tables import Users, db_session


@lru_cache(maxsize=2)
def _get_current_user(user_id: int) -> Users | Response:
    """Retrieve the current user stored in the global variable 'g.user_id'.

    Args:
        user_id (int): The ID of the user.

    Returns:
        If the user is found, returns the user object. Otherwise, returns a 401 HTTP
        status code.

    """
    user = db_session.get(Users, user_id)
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


class Authorize:
    """The Authorize user with jwt tokens."""

    def __init__(self, app: Flask | None = None) -> None:
        """Init class."""
        if app is not None:
            self.init_app(app)
        self.cache = None
        self.cache_key = None
        self.current_user = None

    def init_app(self, app: Flask) -> None:
        """Init app."""
        app.before_request(self.before_request)

    def before_request(self, response: Response, header: str | None = None) -> Response:
        """Before request."""
        if header:
            try:
                user: dict = jwt.decode(
                    header[7:],
                    current_app.config["JWT_SECRET_KEY"],
                    algorithms=["HS256"],
                    options={"verify_exp": True},
                )
                if user_id := user.get("id"):
                    g.user_id = user_id
                    return response
                return abort(401)

            except (ValueError, jwt.exceptions.PyJWTError):
                current_app.logger.exception("Validation Error")
                return abort(401)

        return response

    @property
    def current_user() -> Users:
        """Define current user."""
        return LocalProxy(lambda: _get_current_user(g.user_id))

    def auth_required(self, roles: tuple | None = None) -> Callable:
        """Decorate a function that checks a valid JWT token and the user has roles.

        The decorated function checks if the request contains a valid JWT token in the
        'Authorization' header. If the token is valid, the function is executed.
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
                self.before_request(header=request.headers.get("Authorization"))

                # Role validation
                if roles and self.current_user.role not in roles:
                    return abort(403)

                return func(*args, **kwargs)

            return wrapper

        return decorator
