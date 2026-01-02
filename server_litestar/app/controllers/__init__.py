"""Routes."""

from litestar import Router

from .index import get_index, post_json_file, switch_status
from .items import ItemsController
from .login import AuthController
from .person import PersonController
from .user import UserController

base_router = Router(
    path="/routes",
    route_handlers=[
        get_index,
        switch_status,
        post_json_file,
        AuthController,
        PersonController,
        ItemsController,
        UserController,
    ],
)
