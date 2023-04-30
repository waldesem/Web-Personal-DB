import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    SECRET_KEY = 'my_super_secret_prod_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or "postgresql://postgres:password@localhost/personal"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)
    BOOTSTRAP_BOOTSWATCH_THEME = 'journal'
    AUTO_200_RESPONSE = False
    JSON_SORT_KEYS = False
    WTF_CSRF_ENABLED = False
    DESCRIPTION = 'Web-Personal DB API'
    CONTACT = {'email': 'wsemenenko@gmail.com'}
    LICENSE = [
        {
            'name': 'MIT',
            'url': 'https://opensource.org/licenses/MIT'
        }
    ]
    SERVERS = [
        {
            'name': 'Production Server',
            'url': 'http://api.example.com'
        },
    ]


class DevelopmentConfig(Config):
    SECRET_KEY = 'my_super_secret_dev_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'personal.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)
    BOOTSTRAP_BOOTSWATCH_THEME = 'journal'
    AUTO_200_RESPONSE = False
    TEMPLATES_AUTO_RELOAD = True
    JSON_SORT_KEYS = False
    WTF_CSRF_ENABLED = False
    DESCRIPTION = 'Web-Personal DB API Dev'
    CONTACT = {'email': 'wsemenenko@gmail.com'}
    LICENSE = {
        'name': 'MIT',
        'url': 'https://opensource.org/licenses/MIT'
    }
    SERVERS = [
        {
            'name': 'Development Server',
            'url': 'http://localhost:5000'
        }
    ]
