import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'personal.db')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or "postgresql://postgres:Truxanova@localhost/personal"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
