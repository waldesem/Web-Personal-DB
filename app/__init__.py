import datetime

from flask import Flask

from config import Config
from app.models.model import db
from app.login.userlogin import login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)
    from app.main import bp_routes as routes
    app.register_blueprint(routes)
    from app.main import bp_api as api
    app.register_blueprint(api)
    app.permanent_session_lifetime = datetime.timedelta(days=30)
    return app
