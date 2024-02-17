from apiflask import APIBlueprint

bp_persons = APIBlueprint("route", __name__)

from .persons import persons