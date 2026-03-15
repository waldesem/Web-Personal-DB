"""Routes."""

from litestar import Router

from .index import get_candidates
from .items import ItemsController
from .login import AuthController
from .person import PersonController
from .uploads import JsonController
from .user import UserController

base_router = Router(
    path="/routes",
    route_handlers=[
        get_candidates,
        AuthController,
        PersonController,
        ItemsController,
        JsonController,
        UserController,
    ],
)
