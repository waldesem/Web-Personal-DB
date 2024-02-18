from apiflask import APIBlueprint

bp_index = APIBlueprint("persons", __name__)

from . import index