import os
import datetime

DESCRIPTION = 'Web-Personal DB API'
CONTACT = {'email': 'wsemenenko@gmail.com'}
SECRET_KEY = 'AtK5Jcsngu7ewjoHZk1tweTLl6lM83vuL3aEMcsrKLvGUccEOg'
JWT_SECRET_KEY = '35fc4376a65fabf019998606af3a4108f08f1c3df41c7b264c'
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=24)
SQLALCHEMY_TRACK_MODIFICATIONS = False
TEMPLATES_AUTO_RELOAD = True
SCHEDULER_API_ENABLED = True
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://username:password@localhost/personal'

if os.environ.get('FLASK_ENV') == 'testing':
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.pardir, 'personal.db')
