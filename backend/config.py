import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=600)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BASE_PATH = os.path.abspath(os.path.join('..', 'persons'))

    DEFAULT_PASSWORD = '8'*8