"""Manage dependencies."""

from __future__ import annotations

from functools import wraps
from typing import Callable

from flask import Response, abort, current_app, jsonify, request
from pydantic import BaseModel, ValidationError

from app.models.models import BaseResponse, ModelOut


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
            if model := func.__annotations__.get("json_query"):
                json_query = request.args
                kwargs["json_query"] = model(**json_query)

            # if funcion has json_data argument with Pydantic model
            if model := func.__annotations__.get("json_data"):
                # if json model annotation is InputModel
                if model.__name__ == "ModelIn":
                    models = {
                        cls.__modelname__: cls
                        for cls in model.__subclasses__()
                        if hasattr(cls, "__modelname__")
                    }
                    model = models[kwargs["item"]]
                json_data = request.get_json()
                kwargs["json_data"] = model(**json_data)

        except ValidationError:
            current_app.logger.exception("Error validating data")
            return abort(400)
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
            if (
                isinstance(result, (tuple, list))
                and len(result) == 2
                and isinstance(result[1], int)
                and result[1] in [200, 201, 204, 500]
            ):
                if isinstance(result[0], dict):
                    return jsonify(result[0]), result[1]
                if isinstance(result, str):
                    return jsonify({"message": result[0]}), result[1]

                if model.__name__ == "ModelOut":
                    models = {
                        cls.__modelname__: cls
                        for cls in model.__subclasses__()
                        if hasattr(cls, "__modelname__")
                    }
                    serial = ModelOut[models[kwargs["item"]]]
                else:
                    serial = model

                try:
                    if isinstance(result[0], list):
                        return jsonify(
                            [serial.from_orm(r).dict() for r in result[0]],
                        ), result[1]
                    return jsonify(serial.from_orm(result[0]).dict()), result[1]
                except ValidationError:
                    current_app.logger.exception("Error serialize data")

            return abort(400)

        return wrapper

    return decorator
