"""Command line module."""

from pathlib import Path

import click
from flask import Blueprint, current_app
from flask.cli import with_appcontext
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from app.model.classes import Regions, Roles
from app.model.tables import Users, db_session

bp = Blueprint("command", __name__)


@bp.cli.command("user")
@click.argument("fullname")
@click.argument("username")
@click.argument("email")
@click.option("--role", type=click.Choice([role.value for role in Roles]))
@click.option("--region", type=click.Choice([region.name for region in Regions]))
@with_appcontext
def create_user(
    fullname: str,
    username: str,
    email: str,
    region: str,
    role: str,
) -> None:
    """Create a new user.

    The user is created with a default password given in DEFAULT_PASSWORD config
    variable. The user is created only if it does not exist in the database.

    :param fullname: The full name of the user.
    :param username: The username of the user.
    :param email: The email of the user.
    :param region: The region of the user.
    :param role: The role of the user.

    Example:
        export FLASK_APP=app
        flask command user 'Super Admin' superadmin superadmin@elocalhost --role=admin --region=main

    """
    if not db_session.execute(
        select(Users).filter(Users.username == username),
    ).all():
        db_session.add(
            Users(
                fullname=fullname,
                username=username,
                email=email,
                role=role,
                passhash=generate_password_hash(current_app.config["DEFAULT_PASSWORD"]),
                region=Regions[region].value,
            ),
        )
        db_session.commit()
        click.echo(f"User {username} created")
    else:
        click.echo(f"User {username} already exists")
    db_session.remove()


@bp.cli.command("folders")
@with_appcontext
def create_folders() -> None:
    """Create the folders structure according to the current configuration.

    :param folder: The folder to create the structure in. If not provided, the
        current BASE_PATH is used.
    """
    for region in Regions:
        region_path = Path(current_app.config["BASE_PATH"], region.value)
        Path.mkdir(region_path, exist_ok=True)
        for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ":
            letter_path = Path(region_path, letter)
            Path.mkdir(letter_path, exist_ok=True)
    click.echo("Folders created")
