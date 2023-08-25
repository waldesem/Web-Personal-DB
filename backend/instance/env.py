import os
from datetime import timedelta

DESCRIPTION = 'StaffSec'
CONTACT = {'email': 'wsemenenko@gmail.com'}
SECRET_KEY = 'iQrmtp4hyYsHcN3EpuM-rklBZ2MPe4u13tmurHa-150'
JWT_SECRET_KEY = 'mdm_2F4rLo-60rxuxbll1ouEssk3Hgx7v0q5lUZyu_I'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://flask:flask@localhost/personal'

if os.environ.get('FLASK_ENV') == 'testing':
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.pardir, 'personal.db')

