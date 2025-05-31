"""Manage dependencies."""

from __future__ import annotations

from datetime import datetime, timedelta
from functools import lru_cache, wraps
from typing import Callable

import jwt
from flask import Response, abort, current_app, g, jsonify, make_response, request
from pydantic import ValidationError
from werkzeug.local import LocalProxy

from app.model.models import Model
from app.model.tables import Users, db_session

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


def jwt_required(func: Callable) -> Callable:
    """Decorate a function that checks if the request contains a valid JWT token.

    The decorated function checks if the request contains a valid JWT token in the
    'Authorization' header. If the token is valid, the decorated function is executed.
    Otherwise, a 401 HTTP status code is returned.

    Args:
        func (function): The function to be decorated.
        verify_exp: check token expired

    Returns:
        function: The decorated function.

    """

    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> Callable:
        try:
            header = request.headers.get("Authorization", type=str)
            user: dict = jwt.decode(
                header[7:],
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"],
                options={"verify_exp": True},
            )
            if user.get("id"):
                g.user_id = user["id"]
                return func(*args, **kwargs)

        except ValueError:
            current_app.logger.exception("Headers not found")
        except jwt.exceptions.PyJWTError:
            current_app.logger.exception("Error decoding token")
        return abort(401)

    return wrapper


def roles_required(*roles: str) -> Callable:
    """Decorate a function that checks if the user has one of the specified roles.

    The decorated function checks if the user has one of the specified roles in
    the 'Authorization' header. If the user has the specified role, the decorated
    function is executed. Otherwise, a 403 HTTP status code is returned.

    Args:
        roles (str): The roles to check for.

    Returns:
        function: The decorated function.

    """

    def decorator(func: Callable) -> Callable:
        @jwt_required()
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Callable:
            if current_user.role in roles:
                return func(*args, **kwargs)
            return abort(403)

        return wrapper

    return decorator


def validate(func: Callable) -> Callable:
    """Decorate a function for validating request data using Pydantic models.

    The decorator accepts the following keyword arguments:

        query_data: Optional[BaseModel]
            The model to validate the query data with.
        json_data: Optional[BaseModel]
            The model to validate the body data with.

    The decorator can be used as follows:

    @app.route("/endpoint", methods=["GET"])
    @validate(query_data=QueryData, json_data=BodyData)
    def endpoint(query_data, json_data):
        # The query_data, json_data are validated and available here
        pass
    """

    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> Callable:
        """Validate request data using Pydantic models."""
        # if funcion has query model argument
        try:
            if query_model := func.__annotations__.get("query_data"):
                query_data = request.args.to_dict()
                kwargs["query_data"] = query_model(**query_data)

            # if funcion has json model argument
            if json_model := func.__annotations__.get("json_data"):
                # if json model annotation is Model
                if json_model.__name__ == "Model":
                    models = {
                        cls.__modelname__: cls
                        for cls in Model.__subclasses__()
                        if hasattr(cls, "__modelname__")
                    }
                    json_model = models[kwargs["item"]]
                json_data = request.get_json()
                kwargs["json_data"] = json_model(**json_data)

        except ValidationError:
            current_app.logger.exception("Error validating data")
            return make_response(jsonify({"message": "error"}))
        else:
            return func(*args, **kwargs)

    return wrapper
