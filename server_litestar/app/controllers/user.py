"""User routes."""

from typing import Any, ClassVar

from litestar import Controller, Request, get, post
from litestar.security.jwt import Token  # noqa: TC002
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: TC002

from app.classes.classes import Roles
from app.depends.auth import role_guard
from app.models.models import Actions, User, UserForm
from app.tables.tables import Users
from app.utils.security import generate_password_hash
from config import Config


class UserController(Controller):
    """User Controller."""

    guards: ClassVar = [role_guard]

    @get("/users", opt={"roles": Roles.admin.value})
    async def get_users(self, db_session: AsyncSession) -> list[dict]:
        """Retrieve a list of users from the database."""
        async with db_session.begin():
            users = (await db_session.execute(select(Users))).scalars()
            return [User.model_validate(user).model_dump() for user in users]

    @post("/user/{user_id:int}", opt={"roles": Roles.admin.value})
    async def post_user_actions(
        self,
        user_id: int,
        data: Actions,
        request: Request[User, Token, Any],
        db_session: AsyncSession,
    ) -> dict:
        """Change a user's information in the database based on their user ID."""
        async with db_session.begin():
            user = await db_session.get(Users, user_id)
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
            db_session.commit()
            # Очистить кэш для id пользователей
            return {"message": "success"}

    @post("/user", opt={"roles": Roles.admin.value})
    async def post_user(self, data: UserForm, db_session: AsyncSession) -> dict:
        """Handle the POST request to create a user in the database."""
        # Проверить, существует ли уже пользователь с таким именем
        async with db_session.begin():
            user = (
                await db_session.execute(
                    select(Users).filter(Users.username == data.username),
                )
            ).all()
            if user:
                return {"message": "error"}
            await db_session.add(Users(**data.model_dump()))
            return {"message": "success"}
