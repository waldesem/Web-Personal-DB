"""User routes."""

from typing import Any

from flask import Blueprint, current_app, g
from sqlalchemy import Row, Sequence, select
from werkzeug.security import generate_password_hash

from app import db
from app.classes.classes import Roles
from app.decorators.depend import auth_required, get_current_user
from app.decorators.pydantify import serialize, validize
from app.models.models import User, UserActions, UserForm
from app.tables.tables import Users

bp = Blueprint("users", __name__)


@bp.get("/users")
@serialize(User, orm=True, many=True)
@validize()
@auth_required(Roles.admin.value)
def get_users() -> tuple[Sequence[Row[Any]], int]:
    """Retrieve a list of users from the database."""
    # Преобразовать результат в список словарей и вернуть в качестве ответа
    return db.session.execute(Users).all(), 200


@bp.post("/user/<user_id>")
@serialize()
@validize()
@auth_required(Roles.admin.value)
def post_user_actions(user_id: int, json_data: UserActions) -> tuple[dict, int]:
    """Change a user's information in the database based on their user ID."""
    user = db.session.get(Users, user_id)
    # Если пользователь не найден или пытается изменить собственный профиль
    if not user or g.user.id == user.id:
        return {"message": "error"}, 200

    if json_data.item == "reset":
        # Сбросить пароль пользователя и обнулить попытки входа
        user.passhash = generate_password_hash(
            current_app.config["DEFAULT_PASSWORD"],
        )
        user.attempt = 0
        user.blocked = False
        user.change_pswd = True
    elif json_data.item == "block":
        # Заблокировать или разблокировать пользователя
        user.blocked = not user.blocked
    elif json_data.item == "delete":
        # Удалить или восстановить пользователя
        user.deleted = not user.deleted
    elif json_data.item in [reg.value for reg in Roles]:
        # Изменить роль пользователя
        user.role = json_data.item
    db.session.commit()
    # Очистить кэш для id пользователей
    get_current_user.cache_clear()
    return {"message": "success"}, 201


@bp.post("/user")
@serialize()
@validize()
@auth_required(Roles.admin.value)
def post_user(json_data: UserForm) -> tuple[dict, int]:
    """Handle the POST request to create a user in the database."""
    # Проверить, существует ли уже пользователь с таким именем
    user = db.session.execute(
        select(Users).filter(Users.username == json_data.username),
    ).all()
    if user:
        return {"message": "error"}, 200
    db.session.add(Users(**json_data.model_dump()))
    db.session.commit()
    return {"message": "success"}, 201
