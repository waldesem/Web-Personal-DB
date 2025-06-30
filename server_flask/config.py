"""Configuration class."""

import secrets
from configparser import ConfigParser
from pathlib import Path

setting = ConfigParser()
# reading settings from settings.ini in the current directory
setting.read(
    Path(Path.resolve(Path(__file__).parent), "settings.ini"),
    encoding="utf-8",
)


class Config:
    """Base configuration class."""

    SECRET_KEY = secrets.token_hex(16)
    JWT_SECRET_KEY = secrets.token_hex(16)
    JWT_SECRET_KEY_LIVE = 365
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
    BASE_PATH = setting["Destination"].get("path")
    DATABASE_URI = "sqlite:///" + str(Path(BASE_PATH, "database.db"))
    DEFAULT_PASSWORD = setting["Password"].get("password")
    PAGINATION = 10
