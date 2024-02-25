from apiflask import APIBlueprint

bp = APIBlueprint("route", __name__)

from . import admin
from . import candidate
from . import classify
from . import contact
from . import login
from . import manager
from . import message
