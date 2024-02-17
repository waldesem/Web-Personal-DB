from apiflask import APIBlueprint

bp_login = APIBlueprint("route", __name__)

from .login import login