"""Manage dependencies."""

from __future__ import annotations

from functools import wraps
from typing import Callable

from flask import current_app, jsonify, make_response, request
from pydantic import ValidationError

from app.models.models import Model


def validate(func: Callable) -> Callable:
    """Decorate a function for validating request data using Pydantic models.

    The decorator accepts the following keyword arguments:
        json_query: Optional[BaseModel]
            The model to validate the query parameters with.
        json_data: Optional[BaseModel]
            The model to validate the body data with.

    The decorator can be used as follows:

    @app.route("/endpoint", methods=["GET"])
    @validate(json_data=BodyData, json_query=QueryData)
    def endpoint(json_data, json_query):
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
                if json_model.__name__ == "Model":
                    models = {
                        cls.__modelname__: cls
                        for cls in Model.__subclasses__()
                        if hasattr(cls, "__modelname__")
                    }
                    json_model = models[f"input_{kwargs["item"]}"]
                json_data = request.get_json()
                kwargs["json_data"] = json_model(**json_data)

        except ValidationError:
            current_app.logger.exception("Error validating data")
            return make_response(jsonify({"message": "error"}))
        else:
            return func(*args, **kwargs)

    return wrapper
