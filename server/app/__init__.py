import os
import logging
import bcrypt
import datetime

from logging.handlers import RotatingFileHandler

from apiflask import APIFlask
from flask_migrate import Migrate
from flask_cors import CORS

from config import SqliteConfig, PostgresConfig
from app.models.model import User, Role, db, ma
from app.admin.admin import admin
from app.routes.login import jwt
from app.utils.update import scheduler
from app.utils.check import broker

 
def create_app():
    """
    Initializes and returns a APIFlask app object with various extensions and configurations.
    Returns:
        app (APIFlask): A APIFlask app object.
    """
    app = APIFlask(__name__, static_folder='dist', title="Web-Personal-DB", version="1.0")
    
    # Set up app configurations
    app.config.from_object(SqliteConfig)
    app.json.sort_keys = False
    CORS(app, supports_credentials=True)
    admin.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db, render_as_batch=True)
    broker.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    # Register Blueprints
    from app.routes import bp as route_bp
    app.register_blueprint(route_bp)

    # Set up logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/log.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.WARNING)
    app.logger.info('This is a warning message')

    # create db and admin user
    with app.app_context():
        db.create_all()
        admin_user = db.session.query(User).filter_by(username='admin').first()
        if not admin_user:
            new_admin = User(fullname='Administrator',
                             username='admin', 
                             pswd_create = datetime.date.today(),
                             password = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt()))
            role = Role(name='admin')
            new_admin.roles.append(role)
            db.session.add(new_admin)
            db.session.commit()

    return app
