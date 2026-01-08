"""Login routes."""

from __future__ import annotations

import secrets
from datetime import UTC, datetime, timedelta
from typing import Any, Literal

from litestar import Controller, Request, Response, get, post
from litestar.di import Provide
from litestar.exceptions import NotAuthorizedException
from litestar.security.jwt import Token
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends.auth import get_current_user, jwt_auth, token_store, user_store
from app.models.models import Login, User
from app.tables.tables import Users
from app.utils.security import check_password_hash, generate_password_hash
from constants import (
    ACCESS_SECRET_KEY_LIVE,
    REFRESH_SECRET_KEY,
    REFRESH_SECRET_KEY_LIVE,
)


async def decode_token(request: Request) -> Token:
    """Decode the token."""
    token: dict = await request.json()
    if not token:
        return None
    return Token.decode(
        token.get("refresh_token").split()[1],
        REFRESH_SECRET_KEY,
        "HS256",
    )


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
                user.pswd_create = datetime.now(tz=UTC)
                user.change_pswd = False
                user.attempt = 0
                return {"message": "updated"}

            delta_change = datetime.now() - user.pswd_create
            if not user.change_pswd and delta_change.days < 365:
                user.attempt = 0
                refresh = Token(
                    exp=datetime.now(tz=UTC)
                    + timedelta(minutes=REFRESH_SECRET_KEY_LIVE),
                    jti=secrets.token_hex(10),
                    sub=str(user.id),
                    iat=datetime.now(tz=UTC),
                )
                return {
                    "message": "success",
                    "access_token": f"Bearer {
                        jwt_auth.create_token(
                            identifier=str(user.id),
                            token_unique_jwt_id=secrets.token_hex(10),
                            token_expiration=timedelta(
                                minutes=ACCESS_SECRET_KEY_LIVE,
                            ),
                        )
                    }",
                    "refresh_token": f"Bearer {
                        refresh.encode(
                            REFRESH_SECRET_KEY,
                            algorithm='HS256',
                        )
                    }",
                }
            return {"message": "denied"}

    @post("/logout", dependencies={"refresh": Provide(decode_token)})
    async def logout(self, request: Request[User, Token, Any], refresh: Token) -> dict:
        """Logout the user."""
        await token_store.set(
            "jti",
            request.auth.jti,
            expires_in=timedelta(
                minutes=ACCESS_SECRET_KEY_LIVE,
            ),
        )
        await token_store.set(
            "jti",
            refresh.jti,
            expires_in=timedelta(
                minutes=REFRESH_SECRET_KEY_LIVE,
            ),
        )

    @post("/refresh", dependencies={"refresh": Provide(decode_token)})
    async def refresh_token(self, refresh: Token) -> Response:
        """Refresh the access token."""
        if not refresh:
            raise NotAuthorizedException
        await token_store.delete_expired()
        await user_store.delete_expired()
        return jwt_auth.login(
            identifier=str(refresh.sub),
            token_unique_jwt_id=secrets.token_hex(10),
            token_expiration=timedelta(minutes=ACCESS_SECRET_KEY_LIVE),
        )

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
