from apiflask import APIBlueprint

bp_files = APIBlueprint("files", __name__)

from ..files import files