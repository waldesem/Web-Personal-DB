"""User routes."""

from typing import Any

from litestar import Request, get, post
from litestar.security.jwt import Token
from sqlalchemy import select

from app.classes.classes import Roles
from app.depends.auth import get_current_user, role_guard
from app.models.models import Actions, User, UserForm
from app.tables.tables import Users, session
from app.utils.security import generate_password_hash
from config import Config


@get("/users")
async def get_users(
    sync_to_thread: bool = False,
    guards=[role_guard(role=Roles.admin.value)],
) -> list[dict]:
    """Retrieve a list of users from the database."""
    users = session.execute(select(Users)).scalars()
    return [User.model_validate(user).model_dump() for user in users]


@post("/user/{user_id:int}")
async def post_user_actions(
    request: Request[User, Token, Any],
    user_id: int,
    data: Actions,
    sync_to_thread: bool = False,
    guards=[role_guard(role=Roles.admin.value)],
) -> dict:
    """Change a user's information in the database based on their user ID."""
    user = session.get(Users, user_id)
    # Если пользователь не найден или пытается изменить собственный профиль
    if not user or request.user.id == user.id:
        return {"message": "error"}

    if data.item == "reset":
        # Сбросить пароль пользователя и обнулить попытки входа
        user.passhash = generate_password_hash(Config.DEFAULT_PASSWORD)
        user.attempt = 0
        user.blocked = False
        user.change_pswd = True
    elif data.item == "block":
        # Заблокировать или разблокировать пользователя
        user.blocked = not user.blocked
    elif data.item == "delete":
        # Удалить или восстановить пользователя
        user.deleted = not user.deleted
    elif data.item in [reg.value for reg in Roles]:
        # Изменить роль пользователя
        user.role = data.item
    session.commit()
    # Очистить кэш для id пользователей
    get_current_user.cache_clear()
    return {"message": "success"}


@post("/user")
async def post_user(
    data: UserForm,
    sync_to_thread: bool = False,
    guards=[role_guard(role=Roles.admin.value)],
) -> dict:
    """Handle the POST request to create a user in the database."""
    # Проверить, существует ли уже пользователь с таким именем
    user = session.execute(
        select(Users).filter(Users.username == data.username),
    ).all()
    if user:
        return {"message": "error"}
    session.add(Users(**data.model_dump()))
    session.commit()
    return {"message": "success"}
