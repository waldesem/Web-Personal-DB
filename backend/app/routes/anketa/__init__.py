from apiflask import APIBlueprint

bp_anketa = APIBlueprint("anketa", __name__)

from ..anketa import anketa
