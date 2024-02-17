from apiflask import APIBlueprint

bp_message = APIBlueprint("message", __name__)

from ..messages import message