from flask import Blueprint

bp = Blueprint("route", __name__)

from . import connects, files, index, login, person, users
