from apiflask import APIBlueprint

bp_anketa = APIBlueprint("route", __name__)

from .anketa import anketa
