from apiflask import APIBlueprint

bp_classify = APIBlueprint("classify", __name__)

from . import classify