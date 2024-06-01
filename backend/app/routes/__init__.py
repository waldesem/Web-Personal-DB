from flask import Blueprint

bp = Blueprint("route", __name__)

from . import login
from . import users
from . import index
from . import person
from . import openapi
