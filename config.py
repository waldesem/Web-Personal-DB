import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    SECRET_KEY = 'my_super_secret_prod_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or "postgresql://flask:flask@localhost/personal"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)
    AUTO_200_RESPONSE = False
    DESCRIPTION = 'Web-Personal DB API'
    CONTACT = {'email': 'wsemenenko@gmail.com'}


class DevelopmentConfig(Config):
    SECRET_KEY = 'my_super_secret_dev_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'tmp', 'personal.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)
    AUTO_200_RESPONSE = False
    TEMPLATES_AUTO_RELOAD = True
    DESCRIPTION = 'Web-Personal DB API Dev'
    CONTACT = {'email': 'wsemenenko@gmail.com'}
