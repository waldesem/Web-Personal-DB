from flask import Flask

from config import Config
from .routes.route import bp as route_bp
from .cors.extension import CORS


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    app.register_blueprint(route_bp)

    return app