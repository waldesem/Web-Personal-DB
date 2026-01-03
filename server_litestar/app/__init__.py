"""Initialize the Flask application."""

from __future__ import annotations

from litestar import Litestar, get
from litestar.exceptions import HTTPException
from litestar.logging import LoggingConfig

from app.controllers import base_router
from app.depends.auth import jwt_auth
from app.tables.tables import plugin

logging_config = LoggingConfig(
    disable_stack_trace={404, ValueError},
)


@get("/")
async def index() -> None:
    """Index page."""
    raise HTTPException(detail="an error occurred", status_code=400)


app = Litestar(
    route_handlers=[index, base_router],
    on_app_init=[jwt_auth.on_app_init],
    plugins=[plugin],
    logging_config=logging_config,
    openapi_config=None,
)
