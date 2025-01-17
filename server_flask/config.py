"""Configuration class."""

import secrets
from configparser import ConfigParser
from pathlib import Path

BASE = Path.resolve(Path(__file__).parent)

setting = ConfigParser()
setting.read(Path(BASE, "settings.ini"), encoding="utf-8")


class Config:
    """Base configuration class."""

    SECRET_KEY = secrets.token_hex(16)
    JWT_SECRET_KEY = secrets.token_hex(16)
    MAX_CONTENT_LENGTH = 100 * 1000 * 1000
    BASE_PATH = setting["Destination"].get("path")
    DATABASE_URI = "sqlite:///" + str(Path(BASE_PATH, "database.db"))
    DEFAULT_PASSWORD = "88888888"  # noqa: S105
