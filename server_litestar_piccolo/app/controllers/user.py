"""User routes."""

from typing import Any, ClassVar

import bcrypt
from litestar import Controller, Request, get, post
from litestar.exceptions import ValidationException
from litestar.security.jwt import Token
from pydantic import TypeAdapter

from app.classes.classes import Roles
from app.middleware.auth import role_guard
from app.models.user import Actions, User, UserForm
from app.tables.tables import Users
from constants import DEFAULT_PASSWORD

ta = TypeAdapter(list[User])


class UserController(Controller):
    """User Controller."""

    guards: ClassVar = [role_guard]
    opt: ClassVar = {"roles": Roles.admin.value}

    @get("/users")
    async def get_users(self) -> list[User]:
        """Retrieve a list of users from the database.

        Returns:
            Response with status code 200 and a list of users.

        """
        users = await Users.select()
        return ta.validate_python(users)

    @post("/user")
    async def post_user(self, data: UserForm) -> None:
        """Handle the POST request to create a user in the database.

        Args:
            data: UserForm.

        Returns:
            Response with status code 201.

        """
        # Проверить, существует ли уже пользователь с таким именем
        if not (
            await Users.insert(
                Users(
                    **data.model_dump(),
                    passhash=bcrypt.hashpw(DEFAULT_PASSWORD.encode(), bcrypt.gensalt()),
                ),
            )
            .on_conflict(action="DO NOTHING")
            .returning(Users.id)
        ):
            raise ValidationException

    @post("/user/{user_id:int}")
    async def post_user_actions(
        self,
        user_id: int,
        data: Actions,
        request: Request[User, Token, Any],
    ) -> None:
        """Change a user's information in the database based on their user ID.

        Args:
            user_id: User ID.
            data: Actions.
            request: Request.

        Returns:
            Response with status code 201.

        """
        user = await Users.objects().get(Users.id == user_id)
        # Если пользователь не найден или пытается изменить собственный профиль
        if not user or request.user.id == user.id:
            raise ValidationException

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
            user.change_pswd = True
        await user.save()
