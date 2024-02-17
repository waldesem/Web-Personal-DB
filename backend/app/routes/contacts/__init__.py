from apiflask import APIBlueprint

bp_contact = APIBlueprint("route", __name__)

from .contact import contact