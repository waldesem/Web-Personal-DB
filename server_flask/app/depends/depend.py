"""Manage dependencies."""

from __future__ import annotations

from datetime import datetime, timedelta
from functools import lru_cache, wraps
from types import GenericAlias
from typing import Callable

import jwt
from flask import abort, current_app, g, jsonify, make_response, request
from pydantic import BaseModel, ValidationError
from werkzeug.local import LocalProxy

from app.model.models import File
from app.model.tables import Users, db_session

current_user: Users = LocalProxy(lambda: get_current_user(g.user_id))


@lru_cache(maxsize=2)
def get_current_user(user_id: int) -> Users | None:
    """Retrieve the current user stored in the global variable 'g.user_id'.

    Args:
        user_id (int): The ID of the user.

    Returns:
        instance or None: A instance containing the user's information if the user
        exists, is not blocked, not deleted, and has not changed password in the
        last year. Otherwise, returns None.

    """
    user = db_session.get(Users, user_id)
    if (
        user
        and not user.blocked
        and not user.deleted
        and not user.change_pswd
        and user.pswd_create + timedelta(days=365) > datetime.now()  # noqa: DTZ005
    ):
        return user
    return None


def jwt_required() -> Callable:
    """Decorate a function that checks if the request contains a valid JWT token.

    The decorated function checks if the request contains a valid JWT token in the
    'Authorization' header. If the token is valid, the decorated function is executed.
    Otherwise, a 401 HTTP status code is returned.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.

    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Callable:
            header = request.headers.get("Authorization")
            try:
                user_id = jwt.decode(
                    header[7:],
                    current_app.config["JWT_SECRET_KEY"],
                    algorithms=["HS256"],
                ).get("id")
                if user_id:
                    g.user_id = user_id
                    return func(*args, **kwargs)
            except jwt.exceptions.PyJWTError:
                current_app.logger.exception("Error decoding token")
            return abort(401)

        return wrapper

    return decorator


def roles_required(*roles: list[str]) -> Callable:
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
            if current_user and current_user.role in roles:
                return func(*args, **kwargs)
            return abort(403)

        return wrapper

    return decorator


def validate_data(data: dict, model: BaseModel) -> BaseModel | None:
    """Validate data using Pydantic model."""
    try:
        return model(**data)
    except ValidationError:
        current_app.logger.exception("Error validating data")
        return None


def validate() -> Callable:
    """Decorate a function for validating request data using Pydantic models.

    The decorator accepts the following keyword arguments:

        query_data: Optional[BaseModel]
            The model to validate the query data with.
        json_data: Optional[BaseModel]
            The model to validate the body data with.
        file_data: BaseModel | list[BaseModel]
            The model to validate the file or files data with.

    The decorator can be used as follows:

    @app.route("/endpoint", methods=["GET"])
    @validate(query_data=QueryData, json_data=BodyData, file_data=FileData)
    def endpoint(query_data, json_data, file_data):
        # The query_data, json_data and file_data are validated and available here
        # The return value of the function will be validated as well
        pass
    """

    def decorate(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Callable:
            query_model = func.__annotations__.get("query_data")
            if query_model:
                query_data = request.args.to_dict()
                query_result = validate_data(query_data, query_model)
                if not query_result:
                    return make_response(jsonify({"message": "error"}), 200)
                kwargs["query_data"] = query_result

            json_model = func.__annotations__.get("json_data")
            if json_model:
                json_data = request.get_json()
                json_result = validate_data(json_data, json_model)
                if not json_result:
                    return make_response(jsonify({"message": "error"}), 200)
                kwargs["json_data"] = json_result

            file_model = func.__annotations__.get("file_data")
            if file_model:
                if isinstance(file_model, GenericAlias):
                    file_data = request.files.getlist("file")
                    kwargs["file_data"] = [
                        validate_data(
                            {
                                "file": file,
                                "filename": file.filename,
                            },
                            File,
                        )
                        for file in file_data
                    ]
                else:
                    file_data = request.files.get("file")
                    kwargs["file_data"] = validate_data(
                        {
                            "file": file_data,
                            "filename": file_data.filename,
                        },
                        File,
                    )

            return func(*args, **kwargs)

        return wrapper

    return decorate
