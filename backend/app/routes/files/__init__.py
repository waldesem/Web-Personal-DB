from apiflask import APIBlueprint

bp_files = APIBlueprint("route", __name__)

from .files import files