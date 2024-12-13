"""Configuration class."""

import secrets
from configparser import ConfigParser
from pathlib import Path

BASE = Path.resolve(Path(__file__).parent)

setting = ConfigParser()
setting.read(Path(BASE, "settings.ini"), encoding="utf-8")


class Configuration:
    """Base configuration class."""

    SECRET_KEY = secrets.token_hex(16)
    JWT_SECRET_KEY = secrets.token_hex(16)
    MAX_CONTENT_LENGTH = 100 * 1000 * 1000
    BASE_PATH = setting["Destination"].get("path")
    DATABASE_URI = "sqlite:///" + str(Path(BASE_PATH, "database.db"))
    DEFAULT_PASSWORD = "88888888"  # noqa: S105


class SqliteConfig(Configuration):
    """Sqlite configuration class."""


class PostgreConfig(Configuration):
    """PostgreSQL configuration class."""

    DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        setting["PostgreSQL"]["user"],
        setting["PostgreSQL"]["password"],
        setting["PostgreSQL"]["host"],
        setting["PostgreSQL"]["port"],
        setting["PostgreSQL"]["dbname"],
    )


class Config(SqliteConfig):
    """Configuration class."""
