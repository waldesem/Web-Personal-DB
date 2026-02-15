"""Auth module."""

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from litestar.exceptions import NotAuthorizedException
from litestar.security.jwt import JWTAuth, Token
from litestar.stores.memory import MemoryStore

from app.models.models import User
from app.tables.tables import Users, config
from constants import ACCESS_SECRET_KEY

if TYPE_CHECKING:
    from litestar.connection import ASGIConnection
    from litestar.handlers import BaseRouteHandler
    from sqlalchemy.ext.asyncio import AsyncSession

token_store = MemoryStore()


def role_guard(
    connection: ASGIConnection[Any, Any, Any, Any],
    route_handler: BaseRouteHandler,
) -> None:
    """Check if the user has the required role."""
    if connection.user.role != route_handler.opt.get("roles"):
        raise NotAuthorizedException


async def get_current_user(user_id: int, session: AsyncSession) -> User | None:
    """Retrieve the current user."""
    if (
        (user := await session.get(Users, user_id))
        and not user.blocked
        and not user.deleted
        and not user.change_pswd
        and user.pswd_create + timedelta(days=365) > datetime.now(tz=UTC)
    ):
        return User.model_validate(user)
    return None


async def retrieve_user_handler(
    token: Token,
    _: ASGIConnection[Any, Any, Any, Any],
) -> User | None:
    """Retrieve the current user."""
    async with config.get_session() as db_session:
        current_user = await get_current_user(int(token.sub), db_session)
        if current_user:
            return current_user
        return None


async def revoked_token_handler(
    token: Token,
    _: ASGIConnection[Any, Any, Any, Any],
) -> bool:
    """Check if the token is revoked."""
    if jti := token.jti:
        # Check if the token is already revoked in the BLOCKLIST
        revoked = await token_store.get(jti)
        if revoked:
            return True
    return False


jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    revoked_token_handler=revoked_token_handler,
    token_secret=ACCESS_SECRET_KEY,
    exclude=[
        "/assets/*",
        "/routes/auth/login",
        "/routes/auth/update",
        "/routes/auth/refresh",
    ],
)
