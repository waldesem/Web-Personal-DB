from flask import Blueprint

bpa = Blueprint('api', __name__)

from app.api import api
