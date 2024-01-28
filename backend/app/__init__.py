from apiflask import APIFlask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import BadRequest
from config import Config

ma = Marshmallow()
db = SQLAlchemy()
cache = Cache()
jwt = JWTManager()


def create_app(config_class=Config):
    """
    Initializes and configures a Flask application.
    """
    app = APIFlask(__name__, title="StaffSec", docs_ui="redoc")
    app.config.from_object(config_class)
    app.json.sort_keys = False
    # app.config['REDOC_STANDALONE_JS'] = './static/redoc.standalone.js'
    # for local use, download redoc.standalone.js
    # from https://github.com/Redocly/redoc/blob/master/redoc/static/redoc.standalone.js
    # and save it in the static folder or in frontend/public

    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db, render_as_batch=True)

    from app.routes import bp as route_bp

    app.register_blueprint(route_bp)

    from cli import register_cli

    register_cli(app)

    @app.get("/", defaults={"path": ""})
    @app.get("/<path:path>")
    @app.doc(hide=True)
    def main(path=""):
        return app.send_static_file("index.html")

    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        return e, 400

    return app
