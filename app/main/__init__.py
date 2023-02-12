from flask import Blueprint

bpr = Blueprint('route', __name__)
bpa = Blueprint('api', __name__)

from app.main import routes
from app.main import apis
