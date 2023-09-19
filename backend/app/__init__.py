from apiflask import APIFlask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_jwt_extended import JWTManager

from config import Config

ma = Marshmallow()
db = SQLAlchemy()
cache = Cache()
jwt = JWTManager()


def create_app(config_class=Config):
    """
    Initializes and configures a Flask application.
    :return: The Flask application instance.
    """
    app = APIFlask(__name__, title="StaffSec", docs_ui="redoc")
    app.config.from_object(config_class)
    
    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)  
    migrate = Migrate()
    migrate.init_app(app, db, render_as_batch=True)

    from app.routes import bp as route_bp
    app.register_blueprint(route_bp)

    from command import register_command
    register_command(app)
        
    return app
