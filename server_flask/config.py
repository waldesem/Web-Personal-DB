"""Configuration class."""

import os
import secrets


class Config:
    """Configuration class."""

    SECRET_KEY = secrets.token_hex(16)
    ACCESS_SECRET_KEY = secrets.token_hex(16)
    REFRESH_SECRET_KEY = secrets.token_hex(16)
    ACCESS_SECRET_KEY_LIVE = 60  # minutes
    REFRESH_SECRET_KEY_LIVE = 30 * 24 * 60  # minutes
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
    BASE_PATH = os.getenv("BASE_PATH")
    DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD")
    DATABASE_URI = os.getenv("DATABASE_URI")
