import os
from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict

basedir = os.path.abspath(os.path.dirname(__file__))


class Settings(BaseSettings):
    jwt_secret_key: str | None
    jwt_access_token_expires: timedelta = timedelta(seconds=600)
    jwt_refresh_token_expires: timedelta = timedelta(days=30)
    jwt_tokens_algorithm: str = "HS256"
    sqlalchemy_database_uri: str | None
    base_path: str = os.path.abspath(os.path.join(basedir, "..", "persons"))
    default_password: str = "8" * 8
    pagination: int = 16

    model_config = SettingsConfigDict(env_file = os.path.join(basedir, ".env"))

settings = Settings()
