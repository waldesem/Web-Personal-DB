from apiflask import APIBlueprint

bp_admin = APIBlueprint("admin", __name__)

from . import admin