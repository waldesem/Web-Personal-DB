"""Routes."""

from flask import Blueprint

from .anketa import bp as anketa_bp
from .index import bp as route_bp
from .items import bp as items_bp
from .login import bp as login_bp
from .person import bp as person_bp
from .user import bp as user_bp

bp = Blueprint("route", __name__, url_prefix="/route")

bp.register_blueprint(anketa_bp)
bp.register_blueprint(items_bp)
bp.register_blueprint(login_bp)
bp.register_blueprint(route_bp)
bp.register_blueprint(person_bp)
bp.register_blueprint(user_bp)
