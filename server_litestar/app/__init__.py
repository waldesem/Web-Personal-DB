"""Initialize the Litestar application."""

from litestar import Litestar
from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.logging import LoggingConfig
from litestar.openapi import OpenAPIConfig
from litestar.static_files import create_static_files_router

from app.controllers import base_router
from app.depends.auth import jwt_auth
from app.tables.tables import alchemy_plugin

route_handlers = [
    base_router,
    create_static_files_router(
        path="/",
        directories=["app/static"],
        html_mode=True,
        opt={"exclude_from_auth": "exclude_opt_key"},
    ),
]

compression_config = CompressionConfig(
    backend="gzip",
    minimum_size=1000,
    gzip_compress_level=6,
)

logging_config = LoggingConfig(
    disable_stack_trace={404, ValueError},
    formatters={
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    log_exceptions="always",
    root={"level": "INFO", "handlers": ["queue_listener"]},
)

app = Litestar(
    on_app_init=[jwt_auth.on_app_init],
    route_handlers=route_handlers,
    compression_config=compression_config,
    cors_config=CORSConfig(),
    logging_config=logging_config,
    openapi_config=OpenAPIConfig(title="STAFFSEC API", version="1.0.0"),
    plugins=[alchemy_plugin],
)
