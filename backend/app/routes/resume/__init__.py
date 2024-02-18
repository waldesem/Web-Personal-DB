from apiflask import APIBlueprint

bp_resume = APIBlueprint("resume", __name__)

from . import resume
