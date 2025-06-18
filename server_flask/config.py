"""Configuration class."""

import logging
import secrets
from configparser import ConfigParser
from pathlib import Path

setting = ConfigParser()
# reading settings from settings.ini in the current directory
setting.read(
    Path(Path.resolve(Path(__file__).parent), "settings.ini"),
    encoding="utf-8",
)

handler = logging.FileHandler("error.log", mode="w", encoding="utf-8")
handler.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)


class Config:
    """Base configuration class."""

    SECRET_KEY = secrets.token_hex(16)
    JWT_SECRET_KEY = secrets.token_hex(16)
    JWT_SECRET_KEY_LIVE = 365
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
    BASE_PATH = setting["Destination"].get("path")
    DATABASE_URI = "sqlite:///" + str(Path(BASE_PATH, "database.db"))
    DEFAULT_PASSWORD = setting["Password"].get("password")

