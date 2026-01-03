"""Auth module."""

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from litestar.exceptions import NotAuthorizedException
from litestar.security.jwt import JWTAuth, Token

from app.models.models import User
from app.tables.tables import Users, config
from config import Config

if TYPE_CHECKING:
    from litestar.connection import ASGIConnection
    from litestar.handlers import BaseRouteHandler
    from sqlalchemy.ext.asyncio import AsyncSession


def role_guard(connection: ASGIConnection, route_handler: BaseRouteHandler) -> None:
    """Check if the user has the required role."""
    if connection.user.role not in route_handler.opt.get("roles"):
        raise NotAuthorizedException


async def get_current_user(user_id: int, session: AsyncSession) -> User | None:
    """Retrieve the current user stored in the global variable."""
    async with session.begin():
        if (
            (user := await session.get(Users, user_id))
            and not user.blocked
            and not user.deleted
            and not user.change_pswd
            and user.pswd_create + timedelta(days=365) > datetime.now()
        ):
            return User.model_validate(user)
        return None


async def retrieve_user_handler(
    token: Token,
    _: ASGIConnection[Any, Any, Any, Any],
) -> User | None:
    """Retrieve the current user."""
    session_maker = config.create_session_maker()
    async with session_maker() as db_session:
        return await get_current_user(token.sub, db_session)


jwt_auth = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=Config.ACCESS_SECRET_KEY,
    exclude=[
        "/routes/auth/login",
        "/routes/auth/update",
        "/routes/refresh",
        "/routes/schema",
    ],
)
