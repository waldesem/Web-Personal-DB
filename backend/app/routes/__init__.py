from apiflask import APIBlueprint

bp = APIBlueprint("route", __name__)

from . import admin
from . import anketa
from . import checks
from . import classify
from . import contact
from . import files
from . import index
from . import login
from . import manager
from . import message
from . import resume
