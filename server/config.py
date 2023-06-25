import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'AtK5Jcsngu7ewjoHZk1tweTLl6lM83vuL3aEMcsrKLvGUccEOg'
    JWT_SECRET_KEY = '35fc4376a65fabf019998606af3a4108f08f1c3df41c7b264c'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=24)
    SECURITY_URL_PREFIX = "/admin"
    SCHEDULER_API_ENABLED: True
    DESCRIPTION = 'Web-Personal DB API'
    CONTACT = {'email': 'wsemenenko@gmail.com'}

class PostgresConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or "postgresql://flask:flask@localhost/personal"


class SqliteConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'personal.db')
    
