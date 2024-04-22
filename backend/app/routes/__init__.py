from apiflask import APIBlueprint

bp = APIBlueprint("route", __name__)

from . import admin
from . import index
from . import resume
from . import items
from . import files
from . import classify
from . import contact
from . import login
from . import message
from . import robot
from . import gpt

