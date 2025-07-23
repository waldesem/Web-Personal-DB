"""Manage dependencies."""

from functools import wraps
from typing import Callable, get_type_hints

from flask import Response, abort, current_app, jsonify, request
from pydantic import BaseModel, ValidationError, create_model

from app.models.models import Result


def validate(func: Callable) -> Callable:
    """Decorate a function for validating request data using Pydantic models.

    The decorator can be used as follows:

    @app.route("/endpoint/<data>", methods=["GET", "POST","PATCH"])
    @validate
    def endpoint(data: str, json_data: Model, json_query: Model):
        # The data, json_data or/and json_query are validated and available here
    """

    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> Callable:
        """Validate request data using Pydantic models."""
        try:
            type_hints = get_type_hints(func)
            if params := {
                k: (v, ...)
                for k, v in type_hints.items()
                if k not in ["return", "json_query", "json_data"]
            }:
                model_class = create_model(func.__name__, **params)
                data = dict(zip(params.keys(), args))
                args = [d[1] for d in model_class(**data)]

            if model_class := type_hints.get("json_query"):
                kwargs["json_query"] = model_class(**request.args)

            if model_class := type_hints.get("json_data"):
                json_data = request.get_json()
                kwargs["json_data"] = model_class(**json_data)

        except (ValidationError, KeyError):
            current_app.logger.exception("Error validating data")
            return abort(400)
        else:
            return func(*args, **kwargs)

    return wrapper


def serialize(model: BaseModel = None) -> Callable:
    """Decorate a function for serialize data using Pydantic models.

    Args:
        model (BaseModel): The model for validation.

    Returns:
        function: The decorated function.

    The decorator can be used as follows:

    @app.route("/endpoint", methods=["GET"])
    @serialize(ModelOut)
    def endpoint():
        # Function body

    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Response:
            result = func(*args, **kwargs)
            try:
                data, status = Result(data=result).data
                if isinstance(data, str):
                    return jsonify({"message": data}), status
                if isinstance(data, dict):
                    return jsonify(data), status

                if isinstance(data, tuple):
                    data = data[0]
                if isinstance(data, list):
                    return jsonify(
                        [model.from_orm(d).dict(exclude_none=True) for d in data],
                    ), status
                return jsonify(
                    model.from_orm(data).dict(exclude_none=True),
                ), status
            except (ValidationError, KeyError):
                current_app.logger.exception("Error serialize data")

            return abort(400)

        return wrapper

    return decorator
