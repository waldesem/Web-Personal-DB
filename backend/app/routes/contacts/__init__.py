from apiflask import APIBlueprint

bp_contact = APIBlueprint("contact", __name__)

from . import contact