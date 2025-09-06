"""Routes."""

from flask import Blueprint

from .index import bp as route_bp
from .items import bp as items_bp
from .login import bp as login_bp
from .person import bp as person_bp
from .user import bp as user_bp

bp = Blueprint("routes", __name__, url_prefix="/routes")

bp.register_blueprint(items_bp)
bp.register_blueprint(login_bp)
bp.register_blueprint(route_bp)
bp.register_blueprint(person_bp)
bp.register_blueprint(user_bp)
