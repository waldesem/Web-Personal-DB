from apiflask import APIBlueprint

bp_classify = APIBlueprint("route", __name__)

from .classify import classify