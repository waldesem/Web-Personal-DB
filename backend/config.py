import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=600)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    jwt_tokens_algorithm = "HS256"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(os.path.join("..", 'candidates.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_PATH = os.path.abspath(os.path.join("..", "persons"))
    DEFAULT_PASSWORD = "8" * 8
    PAGINATION = 16
