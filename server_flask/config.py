"""Configuration class."""

import configparser
import secrets
from pathlib import Path

from flask import current_app

setting = configparser.ConfigParser()
# reading settings from settings.ini in the current directory
try:
    setting.read(
        Path(Path.resolve(Path(__file__).parent), "settings.ini"),
        encoding="utf-8",
    )
except configparser.Error:
    current_app.logger.exception()


class Config:
    """Base configuration class."""

    SECRET_KEY = secrets.token_hex(16)
    JWT_SECRET_KEY = secrets.token_hex(16)
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
    BASE_PATH = setting["Destination"].get("path")
    DATABASE_URI = "sqlite:///" + str(Path(BASE_PATH, "database.db"))
    DEFAULT_PASSWORD = "88888888"  # noqa: S105
