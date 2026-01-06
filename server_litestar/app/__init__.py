"""Initialize the Flask application."""

from __future__ import annotations

from litestar import Litestar, get
from litestar.exceptions import HTTPException
from litestar.logging import LoggingConfig

from app.controllers import base_router
from app.depends.auth import jwt_auth
from app.tables.tables import alchemy_plugin

logging_config = LoggingConfig(
    disable_stack_trace={404, ValueError},
)


@get("/")
async def index() -> None:
    """Index page."""
    raise HTTPException(detail="an error occurred", status_code=400)


app = Litestar(
    on_app_init=[jwt_auth.on_app_init],
    route_handlers=[index, base_router],
    logging_config=logging_config,
    plugins=[alchemy_plugin],
    openapi_config=None,
    debug=True,
)
