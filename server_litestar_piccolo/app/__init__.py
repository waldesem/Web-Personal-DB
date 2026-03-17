"""Initialize the Litestar application."""

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from litestar import Litestar
from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.logging import LoggingConfig
from litestar.middleware.logging import LoggingMiddlewareConfig
from litestar.openapi import OpenAPIConfig
from litestar.static_files import create_static_files_router
from piccolo.conf.apps import table_finder
from piccolo.engine import engine_finder
from piccolo.table import Table, create_db_tables

from app.controllers import base_router
from app.middleware.auth import jwt_access

if TYPE_CHECKING:
    from types import AsyncGeneratorType


async def init_db() -> None:
    """Init database."""
    tables = table_finder(modules=["app.tables.tables"])
    await create_db_tables(*tables, if_not_exists=True)
    await Table.raw(
        """
        ALTER TABLE persons DROP CONSTRAINT IF EXISTS person_data;
        ALTER TABLE persons
        ADD CONSTRAINT person_data
        UNIQUE (surname, firstname, patronymic, birthday)
        """,
    )

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
    disable_stack_trace={404},
    formatters={
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
)

logging_middleware_config = LoggingMiddlewareConfig()


@asynccontextmanager
async def lifespan(_: Litestar) -> AsyncGeneratorType:
    """Use a connection pool."""
    engine = engine_finder()
    assert engine
    await engine.start_connection_pool()
    yield
    await engine.close_connection_pool()


app = Litestar(
    on_app_init=[jwt_access.on_app_init],
    route_handlers=route_handlers,
    compression_config=compression_config,
    cors_config=CORSConfig(),
    lifespan=[lifespan],
    logging_config=logging_config,
    middleware=[logging_middleware_config.middleware],
    on_startup=[init_db],
    openapi_config=OpenAPIConfig(title="STAFFSEC API", version="1.0.0"),
    debug=True,
)
