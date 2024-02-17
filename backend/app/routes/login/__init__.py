from apiflask import APIBlueprint

bp_login = APIBlueprint("login", __name__)

from ..login import login