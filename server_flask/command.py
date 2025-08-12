"""Command line module."""

from pathlib import Path

import click
from flask import Blueprint, cli, current_app
from pydantic import ValidationError
from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.classes.classes import Roles
from app.models.models import AnketaJson, UserForm
from app.tables.tables import Users

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
@cli.with_appcontext
def create_user(
    fullname: str,
    username: str,
    email: str,
    role: str,
) -> None:
    """Create a new user.

    Example:
        export FLASK_APP=app
        flask command user 'Super Admin' superadmin superadmin@elocalhost \
            --role=admin

    """
    try:
        user = UserForm(
            fullname=fullname,
            username=username,
            email=email,
            role=role,
        )
        created = db.session.execute(
            select(Users).where(
                or_(Users.username == username or Users.email == email),
            ),
        ).scalar()
        if created:
            click.echo(f"User {username} already exists or email is taken")
        else:
            db.session.add(Users(**user.dict()))
            db.session.commit()
            click.echo(f"User {username} created")
    except (ValidationError, SQLAlchemyError) as error:
        click.echo(error)
        db.session.rollback()


@bp.cli.command("folders")
@cli.with_appcontext
def create_folders() -> None:
    """Create the folders structure according to the current configuration."""
    if Path(current_app.config["BASE_PATH"]).is_dir():
        for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ":
            Path(
                current_app.config["BASE_PATH"],
                "Главный офис",
                letter,
            ).mkdir(exist_ok=True, parents=True)
        click.echo("Folders created")
    else:
        click.echo("BASE_PATH is not a directory")


@bp.cli.command("schemas")
@cli.with_appcontext
def create_schemas() -> None:
    """Create schemas."""
    path = Path("..", "schemas")
    path.mkdir(exist_ok=True)
    file_path = Path(path, f"{AnketaJson.__name__}.json")
    with file_path.open("w", encoding="utf-8") as f:
        schema = AnketaJson.schema_json(by_alias=AnketaJson.__name__ == "AnketaJson")
        f.write(schema)
