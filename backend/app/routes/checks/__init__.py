from apiflask import APIBlueprint

bp_checks = APIBlueprint("checks", __name__)

from ..checks import checks