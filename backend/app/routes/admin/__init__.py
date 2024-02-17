from apiflask import APIBlueprint

bp_admin = APIBlueprint("route", __name__)

from .admin import admin