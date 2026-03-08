"""User routes."""

from typing import Any, ClassVar

import bcrypt
from litestar import Controller, Request, get, post
from litestar.exceptions import PermissionDeniedException
from litestar.security.jwt import Token
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.middleware.auth import role_guard
from app.structures.classes import Roles
from app.structures.models import Actions, User, UserForm
from app.structures.tables import Users
from constants import DEFAULT_PASSWORD

ta = TypeAdapter(list[User])


class UserController(Controller):
    """User Controller."""

    guards: ClassVar = [role_guard]
    opt: ClassVar = {"roles": Roles.admin.value}

    @get("/users")
    async def get_users(self, db_session: AsyncSession) -> list[User]:
        """Retrieve a list of users from the database.

        Args:
            db_session: AsyncSession.

        Returns:
            Response with status code 200 and a list of users.

        """
        async with db_session.begin():
            users = (await db_session.execute(select(Users))).scalars()
            return ta.validate_python(users, from_attributes=True)

    @post("/user")
    async def post_user(self, data: UserForm, db_session: AsyncSession) -> None:
        """Handle the POST request to create a user in the database.

        Args:
            data: UserForm.
            db_session: AsyncSession.

        Returns:
            Response with status code 201.

        """
        # Проверить, существует ли уже пользователь с таким именем
        user = (
            await db_session.execute(
                select(Users).filter(Users.username == data.username),
            )
        ).all()
        if user:
            raise PermissionDeniedException
        db_session.add(Users(**data.model_dump()))

    @post("/user/{user_id:int}")
    async def post_user_actions(
        self,
        user_id: int,
        data: Actions,
        request: Request[User, Token, Any],
        db_session: AsyncSession,
    ) -> None:
        """Change a user's information in the database based on their user ID.

        Args:
            user_id: User ID.
            data: Actions.
            request: Request.
            db_session: AsyncSession.

        Returns:
            Response with status code 201.

        """
        user = await db_session.get(Users, user_id)
        # Если пользователь не найден или пытается изменить собственный профиль
        if not user or request.user.id == user.id:
            raise PermissionDeniedException

        if data.item == "reset":
            # Сбросить пароль пользователя и обнулить попытки входа
            user.passhash = bcrypt.hashpw(DEFAULT_PASSWORD.encode(), bcrypt.gensalt())
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
