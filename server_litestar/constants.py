"""Configuration class."""

import os
import secrets

from dotenv import load_dotenv

load_dotenv()


ACCESS_SECRET_KEY = secrets.token_hex(16)
REFRESH_SECRET_KEY = secrets.token_hex(16)
ACCESS_SECRET_KEY_LIVE = 60  # minutes
REFRESH_SECRET_KEY_LIVE = 30 * 24 * 60  # minutes
BASE_PATH = os.getenv("BASE_PATH")
DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD")
DATABASE_URI = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    os.getenv("DBUSER"),
    os.getenv("PASSWORD"),
    os.getenv("HOST"),
    os.getenv("PORT"),
    os.getenv("DATABASE"),
)
