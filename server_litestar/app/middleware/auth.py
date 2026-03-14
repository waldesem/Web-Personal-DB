"""Auth module."""

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from litestar.exceptions import NotAuthorizedException, NotFoundException
from litestar.security.jwt import JWTAuth, Token
from litestar.stores.memory import MemoryStore

from app.models.user import User
from app.tables.tables import Persons, Users, config
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


async def person_guard(
    connection: ASGIConnection[Any, User, Token, Any],
    _: BaseRouteHandler,
) -> None:
    """Check assotiation user ID with person's user_id."""
    async with config.get_session() as db_session:
        person_id = connection.path_params.get("person_id")
        if (
            not (person := await db_session.get(Persons, person_id))
            or not person.editable
            or person.protected
            or person.deleted
            or connection.auth.sub != str(person.user_id)
        ):
            raise NotFoundException


def role_guard(
    connection: ASGIConnection[Any, User, Token, Any],
    route_handler: BaseRouteHandler,
) -> None:
    """Check if the user has the required role."""
    if (roles := route_handler.opt.get("role")) and connection.user.role not in roles:
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
    if jti := str(token.jti):
        # Check if the token is already revoked in the BLOCKLIST
        revoked = await token_store.get(jti)
        return bool(revoked)
    return True


async def jwt_revoke(token: str | None, *, access: bool = True) -> None:
    """Add token to expires store.

    Args:
        token: str | None.
        access: bool = True.

    Returns:
        None.

    """
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
                minutes=ACCESS_SECRET_KEY_LIVE if access else REFRESH_SECRET_KEY_LIVE,
            ),
        )


jwt_access = JWTAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    revoked_token_handler=revoked_token_handler,
    token_secret=ACCESS_SECRET_KEY,
    default_token_expiration=timedelta(minutes=ACCESS_SECRET_KEY_LIVE),
    require_claims=["sub", "jti", "exp"],
    exclude=[
        "/assets/*",
        "/routes/auth/login",
        "/routes/auth/logout",
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
