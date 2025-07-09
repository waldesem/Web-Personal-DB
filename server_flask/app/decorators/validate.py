"""Manage dependencies."""

from __future__ import annotations

from functools import wraps
from typing import Callable

from flask import Response, current_app, jsonify, make_response, request
from pydantic import BaseModel, ValidationError

from app.models.models import BaseResponse, ModelIn, ModelOut


def validate(func: Callable) -> Callable:
    """Decorate a function for validating request data using Pydantic models.

    The decorator accepts the following keyword arguments:
        json_query: Optional[BaseModel]
            The model to validate the query parameters with.
        json_data: Optional[BaseModel]
            The model to validate the body data with.

    The decorator can be used as follows:

    @app.route("/endpoint", methods=["GET", "POST","PATCH"])
    @validate
    def endpoint(json_data: ModelIn, json_query: ModelIn):
        # The json_data or/and json_query are validated and available here
    """

    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> Callable:
        """Validate request data using Pydantic models."""
        try:
            # if funcion has json_query argument with Pydantic model
            if json_model := func.__annotations__.get("json_query"):
                json_query = request.args
                kwargs["json_query"] = json_model(**json_query)

            # if funcion has json_data argument with Pydantic model
            if json_model := func.__annotations__.get("json_data"):
                # if json model annotation is InputModel
                if json_model.__name__ == "ModelIn":
                    models = {
                        cls.__modelname__: cls
                        for cls in ModelIn.__subclasses__()
                        if hasattr(cls, "__modelname__")
                    }
                    json_model = models[f"input_{kwargs['item']}"]
                json_data = request.get_json()
                kwargs["json_data"] = json_model(**json_data)

        except ValidationError:
            current_app.logger.exception("Error validating data")
            return make_response(jsonify({"message": "error"}))
        else:
            return func(*args, **kwargs)

    return wrapper


def serialize(model: BaseModel = BaseResponse) -> Callable:
    """Decorate a function for serialize data using Pydantic models.

    Args:
        model (BaseModel): The model for validation.

    Returns:
        function: The decorated function.

    The decorator can be used as follows:

    @app.route("/endpoint", methods=["GET"])
    @serialize(ModelOut)
    def endpoint() -> Base  # SqlAlchemy Model, dict, str:
        # Function body

    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Response:
            result = func(*args, **kwargs)
            if model.__name__ == "ModelOut":
                models = {
                    cls.__modelname__: cls
                    for cls in ModelOut.__subclasses__()
                    if hasattr(cls, "__modelname__")
                }
                model = models[f"output_{kwargs['item']}"]
            try:
                if (
                    isinstance(result, tuple)
                    and len(result) == 2
                    and isinstance(result[1], int)
                    and 199 < result[1] < 300
                ):
                    if isinstance(result[0], dict):
                        serialized = model.parse_obj(result[0]).json()
                    elif isinstance(result, (str, int)):
                        serialized = BaseResponse(message=str(result[0])).json()
                    else:
                        serialized = model.from_orm(result[0]).json()
            except ValidationError:
                current_app.logger.exception("Error serialize data")
            else:
                response = make_response(serialized)
                response.mimetype = "application/json"
                response.status_code = result[1]
                return response

            return make_response(jsonify({"message": "error"}))

        return wrapper

    return decorator
