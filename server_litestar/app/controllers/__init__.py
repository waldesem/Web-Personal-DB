"""Routes."""

from litestar import Router

from .index import get_candidates, switch_status
from .items import ItemsController
from .login import AuthController
from .person import PersonController
from .user import UserController

base_router = Router(
    path="/routes",
    route_handlers=[
        get_candidates,
        switch_status,
        AuthController,
        PersonController,
        ItemsController,
        UserController,
    ],
)
