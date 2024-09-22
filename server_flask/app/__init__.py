import logging

from flask import Flask

# from flask_cors import CORS
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from config import Config
from .model.classes import Regions, Roles
from .model.tables import db_session, Users
from .routes.route import bp as route_bp

file_handler = logging.FileHandler("error.log")
file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)


def create_app(config_class=Config):
    """
    Create and configure the Flask application.

    Parameters:
        config_class: The configuration class to use for the application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(route_bp)
    app.logger.addHandler(file_handler)
    # CORS(app, resources={r"/*": {"origins": "*"}})

    if not db_session.execute(
        select(Users).filter(Users.role == Roles.admin.value)
    ).all():
        admin = Users(
            fullname="Администратор",
            username="superadmin",
            email="admin@localhost.ru",
            role=Roles.admin.value,
            passhash=generate_password_hash(Config.DEFAULT_PASSWORD),
            region=Regions.main.value,
        )
        db_session.add(admin)
        db_session.commit()
    db_session.remove()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @app.get("/", defaults={"path": ""})
    def main(path=""):
        return app.send_static_file("index.html")

    @app.get("/<path:path>")
    def static_file(path=""):
        return app.send_static_file(path)

    @app.errorhandler(Exception)
    def handle_error(error):
        app.logger.error(error)
        return app.redirect("/")

    return app
