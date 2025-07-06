"""Manage Validation."""

from __future__ import annotations

from flask import Flask, current_app, jsonify, make_response, request
from pydantic import ValidationError

from app.structures.models import Model


class Validate:
    """A validation class."""

    def __init__(self, app: Flask | None = None) -> None:
        """Initialize the database."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Register the before_request handler."""
        app.after_request(self._after_request)

    def _after_request(self) -> None:
        try:
            func = current_app.view_functions.get(request.endpoint)

            # if funcion has json_query argument with Pydantic model
            if json_model := func.__annotations__.get("json_query"):
                json_query = request.args.get("json_query")
                kwargs["json_query"] = json_model(**json_query)

            # if funcion has json_data argument with Pydantic model
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

