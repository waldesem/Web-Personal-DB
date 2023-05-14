import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    SECRET_KEY = 'my_super_secret_prod_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or "postgresql://username:password@localhost/candidates"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)
    BOOTSTRAP_BOOTSWATCH_THEME = 'journal'
    AUTO_200_RESPONSE = False
    WTF_CSRF_ENABLED = False
    DESCRIPTION = 'Web-Personal DB API'
    CONTACT = {'email': 'wsemenenko@gmail.com'}


class DevelopmentConfig(Config):
    SECRET_KEY = 'my_super_secret_dev_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'personal.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)
    BOOTSTRAP_BOOTSWATCH_THEME = 'journal'
    AUTO_200_RESPONSE = False
    TEMPLATES_AUTO_RELOAD = True
    WTF_CSRF_ENABLED = False
    DESCRIPTION = 'Web-Personal DB API Dev'
    CONTACT = {'email': 'wsemenenko@gmail.com'}
