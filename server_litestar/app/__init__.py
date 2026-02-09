"""Initialize the Flask application."""

from litestar import Litestar
from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.logging import LoggingConfig

from app.controllers import base_router, index
from app.depends.auth import jwt_auth
from app.tables.tables import alchemy_plugin

cors_config = CORSConfig()
logging_config = LoggingConfig(
    disable_stack_trace={404, ValueError},
)


app = Litestar(
    on_app_init=[jwt_auth.on_app_init],
    route_handlers=[index, base_router],
    compression_config=CompressionConfig(backend="gzip", gzip_compress_level=6),
    cors_config=cors_config,
    logging_config=logging_config,
    openapi_config=None,
    plugins=[alchemy_plugin],
    debug=True,
)
