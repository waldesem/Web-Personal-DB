"""Manage dependencies."""

from functools import wraps
from typing import Callable, get_type_hints

from flask import Response, abort, current_app, jsonify, request
from pydantic import BaseModel, ValidationError, create_model

from app.models.models import BaseResponse, Result


def pydantify(
    model: BaseModel = BaseResponse,
    *,
    orm: bool = False,
    many: bool = False,
) -> Callable:
    """Decorate a function for validate and serialize data using Pydantic models."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Response:
            try:
                # Валидация входных данных параметров функции
                type_hints = get_type_hints(func)
                if params := {
                    k: (v, ...)
                    for k, v in type_hints.items()
                    if k not in ["return", "json_query", "json_data"]
                }:
                    model_class: BaseModel = create_model("Params", **params)
                    kwargs = model_class(**{key: kwargs[key] for key in params}).dict()

                if model_class := type_hints.get("json_query"):
                    kwargs["json_query"] = model_class(**request.args)

                if model_class := type_hints.get("json_data"):
                    json_data = request.get_json()
                    kwargs["json_data"] = model_class(**json_data)

                # Декорируемая функция
                result = func(*args, **kwargs)

                # Валидация выходных данных функции
                data, status = Result(data=result).data
                if orm:
                    if many:
                        return jsonify(
                            [model.from_orm(d).dict() for d in data],
                        ), status
                    return jsonify(model.from_orm(data).dict()), status

                if many:
                    return jsonify([model(**d).dict() for d in data]), status
                return jsonify(model(**data).dict()), status

            except (ValidationError, KeyError):
                current_app.logger.exception("Error pydantify data")

                return abort(400)

        return wrapper

    return decorator
