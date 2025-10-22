"""Configuration class."""

import secrets
from configparser import ConfigParser
from pathlib import Path

setting = ConfigParser()
setting.read(
    Path(Path.resolve(Path(__file__).parent), "settings.ini"),
    encoding="utf-8",
)


class Config:
    """Base configuration class."""

    SECRET_KEY = secrets.token_hex(16)
    ACCESS_SECRET_KEY = secrets.token_hex(16)
    REFRESH_SECRET_KEY = secrets.token_hex(16)
    ACCESS_SECRET_KEY_LIVE = 60  # minutes
    REFRESH_SECRET_KEY_LIVE = 30 * 24 * 60  # minutes
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
    BASE_PATH = setting["Destination"].get("path")
    DEFAULT_PASSWORD = (
        setting["Password"].get("password")
        if setting["Password"].get("password")
        else "88888888"
    )
    DATABASE_URI = "sqlite:///" + str(Path(BASE_PATH, "database.db"))
