"""Module for managing dependencies."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from functools import lru_cache, wraps
from typing import Callable

import jwt
from flask import abort, current_app, g, jsonify, make_response, request
from pydantic import BaseModel, ValidationError
from werkzeug.local import LocalProxy

from app.model.models import File
from app.model.tables import Users, db_session

current_user = LocalProxy(lambda: get_current_user(g.user_id))


def get_payload(header: str | None = None) -> int | None:
    """Validate a JWT token and returns the user ID.

    Args:
        header (str): The JWT token to validate.

    Returns:
        int or None: The user ID if the token is valid, None if not.

    """
    if isinstance(header, str) and header.startswith("Bearer "):
        try:
            return jwt.decode(
                header[7:],
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"],
            )["id"]
        except jwt.exceptions.PyJWTError:
            current_app.logger.info("Invalid token")
            return None
    return None


@lru_cache(maxsize=2)
def get_current_user(user_id: int) -> dict:
    """Retrieve the current user stored in the global variable 'g.user_id'.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict or None: A instance containing the user's information if the user exists,
            is not blocked, not deleted, and has not changed password in the last year.
            Otherwise, returns None.

    """
    user = db_session.get(Users, user_id)
    if (
        user
        and not user.blocked
        and not user.deleted
        and not user.change_pswd
        and user.pswd_create + timedelta(days=365) > datetime.now()  # noqa: DTZ005
    ):
        return user.to_dict()
    return {}


def create_token(user: Users) -> str:
    """Create a JWT token containing the user's information.

    Args:
        user (Users): The user object.

    Returns:
        str: The JWT token.

    """
    try:
        return "Bearer " + jwt.encode(
            {
                "id": user.id,
                "fullname": user.fullname,
                "username": user.username,
                "email": user.email,
                "region": user.region,
                "role": user.role,
                "exp": datetime.now(tz=timezone.utc) + timedelta(hours=12),
            },
            current_app.config["JWT_SECRET_KEY"],
            algorithm="HS256",
        )
    except jwt.exceptions.InvalidTokenError:
        return None
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
            user_id = get_payload(header)
            if user_id:
                g.user_id = user_id
                return func(*args, **kwargs)
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
            if current_user.get("role") in roles:
                return func(*args, **kwargs)
            return abort(403)

        return wrapper

    return decorator


def validate() -> Callable:  # noqa: C901
    """Decorate a function for validating request data using Pydantic models.

    The decorator accepts the following keyword arguments:

        query_data: Optional[BaseModel]
            The model to validate the query data with.
        json_data: Optional[BaseModel]
            The model to validate the body data with.
        file_data: BaseModel | list[BaseModel]
            The model to validate the file data with.

    The decorator can be used as follows:

    @app.route("/endpoint", methods=["GET"])
    @validate(query_data=QueryData, json_data=BodyData, file_data=FileData)
    def endpoint(query_data, json_data):
        # The query_data and json_data are validated and available here
        # The return value of the function will be validated as well
        pass
    """

    def decorate(func: Callable) -> Callable:  # noqa: C901
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Callable:  # noqa: C901
            err = []
            query_model: BaseModel | None = func.__annotations__.get("query_data")
            if query_model:
                query_data = request.args.to_dict()
                try:
                    kwargs["query_data"] = query_model(**query_data)
                except ValidationError as ve:
                    err.append(str(ve))

            json_model: BaseModel | None = func.__annotations__.get("json_data")
            if json_model:
                content_type = request.headers.get("Content-Type", "").lower()
                if content_type.split(";")[0] != "application/json":
                    body = {"message": f"Unsupported media type: '{content_type}'"}
                    return make_response(jsonify(body), 415)

                json_data = request.get_json()
                try:
                    kwargs["json_data"] = json_model(**json_data)
                except ValidationError as ve:
                    err.append(str(ve))

            file_model: BaseModel | list[BaseModel] = func.__annotations__.get(
                "file_data",
            )
            if file_model:
                content_type = request.headers.get("Content-Type", "").lower()
                if content_type.split(";")[0] != "multipart/form-data":
                    body = {"message": f"Unsupported media type: '{content_type}'"}
                    return make_response(jsonify(body), 415)

                try:
                    iter(file_model)
                    file_data = request.files.getlist("file")
                    try:
                        kwargs["file_data"] = [
                            File(file=f, filename=f.filename) for f in file_data
                        ]
                    except ValidationError as ve:
                        err.append(str(ve))
                except TypeError:
                    file_data = request.files.get("file")
                    try:
                        kwargs["file_data"] = File(
                            file=file_data,
                            filename=file_data.filename,
                        )
                    except ValidationError as ve:
                        err.append(str(ve))
            if err:
                current_app.logger.error("; ".join(err))
                return make_response(jsonify({"message": "error"}), 200)

            return func(*args, **kwargs)

        return wrapper

    return decorate
