import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    SECRET_KEY = 'AtK5Jcsngu7ewjoHZk1tweTLl6lM83vuL3aEMcsrKLvGUccEOg'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or "postgresql://flask:flask@localhost/personal"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)
    DEBUG = False
    SECURITY_URL_PREFIX = "/admin"
    DESCRIPTION = 'Web-Personal DB API'
    CONTACT = {'email': 'wsemenenko@gmail.com'}


class DevelopmentConfig(Config):
    SECRET_KEY = 'XBSn6VoOJQaQvENTooCHkb2y2YtbI82FgybeVUGIRSkcJf0E5u'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'personal.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)
    DEBUG = True
    AUTO_200_RESPONSE = False
    TEMPLATES_AUTO_RELOAD = True
    SECURITY_URL_PREFIX = "/admin"
    DESCRIPTION = 'Web-Personal DB API Dev'
    CONTACT = {'email': 'wsemenenko@gmail.com'}
