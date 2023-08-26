import os
from datetime import timedelta

DESCRIPTION = 'StaffSec'
CONTACT = {'email': 'wsemenenko@gmail.com'}
SECRET_KEY = 'SECRET_KEY'  # Must be at least 32 characters
JWT_SECRET_KEY = 'JWT_SECRET_KEY'  # Must be at least 32 characters
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://flask:flask@localhost/personal'

if os.environ.get('FLASK_ENV') == 'testing':
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.pardir, 'personal.db')

