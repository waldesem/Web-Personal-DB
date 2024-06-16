from flask import Blueprint

bp = Blueprint("route", __name__)

from . import contacts, files, index, login, person, users
