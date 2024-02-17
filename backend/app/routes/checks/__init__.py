from apiflask import APIBlueprint

bp_checks = APIBlueprint("route", __name__)

from .checks import checks