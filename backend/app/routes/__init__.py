from apiflask import APIBlueprint

bp = APIBlueprint('route', __name__)

from app.routes import route

from app.routes import api

from app.routes import login

from app.routes import admin

from app.routes import error

from app.routes import contact

from app.routes import message

from app.routes import classify

