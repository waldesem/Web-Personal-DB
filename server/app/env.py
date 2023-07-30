import os
from datetime import timedelta
import secrets

DESCRIPTION = 'StaffSec DB API'
CONTACT = {'email': 'wsemenenko@gmail.com'}
SECRET_KEY = secrets.token_urlsafe(32)
JWT_SECRET_KEY = secrets.token_urlsafe(32)
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SCHEDULER_API_ENABLED = True
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://username:password@localhost/personal'

if os.environ.get('FLASK_ENV') == 'testing':
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.pardir, 'personal.db')
    SECRET_KEY = 'SECRET_KEY'
    JWT_SECRET_KEY = 'JWT_SECRET_KEY'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)

