from flask import Blueprint


bp_routes = Blueprint('routes', __name__)
bp_api = Blueprint('api', __name__)

from app.main import routes
from app.main import api
