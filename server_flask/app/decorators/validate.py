"""Manage dependencies."""

from functools import wraps
from typing import Callable, get_type_hints

from flask import Response, abort, current_app, jsonify, request
from pydantic import BaseModel, ValidationError

from app.models.models import Items, ModelIn, ModelOut

# Dict of models for validation
MODELS_IN = {
    cls.__modelname__: cls
    for cls in ModelIn.__subclasses__()
    if hasattr(cls, "__modelname__")
}

# Dict of models for serialization
MODELS_OUT = {
    cls.__modelname__: cls
    for cls in ModelOut.__subclasses__()
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
    def endpoint(json_data: ModelIn, json_query: ModelIn):
        # The json_data or/and json_query are validated and available here
    """

    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> Callable:
        """Validate request data using Pydantic models."""
        try:
            # if funcion has json_query argument with Pydantic model
            if model_class := get_type_hints(func).get("json_query"):
                json_query = request.args
                kwargs["json_query"] = model_class(**json_query)

            # if funcion has json_data argument with Pydantic model
            if model_class := get_type_hints(func).get("json_data"):
                # if json model annotation is ModelIn
                if model_class.__name__ == "ModelIn":
                    item = Items(item=kwargs.get("item"))
                    model_class = MODELS_IN[item.item]
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
            result: tuple[str | dict | BaseModel, int] = func(*args, **kwargs)
            if (
                result
                and isinstance(result, tuple)
                and len(result) == 2
                and isinstance(result[1], int)
            ):
                response, status = result
                if isinstance(response, str):
                    response = {"message": response}
                if isinstance(response, dict):
                    return jsonify(response), status

                try:
                    if model.__name__ == "ModelOut":
                        item = Items(item=kwargs.get("item"))
                        model_class = MODELS_OUT[item.item]
                    else:
                        model_class = model

                    if isinstance(response, tuple):
                        response = response[0]
                    if isinstance(response, list):
                        resp = [model_class.from_orm(r).dict() for r in response]
                        return jsonify(resp), status
                    return jsonify(model_class.from_orm(response).dict()), status
                except ValidationError:
                    current_app.logger.exception("Error serialize data")

            return abort(400)

        return wrapper

    return decorator
