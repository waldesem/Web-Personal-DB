"""Manage dependencies."""

from collections.abc import Callable
from functools import wraps
from typing import get_type_hints

from flask import Response, abort, current_app, jsonify, request
from pydantic import ValidationError, create_model

from app.models.models import BaseModel, BaseResponse, models


def validize() -> Callable:
    """Decorate a function for validate data using Pydantic models."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> tuple[Response, int]:
            try:
                type_hints = get_type_hints(func)
                if params := {
                    k: (v, ...)
                    for k, v in type_hints.items()
                    if k not in ["return", "json_query", "json_data"]
                }:
                    model_class = create_model("Params", **params)
                    kwargs = model_class(**{key: kwargs[key] for key in params}).dict()

                if model_class := type_hints.get("json_query"):
                    orm_model = (
                        models.get(kwargs["item"])
                        if model_class.__name__ == "Model"
                        else model_class
                    )
                    kwargs["json_query"] = orm_model(**request.args)

                if model_class := type_hints.get("json_data"):
                    orm_model = (
                        models.get(kwargs["item"])
                        if model_class.__name__ == "Model"
                        else model_class
                    )
                    json_data = request.get_json()
                    kwargs["json_data"] = orm_model(**json_data)

                # Декорируемая функция
                return func(*args, **kwargs)

            except (ValidationError, KeyError):
                current_app.logger.exception("Error pydantify data")

                return abort(400)

        return wrapper

    return decorator


def serialize(
    model: type[BaseModel] = BaseResponse,
    *,
    orm: bool = False,
    many: bool = False,
) -> Callable:
    """Decorate a function for serialize data using Pydantic models."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> tuple[Response, int]:
            try:
                data, status = func(*args, **kwargs)
                if orm:
                    # Если модель не указана, то используем модель из словаря models
                    orm_model = (
                        models.get(kwargs["item"])
                        if model.__name__ == "Model"
                        else model
                    )
                    if many:
                        return jsonify(
                            [orm_model.from_orm(d).dict() for d in data],
                        ), status
                    return jsonify(orm_model.from_orm(data).dict()), status

                if many:
                    return jsonify([model(**d).dict() for d in data]), status
                return jsonify(model(**data).dict()), status

            except (ValidationError, KeyError):
                current_app.logger.exception("Error pydantify data")

                return abort(400)

        return wrapper

    return decorator
