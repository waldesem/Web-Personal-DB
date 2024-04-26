from apiflask import APIFlask
from flask import jsonify, send_from_directory
from flask_migrate import Migrate
from flask_cors import CORS
from flask_caching import Cache
from flask_jwt_extended import JWTManager

from config import Config
from .models.model import db

cache = Cache()
jwt = JWTManager()
migrate = Migrate()


def create_app(config=Config):
    """
    Initializes and configures a Flask application.
    """
    app = APIFlask(__name__, title="StaffSec", docs_ui="redoc")
    app.config.from_object(config)
    # app.config['REDOC_STANDALONE_JS'] = './static/redoc.standalone.js'
    # for local use, download redoc.standalone.js
    # from https://github.com/Redocly/redoc/blob/master/redoc/static/redoc.standalone.js
    # Save it in the static folder or in frontend/public before build
    # Uncomment string app.config['REDOC_STANDALONE_JS'] = './static/redoc.standalone.js'

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from app.routes import bp as route_bp

    app.register_blueprint(route_bp)

    from cli import register_cli

    register_cli(app)

    @app.doc(hide=True)
    @app.get("/", defaults={"path": ""})
    @app.get("/<path:path>")
    def main(path=""):
        return app.send_static_file("index.html")

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(error=str(error)), 404

    return app
