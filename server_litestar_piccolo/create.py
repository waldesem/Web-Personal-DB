"""Command line module."""

import asyncio
from functools import wraps
from typing import TYPE_CHECKING

import bcrypt
import click
from piccolo.conf.apps import table_finder
from piccolo.table import create_db_tables, drop_db_tables
from rich import print as rprint

from app.classes.classes import Roles
from app.models.user import UserForm
from app.tables.tables import Persons, Users
from constants import DEFAULT_PASSWORD

if TYPE_CHECKING:
    from collections.abc import Callable


def async_cmd(f: Callable) -> Callable:
    """Async command decorator."""

    @wraps(f)
    def wrapper(*args: tuple, **kwargs: dict) -> None:
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.command()
@click.argument("fullname")
@click.argument("username")
@click.argument("email")
@click.argument("role", type=click.Choice(Roles))
@async_cmd
async def create(fullname: str, username: str, email: str, role: Roles) -> None:
    """Create a new user.

    Example:
        python3 create.py "Super User" superadmin super@host.ru admin

    """
    tables = table_finder(modules=["app.tables.tables"])
    await drop_db_tables(*tables)
    await create_db_tables(*tables, if_not_exists=True)

    await Persons.raw(
        """
        ALTER TABLE persons
        ADD CONSTRAINT person_data
        UNIQUE (surname, firstname, patronymic, birthday)
        """,
    )

    data = UserForm(fullname=fullname, username=username, email=email, role=role)
    user = (
        await Users.insert(
            Users(
                username=data.username,
                email=data.email,
                passhash=bcrypt.hashpw(DEFAULT_PASSWORD.encode(), bcrypt.gensalt()),
                role=data.role,
            ),
        )
        .on_conflict(action="DO NOTHING")
        .returning(Users.id)
    )
    if not user:
        rprint(f"User {username} already exists or email is taken")
    else:
        rprint(f"User {username} created")


if __name__ == "__main__":
    create()
