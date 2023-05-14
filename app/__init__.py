import os
import logging
from logging.handlers import RotatingFileHandler

from apiflask import APIFlask
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_cors import CORS 

from config import DevelopmentConfig, ProductionConfig
from app.models.model import db, ma, User
from app.admins.admin import admin


def create_app():
    """
    Initializes and returns a Flask app object with various extensions and configurations.

    Returns:
        app (Flask): A Flask app object.
    """
    app = APIFlask(__name__, title="Web-Personal-DB API", version="1.0")
    
    # Set up app configurations
    app.config.from_object(ProductionConfig)
    app.json.sort_keys = False
    CORS(app)
    admin.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'route.login'
    login_manager.init_app(app)
    bootstrap = Bootstrap5()
    bootstrap.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db, render_as_batch=True)
    
    # Register Blueprints
    from app.routes import bp as route_bp
    app.register_blueprint(route_bp)

    # Set up logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/log.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.WARNING)
    app.logger.info('This is a warning message')

    @login_manager.user_loader
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


# for start application in debug mode enter commands in terminal: 
# export FLASK_APP=app
# export FLASK_DEBUG=1
# flask run

# for create database enter commands in $flask shell:
# db.create_all()

# for migrate database enter commands in $flask shell:
# flask db init - only first time if migration folder is not exist
# flask db migrate
# flask db upgrade
