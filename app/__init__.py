import os
import logging
from logging.handlers import RotatingFileHandler

from apiflask import APIFlask
from flask_migrate import Migrate
from flask_cors import CORS

from config import DevelopmentConfig, ProductionConfig
from app.models.model import db, ma, User
from app.admin.admin import admin
from app.routes.login import lm

 
def create_app():
    """
    Initializes and returns a Flask app object with various extensions and configurations.
    Returns:
        app (Flask): A Flask app object.
    """
    app = APIFlask(__name__, title="Web-Personal-DB API", version="1.0")
    
    # Set up app configurations
    app.config.from_object(DevelopmentConfig)
    app.json.sort_keys = False
    CORS(app)
    admin.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    lm.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db, render_as_batch=True)
    
    # Register Blueprints
    from app.routes import bp as route_bp
    app.register_blueprint(route_bp)

    # Set up logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/log.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.WARNING)
    app.logger.info('This is a warning message')

    @lm.user_loader
    def load_user(user_id):
        """
        Loads a user object from the database based on the given user ID.
        Args:
            user_id (int): The ID of the user to load.
        Returns:
            user (User): A User object representing the loaded user.
        """
        return User.query.get(user_id)
    
    return app
