from flask import Blueprint

from .anketa import bp as anketa_bp
from .login import bp as auth_bp
from .file import bp as file_bp
from .items import bp as items_bp
from .route import bp as route_bp
from .user import bp as user_bp

bp = Blueprint("route", __name__, url_prefix="/route")

bp.register_blueprint(auth_bp)
bp.register_blueprint(anketa_bp)
bp.register_blueprint(route_bp)
bp.register_blueprint(user_bp)
bp.register_blueprint(file_bp)
bp.register_blueprint(items_bp)
