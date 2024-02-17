from apiflask import APIBlueprint

bp_persons = APIBlueprint("persons", __name__)

from ..person import persons