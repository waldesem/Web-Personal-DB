from apiflask import APIBlueprint

bp_manager = APIBlueprint("manager", __name__)

from . import manager