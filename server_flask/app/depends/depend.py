from datetime import datetime, timedelta, timezone
from functools import lru_cache, wraps
from typing import Callable, Optional

import jwt
from flask import abort, current_app, g, jsonify, make_response, request
from pydantic import BaseModel, ValidationError
from werkzeug.local import LocalProxy

from ..model.tables import Users, db_session

current_user = LocalProxy(lambda: get_current_user(g.user_id))


def get_payload(header):
    """Validates a JWT token and returns the user ID.

    Parameters:
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
def get_current_user(user_id):
    """
    Retrieve the current user based on the user ID stored in the global variable 'g.user_id'.

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
        and user.pswd_create + timedelta(days=365) > datetime.now()
    ):
        return user.to_dict()
    return None


def create_token(user: dict):
    """
    Creates a JWT token containing the user's information.

    Args:
        user (dict): A dictionary containing the user's information.

    Returns:
        str: The JWT token.
    """
    if isinstance(user, dict):
        user.update({"exp": datetime.now(tz=timezone.utc) + timedelta(hours=12)})
        try:
            token = "Bearer " + jwt.encode(
                user,
                current_app.config["JWT_SECRET_KEY"],
                algorithm="HS256",
            )
            return token
        except jwt.exceptions.InvalidTokenError:
            return None
    return None


def jwt_required():
    """
    Decorator function that checks if the request contains a valid JWT token.

    The decorated function checks if the request contains a valid JWT token in the
    'Authorization' header. If the token is valid, the decorated function is executed.
    Otherwise, a 401 HTTP status code is returned.

    Parameters:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization")
            user_id = get_payload(header)
            if user_id:
                g.user_id = user_id
                return func(*args, **kwargs)
            abort(401)

        return wrapper

    return decorator


def roles_required(*roles):
    def decorator(func):
        @jwt_required()
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.get("role") in roles:
                return func(*args, **kwargs)
            abort(403)

        return wrapper

    return decorator


def validate():
    """
    Decorator for validating request data using Pydantic models.

    This decorator checks the request query, body and headers for validation errors.
    If any errors are found, the decorator returns a 400 response with a JSON body
    containing a dictionary with the validation errors.

    The decorator accepts the following keyword arguments:

        query_data: Optional[BaseModel]
            The model to validate the query data with.
        json_data: Optional[BaseModel]
            The model to validate the body data with.
        return: result
            The model to validate the response data with.

    The decorator can be used as follows:

    @app.route("/endpoint", methods=["GET"])
    @validate(query_data=QueryData, json_data=BodyData, return=ResponseData)
    def endpoint(query_data, json_data):
        # The query_data and json_data are validated and available here
        # The return value of the function will be validated as well
        pass

    :param query_data: The model to validate the query data with.
    :param json_data: The model to validate the body data with.
    :return: The decorated function.
    """

    def decorate(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            err = {}
            query_model: Optional[BaseModel] = func.__annotations__.get("query_data")
            if query_model:
                query_data = request.args.to_dict()
                try:
                    kwargs["query_data"] = query_model(**query_data)
                except ValidationError as ve:
                    err["query_data"] = ve.errors()

            json_model: Optional[BaseModel] = func.__annotations__.get("json_data")
            if json_model:
                content_type = request.headers.get("Content-Type", "").lower()
                if content_type.split(";")[0] != "application/json":
                    body = {"detail": f"Unsupported media type: '{content_type}'"}
                    return make_response(jsonify(body), 415)

                json_data = request.get_json()
                try:
                    kwargs["json_data"] = json_model(**json_data)
                except ValidationError as ve:
                    err["json_data"] = ve.errors()

            if err:
                return make_response(
                    jsonify({"message": "error", "validation_error": err}), 400
                )

            res = func(*args, **kwargs)

            return res

        return wrapper

    return decorate


def serialize():
    def decorate(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            err = {}
            result = func(*args, **kwargs)
            
            try:
                if hasattr(result, "__iter__"):
                    result = [res.to_dict() for res in result]
                else:
                    result = result.to_dict()
            except Exception as e:
                err["result"] = e

            if err:
                return make_response(
                    jsonify({"message": "error", "serialization_error": err}), 400
                )
            
            return make_response(jsonify(result), 200)

        return wrapper

    return decorate