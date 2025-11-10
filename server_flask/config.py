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
    """Configuration class."""

    SECRET_KEY = secrets.token_hex(16)
    ACCESS_SECRET_KEY = secrets.token_hex(16)
    REFRESH_SECRET_KEY = secrets.token_hex(16)
    ACCESS_SECRET_KEY_LIVE = 60  # minutes
    REFRESH_SECRET_KEY_LIVE = 30 * 24 * 60  # minutes
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
    BASE_PATH = Path(setting["Destination"].get("path"))
    DEFAULT_PASSWORD = setting["Password"].get("password")
    DATABASE_URI = f"sqlite:///{BASE_PATH.joinpath("database.db")}"
