"""Command line module."""

import click
from flask import Blueprint, cli
from pydantic import ValidationError
from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.classes.classes import Roles
from app.models.models import UserForm
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
    role: Roles,
) -> None:
    """Create a new user.

    Example:
        export FLASK_APP=app
        flask command user Super superadmin 'superadmin@localhost.ru' --role=admin

    """
    try:
        user = UserForm(
            fullname=fullname,
            username=username,
            email=email,
            role=role,
        )
        if db.session.execute(
            select(Users).where(
                or_(Users.username == username, Users.email == email),
            ),
        ).scalar():
            click.echo(f"User {username} already exists or email is taken")
        else:
            db.session.add(Users(**user.model_dump()))
            db.session.commit()
            click.echo(f"User {username} created")
    except (ValidationError, SQLAlchemyError) as error:
        click.echo(error)
        db.session.rollback()
