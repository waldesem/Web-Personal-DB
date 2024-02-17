from apiflask import APIBlueprint

bp_message = APIBlueprint("route", __name__)

from .message import message