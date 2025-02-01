"""Command line module."""

from pathlib import Path

import click
from flask import Blueprint, current_app
from flask.cli import with_appcontext
from sqlalchemy import text

from app.model.classes import Regions, Roles
from app.model.tables import db_session

bp = Blueprint("command", __name__)


@bp.cli.command("user")
@click.argument("fullname")
@click.argument("username")
@click.argument("email")
@click.option(
    "--role",
    type=click.Choice([role.value for role in Roles]),
    default=Roles.admin.value,
)
@click.option(
    "--region",
    type=click.Choice([region.name for region in Regions]),
    default=Regions.main.name,
)
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
        flask command user 'Super Admin' superadmin superadmin@elocalhost \
            --role=admin --region=main

    """
    if not db_session.execute(
        text("SELECT * FROM users WHERE username = :username"),
        {"username": username},
    ).all():
        db_session.execute(text(
            "INSERT INTO users (fullname, username, email, role, region) "
            "VALUES (:fullname, :username, :email, :role, :region)",
            {
                "fullname": fullname,
                "username": username,
                "email": email,
                "role": role,
                "region": Regions[region].value,
            },
        ))
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
    if Path(current_app.config["BASE_PATH"]).is_dir():
        for region in Regions:
            region_path = Path(current_app.config["BASE_PATH"], region.value)
            region_path.mkdir(exist_ok=True)
            for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ":
                Path(region_path, letter).mkdir(exist_ok=True)
        click.echo("Folders created")
    else:
        click.echo("BASE_PATH is not a directory")
