import os

from apiflask import APIFlask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_apscheduler import APScheduler
from flask import send_from_directory

from config import Config

ma = Marshmallow()
db = SQLAlchemy()
cache = Cache()
jwt = JWTManager()
scheduler = APScheduler()


def create_app(config_class=Config):
    """
    Initializes and configures a Flask application.
    :return: The Flask application instance.
    """
    app = APIFlask(__name__, title="StaffSec", docs_ui="redoc")
    app.config.from_object(config_class)
    app.config['REDOC_STANDALONE_JS'] = './static/redoc.standalone.js'
    app.json.sort_keys = False
    
    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    migrate = Migrate()
    migrate.init_app(app, db, render_as_batch=True)

    from app.routes import bp as route_bp
    app.register_blueprint(route_bp)

    from cli import register_cli
    register_cli(app)

    @app.get('/', defaults={'path': ''})
    @app.get('/<path:path>')
    @app.doc(hide=True)
    def main(path=''):
        """
        Get the file from the specified path in the static folder and return it, 
        or return the index.html file if the path is not found.
        """
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        
        return app.send_static_file('index.html')

    return app