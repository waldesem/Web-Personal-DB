"""Command line module."""

from pathlib import Path

import click
from flask import Blueprint, cli, current_app
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.model.classes import Regions, Roles
from app.model.models import User
from app.model.tables import Users, db_session

bp = Blueprint("command", __name__)


@bp.cli.command("user")
@click.argument("fullname")
@click.argument("username")
@click.argument("email")
@click.option(
    "--role",
    type=click.Choice([role.value for role in Roles]),
    default=Roles.user.value,
)
@click.option(
    "--region",
    type=click.Choice([region.name for region in Regions]),
    default=Regions.main.name,
)
@cli.with_appcontext
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
    try:
        user = User(
            fullname=fullname,
            username=username,
            email=email,
            role=role,
            region=region,
        )
        if not db_session.execute(
            select(Users).where(Users.username == user.username),
        ).all():
            db_session.add(Users(**user.dict()))
            db_session.commit()
            click.echo(f"User {user.username} created")
        else:
            click.echo(f"User {user.username} already exists")
    except (ValidationError, SQLAlchemyError) as error:
        click.echo(error)


@bp.cli.command("folders")
@cli.with_appcontext
def create_folders() -> None:
    """Create the folders structure according to the current configuration.

    :param folder: The folder to create the structure in. If not provided, the
        current BASE_PATH is used.
    """
    if Path(current_app.config["BASE_PATH"]).is_dir():
        for region in Regions:
            region_path = Path(current_app.config["BASE_PATH"], region.value)
            region_path.mkdir(exist_ok=True, parents=True)
            for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ":
                Path(region_path, letter).mkdir(exist_ok=True, parents=True)
        click.echo("Folders created")
    else:
        click.echo("BASE_PATH is not a directory")
