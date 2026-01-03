"""Login routes."""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

import jwt
from litestar import Controller, Request, get, post
from litestar.exceptions import NotAuthorizedException
from litestar.security.jwt import Token  # noqa: TC002
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: TC002

from app.depends.auth import get_current_user, jwt_auth, store
from app.models.models import Login, User  # noqa: TC001
from app.tables.tables import Users
from app.utils.security import check_password_hash, generate_password_hash
from config import Config


class AuthController(Controller):
    """Auth controller."""

    path = "/auth"

    @post("/{action:str}")
    async def post_login(
        self,
        action: Literal["login", "update"],
        data: Login,
        db_session: AsyncSession,
    ) -> dict:
        """Handle the login process."""
        async with db_session.begin():
            user = (
                await db_session.execute(
                    select(Users).filter_by(username=data.username),
                )
            ).scalar_one_or_none()

            if not user or user.blocked or user.deleted:
                return {"message": "invalid"}

            if not check_password_hash(user.passhash, data.password):
                if user.attempt < 5:
                    user.attempt += 1
                else:
                    user.blocked = True
                return {"message": "invalid"}

            if action == "update" and data.new_pswd:
                user.passhash = generate_password_hash(data.new_pswd)
                user.pswd_create = datetime.now(tz=timezone.utc)  # noqa: UP017
                user.change_pswd = False
                user.attempt = 0
                return {"message": "updated"}

            delta_change = datetime.now() - user.pswd_create
            if not user.change_pswd and delta_change.days < 365:
                user.attempt = 0
                return {
                    "message": "success",
                    "access_token": jwt_auth.create_token(
                        identifier=str(user.id),
                        token_unique_jwt_id=secrets.token_hex(10),
                        token_expiration=timedelta(
                            minutes=Config.ACCESS_SECRET_KEY_LIVE,
                        ),
                    ),
                    "refresh_token": jwt.encode(
                        {
                            "id": str(user.id),
                            "jti": secrets.token_hex(10),
                            "exp": datetime.now(tz=timezone.utc)  # noqa: UP017
                            + timedelta(minutes=Config.REFRESH_SECRET_KEY_LIVE),
                        },
                        Config.REFRESH_SECRET_KEY,
                        algorithm="HS256",
                    ),
                }
            return {"message": "denied"}

    @post("/logout")
    async def logout(self, token: Token, request: Request) -> dict:
        """Logout the user."""
        refresh = await request.json()
        decoded = jwt.decode(
            refresh.get("refresh_token"),
            Config.REFRESH_SECRET_KEY,
            algorithms=["HS256"],
        )
        store.set("jti", token.jti, expires_in=token.exp)
        store.set("jti", decoded["jti"], expires_in=decoded["exp"])
        await store.delete_expired()

    @post("/refresh")
    async def refresh_token(self, request: Request) -> dict:
        """Refresh the access token."""
        token: dict = await request.json()
        decoded = jwt.decode(
            token.get("refresh_token"),
            Config.REFRESH_SECRET_KEY,
            algorithms=["HS256"],
            verify=True,
        )
        return {
            "access_token": jwt_auth.create_token(
                identifier=str(decoded["id"]),
                token_unique_jwt_id=secrets.token_hex(10),
                token_expiration=timedelta(minutes=Config.ACCESS_SECRET_KEY_LIVE),
            ),
        }

    @get("/session")
    async def get_session(
        self,
        request: Request[User, Token, Any],
        db_session: AsyncSession,
    ) -> dict | Exception:
        """Retrieve an item from the database based on the provided item ID."""
        if not request.user:
            raise NotAuthorizedException
        return await get_current_user(request.user.id, db_session)
