import os

import click
from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from config import setting
from .model.classes import Roles, Regions
from .model.tables import db_session, Users

from . import create_app


app = create_app()


@app.cli.command("user")
@click.argument("fullname", "username", "email")
@click.option("--role", type=click.Choice([role.value for role in Roles]))
@click.option("--region", type=click.Choice([region.value for region in Regions]))
@with_appcontext
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
    if not db_session.execute(select(Users).filter(Users.username == username)).all():
        db_session.add(
            Users(
                fullname=fullname,
                username=username,
                email=email,
                role=role,
                passhash=generate_password_hash(current_app.config["DEFAULT_PASSWORD"]),
                region=region,
            )
        )
        db_session.commit()
    db_session.remove()

    click.echo(f"User {username} created")


@app.cli.command("folder")
@click.argument("folder", default=None)
@with_appcontext
def create_folders(folder):
    """Create the folders structure according to the current configuration.

    The folders structure is as follows: BASE_PATH/REGION/LETTER, where BASE_PATH
    is the base path defined in the configuration, REGION is one of the regions
    defined in the Regions enum, and LETTER is one of the letters defined in the
    configuration.

    :param folder: The folder to create the structure in. If not provided, the
        current BASE_PATH is used.
    """
    if folder:
        setting["Destination"]["path"] = folder
    if not os.path.isdir(current_app.config["BASE_PATH"]):
        os.mkdir(current_app.config["BASE_PATH"])
    for region in Regions:
        region_path = os.path.join(current_app.config["BASE_PATH"], region.value)
        if not os.path.isdir(region_path):
            os.mkdir(region_path)
        for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ":
            letter_path = os.path.join(region_path, letter)
            if not os.path.isdir(letter_path):
                os.mkdir(letter_path)
