from flask import Blueprint

from .relations import bp as relations_bp

bp = Blueprint("items", __name__)

bp.register_blueprint(relations_bp)
