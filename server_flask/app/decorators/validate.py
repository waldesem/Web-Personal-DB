"""Manage dependencies."""

from functools import wraps
from typing import Callable, get_type_hints

from flask import Response, abort, current_app, jsonify, request
from pydantic import BaseModel, ValidationError

from app.models.models import Items, Model, Result

# Dict of models for validation
MODELS = {
    cls.__modelname__: cls
    for cls in Model.__subclasses__()
    if hasattr(cls, "__modelname__")
}


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
    def endpoint(json_data: Model, json_query: Model):
        # The json_data or/and json_query are validated and available here
    """

    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> Callable:
        """Validate request data using Pydantic models."""
        try:
            # if funcion has json_query argument with Pydantic model
            if model_class := get_type_hints(func).get("json_query"):
                kwargs["json_query"] = model_class(**request.args)

            # if funcion has json_data argument with Pydantic model
            if model_class := get_type_hints(func).get("json_data"):
                if model_class.__name__ == "Model":
                    item = Items(item=kwargs.get("item"))
                    model_class = MODELS[item.item]
                json_data = request.get_json()
                kwargs["json_data"] = model_class(**json_data)

        except ValidationError:
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

                if model.__name__ == "Model":
                    item = Items(item=kwargs.get("item"))
                    model_class = MODELS[item.item]
                else:
                    model_class = model

                if isinstance(data, tuple):
                    data = data[0]
                if isinstance(data, list):
                    return jsonify(
                        [model_class.from_orm(r).dict(exclude_none=True) for r in data],
                    ), status
                return jsonify(
                    model_class.from_orm(data).dict(exclude_none=True),
                ), status
            except ValidationError:
                current_app.logger.exception("Error serialize data")

            return abort(400)

        return wrapper

    return decorator
