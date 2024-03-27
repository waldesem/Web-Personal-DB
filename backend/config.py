import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=600)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 600
    CACHE_KEY_PREFIX = "staffsec_"
    CACHE_REDIS_HOST = "localhost" 
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0

    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_REDIS_HOST = "localhost" 
    JWT_REDIS_PORT = 6379
    JWT_REDIS_DB = 1

    BASE_PATH = os.path.abspath(os.path.join("..", "persons"))
    NO_PHOTO = os.path.join(BASE_PATH, 'no-photo.png')

    DEFAULT_PASSWORD = "8" * 8

    PAGINATION = 16
