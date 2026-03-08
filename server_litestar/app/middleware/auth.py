"""Auth module."""

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from litestar.exceptions import NotAuthorizedException
from litestar.security.jwt import JWTAuth, Token
from litestar.stores.memory import MemoryStore

from app.models.auth import User
from app.tables.tables import Users, config
from constants import (
    ACCESS_SECRET_KEY,
    ACCESS_SECRET_KEY_LIVE,
    REFRESH_SECRET_KEY,
    REFRESH_SECRET_KEY_LIVE,
)

if TYPE_CHECKING:
    from litestar.connection import ASGIConnection
    from litestar.handlers import BaseRouteHandler

token_store = MemoryStore()


def role_guard(
    connection: ASGIConnection[Any, Any, Any, Any],
    route_handler: BaseRouteHandler,
) -> None:
    """Check if the user has the required role."""
    if connection.user.role != route_handler.opt.get("role"):
        raise NotAuthorizedException


async def retrieve_user_handler(
    token: Token,
    _: ASGIConnection[Any, Any, Any, Any],
) -> User | None:
    """Retrieve the current user."""
    async with config.get_session() as db_session:
        if (
            (user := await db_session.get(Users, int(token.sub)))
            and not user.blocked
            and not user.deleted
            and not user.change_pswd
            and user.pswd_create + timedelta(days=365) > datetime.now(tz=UTC)
        ):
            return User.model_validate(user, from_attributes=True)
        return None


async def revoked_token_handler(
    token: Token,
    _: ASGIConnection[Any, Any, Any, Any],
) -> bool:
    """Check if the token is revoked."""
    if jti := token.jti:
        # Check if the token is already revoked in the BLOCKLIST
        revoked = await token_store.get(jti)
        return bool(revoked)
    return True


jwt_access = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    revoked_token_handler=revoked_token_handler,
    token_secret=ACCESS_SECRET_KEY,
    default_token_expiration=timedelta(minutes=ACCESS_SECRET_KEY_LIVE),
    require_claims=["sub", "jti", "exp"],
    exclude=[
        "/assets/*",
        "/routes/auth/login",
        "/routes/auth/update",
        "/routes/auth/refresh",
        "/schema/swagger",
    ],
)

jwt_refresh = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    revoked_token_handler=revoked_token_handler,
    token_secret=REFRESH_SECRET_KEY,
    default_token_expiration=timedelta(minutes=REFRESH_SECRET_KEY_LIVE),
    require_claims=["sub", "jti", "exp"],
)
