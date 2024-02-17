from apiflask import APIBlueprint

bp_manager = APIBlueprint("route", __name__)

from .manager import manager