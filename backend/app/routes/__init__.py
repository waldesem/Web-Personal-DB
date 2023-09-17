from apiflask import APIBlueprint

bp = APIBlueprint('route', __name__)

from app.routes import route

from app.routes import api

from app.routes import login

from app.routes import admin

from app.routes import error

from app.routes import contacts

from app.routes import messages

from app.routes import classify 

