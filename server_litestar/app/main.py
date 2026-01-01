"""Initialize the Flask application."""

from __future__ import annotations

from litestar import Litestar, MediaType, Request, Response, get
from litestar.exceptions import HTTPException
from litestar.logging import LoggingConfig
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR

from app.depends.auth import jwt_auth
from app.routes import base_router

logging_config = LoggingConfig(
    disable_stack_trace={404, ValueError},
)


def plain_text_exception_handler(_: Request, exc: Exception) -> Response:
    """Handle exceptions subclassed from HTTPException."""
    status_code = getattr(exc, "status_code", HTTP_500_INTERNAL_SERVER_ERROR)
    detail = getattr(exc, "detail", "")

    return Response(
        media_type=MediaType.TEXT,
        content=detail,
        status_code=status_code,
    )


@get("/")
async def index() -> None:
    """Index page."""
    raise HTTPException(detail="an error occurred", status_code=400)


app = Litestar(
    route_handlers=[index, base_router],
    on_app_init=[jwt_auth.on_app_init],
    exception_handlers={HTTPException: plain_text_exception_handler},
    logging_config=logging_config,
    openapi_config=None,
    debug=True,
)
