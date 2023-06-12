import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    SECRET_KEY = 'AtK5Jcsngu7ewjoHZk1tweTLl6lM83vuL3aEMcsrKLvGUccEOg'
    JWT_SECRET_KEY = '35fc4376a65fabf019998606af3a4108f08f1c3df41c7b264c'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or "postgresql://flask:flask@localhost/personal"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
    DEBUG = False
    SECURITY_URL_PREFIX = "/admin"
    DESCRIPTION = 'Web-Personal DB API'
    CONTACT = {'email': 'wsemenenko@gmail.com'}


class DevelopmentConfig(Config):
    SECRET_KEY = 'XBSn6VoOJQaQvENTooCHkb2y2YtbI82FgybeVUGIRSkcJf0E5u'
    JWT_SECRET_KEY = '4773f14a625a6368f533e1e23f70c934fa914ff939510381d7'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'personal.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
    SECURITY_URL_PREFIX = "/admin"
    DESCRIPTION = 'Web-Personal DB API Dev'
    CONTACT = {'email': 'wsemenenko@gmail.com'}
