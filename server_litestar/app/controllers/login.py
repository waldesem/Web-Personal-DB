"""Login routes."""

from __future__ import annotations

import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

from litestar import Controller, Request, Response, get, post
from litestar.di import Provide
from litestar.exceptions import NotAuthorizedException
from litestar.security.jwt import Token
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends.auth import get_current_user, jwt_auth, token_store
from app.models.models import AuthLogin, AuthResponse, UpdateLogin, User
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
        raise NotAuthorizedException
    return Token.decode(
        token.get("refresh_token").split()[1],
        REFRESH_SECRET_KEY,
        "HS256",
    )


class AuthController(Controller):
    """Auth controller."""

    path = "/auth"

    @staticmethod
    async def check_user(
        db_session: AsyncSession,
        data: AuthLogin | UpdateLogin,
    ) -> Users | None:
        """Check user."""
        user = (
            await db_session.execute(
                select(Users).filter_by(username=data.username),
            )
        ).scalar_one_or_none()

        if not user or user.blocked or user.deleted:
            return None

        if not check_password_hash(user.passhash, data.password):
            if user.attempt < 5:
                user.attempt += 1
            else:
                user.blocked = True
            return None

        return user

    @post("/login")
    async def post_login_auth(
        self,
        data: AuthLogin,
        db_session: AsyncSession,
    ) -> AuthResponse:
        """Handle the login process."""
        if user := await self.check_user(db_session, data):
            delta_change = datetime.now(UTC) - user.pswd_create

            if user.change_pswd or delta_change.days > 365:
                return AuthResponse(message="denied")

            user.attempt = 0
            refresh = Token(
                exp=datetime.now(tz=UTC) + timedelta(minutes=REFRESH_SECRET_KEY_LIVE),
                jti=secrets.token_hex(10),
                sub=str(user.id),
                iat=datetime.now(tz=UTC),
            )
            return AuthResponse(
                message="success",
                access_token=f"Bearer {
                    jwt_auth.create_token(
                        identifier=str(user.id),
                        token_unique_jwt_id=secrets.token_hex(10),
                        token_expiration=timedelta(
                            minutes=ACCESS_SECRET_KEY_LIVE,
                        ),
                    )
                }",
                refresh_token=f"Bearer {
                    refresh.encode(
                        REFRESH_SECRET_KEY,
                        algorithm='HS256',
                    )
                }",
            )
        raise NotAuthorizedException

    @post("/update")
    async def post_login(
        self,
        data: UpdateLogin,
        db_session: AsyncSession,
    ) -> AuthResponse:
        """Handle the login process."""
        if user := await self.check_user(db_session, data):
            user.passhash = generate_password_hash(data.new_pswd)
            user.pswd_create = datetime.now(tz=UTC)
            user.change_pswd = False
            user.attempt = 0
            return AuthResponse(message="updated")
        raise NotAuthorizedException

    @post("/logout", dependencies={"refresh": Provide(decode_token)})
    async def logout(self, request: Request[User, Token, Any], refresh: Token) -> None:
        """Logout the user."""
        if isinstance(request.auth.jti, str):
            await token_store.set(
                "jti",
                request.auth.jti,
                expires_in=timedelta(
                    minutes=ACCESS_SECRET_KEY_LIVE,
                ),
            )
        if isinstance(refresh.jti, str):
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
    ) -> User:
        """Retrieve an item from the database based on the provided item ID."""
        if not request.user or not isinstance(request.user.id, int):
            raise NotAuthorizedException
        if current_user := await get_current_user(request.user.id, db_session):
            return current_user
        raise NotAuthorizedException
