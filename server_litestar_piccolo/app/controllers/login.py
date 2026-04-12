"""Login routes."""

from __future__ import annotations

import secrets
from datetime import UTC, datetime
from typing import Any

import bcrypt
from litestar import Controller, Request, Response, get, patch, post
from litestar.exceptions import NotAuthorizedException
from litestar.security.jwt import Token

from app.middleware.auth import jwt_access, jwt_refresh, jwt_revoke
from app.models.user import AuthLogin, AuthResponse, Session, UpdateLogin, User
from app.tables.tables import Users


def key_builder(request: Request) -> str:
    """Specify a cache key builder."""
    return request.headers.get("Authorization", "").split(".")[-1]


class AuthController(Controller):
    """Auth controller."""

    path = "/auth"

    @classmethod
    async def check_user(
        cls,
        data: AuthLogin | UpdateLogin,
    ) -> Users | None:
        """Check user.

        Args:
            db_session: AsyncSession.
            data: AuthLogin | UpdateLogin.

        Returns:
            Users | None.

        """
        user = await Users.objects().get(Users.username == data.username)

        if not user or user.blocked or user.deleted:
            return None

        if not bcrypt.checkpw(data.password.encode(), user.passhash):
            if user.attempt < 5:
                user.attempt += 1
            else:
                user.blocked = True
            await user.save()
            return None

        return user

    @post("/login")
    async def post_login(
        self,
        data: AuthLogin,
    ) -> AuthResponse:
        """Handle the login process.

        Args:
            data: AuthLogin.
            db_session: AsyncSession.

        Returns:
            Response with status code 200 and AuthResponse.

        """
        if user := await self.check_user(data):
            delta_change = datetime.now(UTC) - user.pswd_create

            if user.change_pswd or delta_change.days > 365:
                return AuthResponse(message="denied")

            if user.attempt > 0:
                user.attempt = 0
                await user.save()
            return AuthResponse(
                message="success",
                access_token=f"Bearer {
                    jwt_access.create_token(
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

    @patch("/login")
    async def patch_login(
        self,
        data: UpdateLogin,
    ) -> None:
        """Proceed login process.

        Args:
            data: UpdateLogin.

        Returns:
            Response with status code 200 and AuthResponse.

        """
        if user := await self.check_user(data):
            user.passhash = bcrypt.hashpw(
                data.new_pswd.encode(),
                bcrypt.gensalt(),
            )
            user.pswd_create = datetime.now(tz=UTC)
            user.change_pswd = False
            user.attempt = 0
            await user.save()
        else:
            raise NotAuthorizedException

    @patch("/logout")
    async def logout(self, data: AuthResponse) -> None:
        """Logout the user.

        Args:
            data: AuthResponse.

        Returns:
            Response with status code 200.

        """
        if data.access_token:
            await jwt_revoke(data.access_token)
        if data.refresh_token:
            await jwt_revoke(data.refresh_token, access=False)

    @get("/refresh", middleware=[jwt_refresh.middleware])
    async def refresh_token(self, request: Request[User, Token, Any]) -> Response:
        """Refresh the access token.

        Args:
            request: Request.

        Returns:
            Response with status code 201 and access token.

        """
        return jwt_access.login(
            identifier=str(request.auth.sub),
            token_unique_jwt_id=secrets.token_hex(10),
            send_token_as_response_body=True,
        )

    @get("/session", cache=120, cache_key_builder=key_builder)
    async def get_session(self, request: Request[User, Token, Any]) -> Session:
        """Retrieve user session data.

        Args:
            request: Request.

        Returns:
            Session.

        """
        return Session(
            id=request.user.id,
            fullname=request.user.fullname,
            username=request.user.username,
            email=request.user.email,
            role=request.user.role,
        )
