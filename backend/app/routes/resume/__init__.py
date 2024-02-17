from apiflask import APIBlueprint

bp_resume = APIBlueprint("route", __name__)

from .resume import resume
