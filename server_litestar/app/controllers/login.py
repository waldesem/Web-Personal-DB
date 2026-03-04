"""Login routes."""

from __future__ import annotations

import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

from litestar import Controller, Request, Response, get, post
from litestar.exceptions import NotAuthorizedException
from litestar.security.jwt import Token
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.middleware.auth import jwt_auth, jwt_refresh, token_store
from app.structures.models import AuthLogin, AuthResponse, Session, UpdateLogin, User
from app.structures.tables import Users
from app.utils.security import check_password_hash, generate_password_hash
from constants import (
    ACCESS_SECRET_KEY,
    ACCESS_SECRET_KEY_LIVE,
    REFRESH_SECRET_KEY,
    REFRESH_SECRET_KEY_LIVE,
)


def key_builder(request: Request) -> str:
    """Specify a cache key builder."""
    return request.headers.get("Authorization", "").split(".")[-1]


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
            await db_session.commit()
            return None

        return user

    @staticmethod
    async def add_expiry(token: str | None, *, access: bool = True) -> None:
        """Add token to expires store."""
        await token_store.delete_expired()
        if token:
            decoded = Token.decode(
                token.split()[1],
                ACCESS_SECRET_KEY if access else REFRESH_SECRET_KEY,
                "HS256",
                verify_exp=False,
            )
            await token_store.set(
                str(decoded.jti),
                b"jti",
                timedelta(
                    minutes=ACCESS_SECRET_KEY_LIVE
                    if access
                    else REFRESH_SECRET_KEY_LIVE,
                ),
            )

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
            return AuthResponse(
                message="success",
                access_token=f"Bearer {
                    jwt_auth.create_token(
                        identifier=str(user.id),
                        token_unique_jwt_id=secrets.token_hex(10),
                    )
                }",
                refresh_token=f"Bearer {
                    jwt_refresh.create_token(
                        identifier=str(user.id),
                        token_unique_jwt_id=secrets.token_hex(10),
                    )
                }",
            )
        raise NotAuthorizedException

    @post("/update")
    async def post_login_update(
        self,
        data: UpdateLogin,
        db_session: AsyncSession,
    ) -> AuthResponse:
        """Proceed login process."""
        if user := await self.check_user(db_session, data):
            user.passhash = generate_password_hash(data.new_pswd)
            user.pswd_create = datetime.now(tz=UTC)
            user.change_pswd = False
            user.attempt = 0
            return AuthResponse(message="updated")
        raise NotAuthorizedException

    @post("/logout")
    async def logout(self, data: AuthResponse) -> None:
        """Logout the user."""
        await self.add_expiry(data.access_token)
        await self.add_expiry(data.refresh_token, access=False)

    @get("/refresh", middleware=[jwt_refresh.middleware])
    async def refresh_token(self, request: Request[User, Token, Any]) -> Response:
        """Refresh the access token."""
        return jwt_auth.login(
            identifier=str(request.auth.sub),
            token_unique_jwt_id=secrets.token_hex(10),
            send_token_as_response_body=True,
        )

    @get("/session", cache=120, cache_key_builder=key_builder)
    async def get_session(self, request: Request[User, Token, Any]) -> Session:
        """Retrieve user data."""
        return Session(**request.user.model_dump())
