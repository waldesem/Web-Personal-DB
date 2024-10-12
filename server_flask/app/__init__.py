from configparser import ConfigParser
import logging
import os

import click
from flask import Flask
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from config import Config, basedir
from .model.tables import db_session, Users
from .model.classes import Roles, Regions
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

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @app.get("/", defaults={"path": ""})
    def main(path=""):
        return app.send_static_file("index.html")

    @app.get("/<path:path>")
    def static_file(path=""):
        return app.send_static_file(path)

    @app.errorhandler(404)
    def handle_404(error):
        return app.redirect("/")

    @app.errorhandler(400)
    def handle_400(error):
        app.logger.exception(error)
        return app.redirect("/")
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.exception(error)
        return error

    @app.cli.command("user")
    @click.argument("fullname")
    @click.argument("username")
    @click.argument("email")
    @click.option("--role", type=click.Choice([role.value for role in Roles]))
    @click.option("--region", type=click.Choice([region.name for region in Regions]))
    def create_user(fullname, username, email, region, role):
        """Create a new user.

        The user is created with a default password given in DEFAULT_PASSWORD config
        variable. The user is created only if it does not exist in the database.

        :param fullname: The full name of the user.
        :param username: The username of the user.
        :param email: The email of the user.
        :param region: The region of the user.
        :param role: The role of the user.
        """
        if not db_session.execute(
            select(Users).filter(Users.username == username)
        ).all():
            db_session.add(
                Users(
                    fullname=fullname,
                    username=username,
                    email=email,
                    role=role,
                    passhash=generate_password_hash(config_class.DEFAULT_PASSWORD),
                    region=Regions[region].value,
                )
            )
            db_session.commit()
            click.echo(f"User {username} created")
        else:
            click.echo(f"User {username} already exists")
        db_session.remove()

    @app.cli.command("folders")
    def create_folders():
        """Create the folders structure according to the current configuration.

        The folders structure is as follows: BASE_PATH/REGION/LETTER, where BASE_PATH
        is the base path defined in the configuration, REGION is one of the regions
        defined in the Regions enum, and LETTER is one of the letters defined in the
        configuration.

        :param folder: The folder to create the structure in. If not provided, the
            current BASE_PATH is used.
        """
        setting = ConfigParser()
        setting.read(os.path.join(basedir, "settings.ini"), encoding="utf-8")
        base_path = setting.get("Destination", "path")
        for region in Regions:
            region_path = os.path.join(base_path, region.value)
            if not os.path.isdir(region_path):
                os.mkdir(region_path)
            for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ":
                letter_path = os.path.join(region_path, letter)
                if not os.path.isdir(letter_path):
                    os.mkdir(letter_path)
        click.echo("Folders created")

    return app
