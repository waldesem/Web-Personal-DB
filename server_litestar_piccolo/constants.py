"""Configuration constants."""

import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


ACCESS_SECRET_KEY = secrets.token_hex(16)
REFRESH_SECRET_KEY = secrets.token_hex(16)
ACCESS_SECRET_KEY_LIVE = 60  # minutes
REFRESH_SECRET_KEY_LIVE = 30 * 24 * 60  # minutes
BASE_PATH = os.getenv("BASE_PATH") or Path(__file__).parent.joinpath("Personals")
DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD") or "88888888"
