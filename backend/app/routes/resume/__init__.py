from apiflask import APIBlueprint

bp_resume = APIBlueprint("resume", __name__)

from ..resume import resume
