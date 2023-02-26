from flask import Blueprint

bpr = Blueprint('route', __name__)

from app.main import routes
