import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:

    DESCRIPTION = 'EconSec'

    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 90

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BASE_PATH = os.path.abspath(os.path.join('..', 'persons'))

    DEFAULT_PASSWORD = '8'*8
