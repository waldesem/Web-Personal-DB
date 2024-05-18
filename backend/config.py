import os
from datetime import timedelta

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Settings(BaseSettings):
    jwt_secret_key: str | None = os.getenv("jwt_secret_key")
    jwt_access_token_expires: timedelta = timedelta(seconds=600)
    jwt_refresh_token_expires: timedelta = timedelta(days=30)
    jwt_tokens_algorithm: str = "HS256"
    sqlalchemy_database_uri: str | None = os.getenv("sqlalchemy_database_uri")
    base_path: str = os.path.abspath(os.path.join(basedir, "..", "persons"))
    default_password: str = "8" * 8
    pagination: int = 16


settings = Settings()
