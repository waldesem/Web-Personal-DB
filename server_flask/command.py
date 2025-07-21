"""Command line module."""

from pathlib import Path

import click
from flask import Blueprint, cli, current_app
from pydantic import ValidationError, schema_json_of
from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.classes.classes import Roles
from app.models.models import (
    AnketaJson,
    Candidates,
    Content,
    Index,
    Items,
    Login,
    PersonIn,
    PersonOut,
    Token,
    User,
    UserActions,
    UserForm,
)
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

    The user is created with a default password given in DEFAULT_PASSWORD config
    variable. The user is created only if it does not exist in the database.

    :param fullname: The full name of the user.
    :param username: The username of the user.
    :param email: The email of the user.
    :param role: The role of the user.

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
    """Create the folders structure according to the current configuration.

    :param folder: The folder to create the structure in. If not provided, the
        current BASE_PATH is used.
    """
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
    tests = Path("schemas")
    tests.mkdir(exist_ok=True)
    for model in [
        AnketaJson,
        Candidates,
        Content,
        Index,
        Items,
        Login,
        PersonIn,
        PersonOut,
        Token,
        User,
        UserActions,
        UserForm,
    ]:
        file_path = Path(tests, f"{model.__name__}.json")
        with Path.open(file_path, "w") as f:
            schema = model.schema_json(by_alias=model.__name__ == "AnketaJson")
            f.write(schema)

    file_path = Path(tests, "Content.json")
    with Path.open(file_path, "w") as f:
        schema = schema_json_of(Content, title="Схема для валидации зависимых таблиц.")
        f.write(schema)

    file_path = Path(tests, "Items.json")
    with Path.open(file_path, "w") as f:
        schema = schema_json_of(Items, title="Схема валидации типа зависимых таблиц.")
        f.write(schema)
