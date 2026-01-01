from datetime import datetime, timedelta
from functools import lru_cache

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers import BaseRouteHandler
from litestar.security.jwt import JWTAuth, Token

from app.classes.classes import Roles
from app.models.models import User
from app.tables.tables import Users, session
from config import Config


def role_guard(connection: ASGIConnection, _: BaseRouteHandler, role: Roles) -> None:
    if not connection.user.has_role(role):
        raise NotAuthorizedException()


@lru_cache(maxsize=2)
def get_current_user(user_id: int) -> User | None:
    """Retrieve the current user stored in the global variable."""
    if (
        (user := session.get(Users, user_id))
        and not user.blocked
        and not user.deleted
        and not user.change_pswd
        and user.pswd_create + timedelta(days=365) > datetime.now()
    ):
        return User.model_validate(user)
    return None


async def retrieve_user_handler(token: Token) -> User | None:
    # logic here to retrieve the user instance
    return get_current_user(token.sub)


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
