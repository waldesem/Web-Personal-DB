from quart import Blueprint

bp = Blueprint('route', __name__)

from app.routes import route

from app.routes import login

from app.routes import admin

from app.routes import contact

from app.routes import message

from app.routes import classify

from app.routes import files

