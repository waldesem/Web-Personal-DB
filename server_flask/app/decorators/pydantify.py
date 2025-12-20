"""Manage dependencies."""

from collections.abc import Callable
from functools import wraps
from typing import get_type_hints

from flask import abort, current_app, request
from pydantic import BaseModel, ValidationError

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
                # Получаем типы аргументов функции
                type_hints: dict[str, BaseModel] = get_type_hints(func)
                # Проверяем аргументы на соответствие Pydantic моделям
                for arg, model in type_hints.items():
                    pydantic_model = (
                        models[kwargs["item"]] if model.__name__ == "Model" else model
                    )
                    if arg == "json_query":
                        kwargs[arg] = pydantic_model(**request.args)
                    if arg == "json_data":
                        kwargs[arg] = pydantic_model(**request.get_json())

                # Декорируемая функция
                return func(*args, **kwargs)

            except ValidationError:
                current_app.logger.exception("Error validating data")
                abort(400)

        return wrapper

    return decorator
