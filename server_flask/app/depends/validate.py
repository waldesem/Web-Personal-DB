"""Manage dependencies."""

from __future__ import annotations

from functools import wraps
from typing import Callable

from flask import current_app, jsonify, make_response, request
from pydantic import ValidationError

from app.structures.models import Model


def validate(func: Callable) -> Callable:
    """Decorate a function for validating request data using Pydantic models.

    The decorator accepts the following keyword arguments:
        json_data: Optional[BaseModel]
            The model to validate the body data with.

    The decorator can be used as follows:

    @app.route("/endpoint", methods=["GET"])
    @validate(json_data=BodyData)
    def endpoint(json_data):
        # The json_data are validated and available here
        pass
    """

    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> Callable:
        """Validate request data using Pydantic models."""
        try:
            # if funcion has json model argument with Pydantic model
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
