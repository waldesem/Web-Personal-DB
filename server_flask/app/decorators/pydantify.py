"""Manage dependencies."""

from collections.abc import Callable
from functools import wraps
from typing import get_type_hints

from flask import abort, current_app, request
from pydantic import BaseModel, ValidationError, create_model

from app.models.models import models


def get_model(model: type[BaseModel], kwargs: dict) -> type[BaseModel]:
    """Get Pydantic model class."""
    return models.get(kwargs["item"]) if model.__name__ == "Model" else model


def validize() -> Callable:
    """Decorate a function for validate data using Pydantic models."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Callable:
            try:
                type_hints = get_type_hints(func)
                if params := {
                    k: (v, ...)
                    for k, v in type_hints.items()
                    if k not in ["return", "json_query", "json_data"]
                }:
                    model = create_model("Params", **params)
                    kwargs = model(**{key: kwargs[key] for key in params}).model_dump()

                if model := type_hints.get("json_query"):
                    pydantic_model = get_model(model, kwargs)
                    kwargs["json_query"] = pydantic_model(**request.args)

                if model := type_hints.get("json_data"):
                    pydantic_model = get_model(model, kwargs)
                    json_data = request.get_json()
                    kwargs["json_data"] = pydantic_model(**json_data)

                # Декорируемая функция
                return func(*args, **kwargs)

            except ValidationError:
                current_app.logger.exception("Error validating data")
                return abort(400)

        return wrapper

    return decorator
