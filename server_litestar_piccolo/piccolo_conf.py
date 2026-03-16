"""Piccolo conf."""

import os

from dotenv import load_dotenv
from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine

load_dotenv()

DB = PostgresEngine(
    config={
        "host": os.getenv("PG_HOST"),
        "port": os.getenv("PG_PORT"),
        "database": os.getenv("PG_DATABASE"),
        "user": os.getenv("PG_USER"),
        "password": os.getenv("PG_PASSWORD"),
    },
)

APP_REGISTRY = AppRegistry(
    apps=[
        "app.piccolo_app",
        "piccolo_admin.piccolo_app",
    ],
)
