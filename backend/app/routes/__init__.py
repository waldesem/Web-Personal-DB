from apiflask import APIBlueprint

bp = APIBlueprint('route', __name__)

from app.routes import route

from app.routes import api

from app.routes import login

from app.routes import admin

