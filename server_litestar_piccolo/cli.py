"""Command line module."""

import asyncio
import sqlite3
from datetime import UTC, datetime
from functools import wraps
from typing import TYPE_CHECKING

import bcrypt
import click
from piccolo.conf.apps import table_finder
from piccolo.table import Table, create_db_tables, drop_db_tables
from piccolo.utils.pydantic import create_pydantic_model
from pydantic import RootModel, field_validator
from rich import print as rprint

from app.classes.classes import ItemCategory, Roles
from app.controllers.items import tables
from app.models.items import ItemTypeOut
from app.models.user import UserForm
from app.tables.tables import Persons, Users
from constants import DEFAULT_PASSWORD

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


class Person(create_pydantic_model(Persons)):  # ty:ignore[unsupported-base]
    """Person schema."""

    @field_validator("updated_at", "created_at")
    @classmethod
    def check_date(cls, v: datetime) -> datetime:
        """Check date tz."""
        return v if v.tzinfo else v.replace(tzinfo=UTC)


class ItemModel(RootModel[ItemTypeOut]):
    """Validation class."""

    @field_validator("updated_at", "created_at")
    @classmethod
    def check_date(cls, v: datetime) -> datetime:
        """Check date tz."""
        return v if v.tzinfo else v.replace(tzinfo=UTC)


def async_decorator(f: Callable) -> Callable:
    """Async command decorator."""

    @wraps(f)
    def wrapper(*args: tuple, **kwargs: dict) -> None:
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group()
def cli() -> None:
    """Cli group."""


@cli.command("create")
@async_decorator
async def create() -> None:
    """MIgrate data from sqlite to postgresql.

    Example:
        python3 cli.py create

    """
    tables = table_finder(modules=["app.tables.tables"])
    await drop_db_tables(*tables)
    await create_db_tables(*tables)

    await Table.raw(
        """ALTER TABLE persons
        ADD CONSTRAINT constraint_surname_firstname_patronymic_birthday
        UNIQUE (surname, firstname, patronymic, birthday);
        """,
    )

    rprint("DB tables creations finished!")


@cli.command("migrate")
@click.argument("path", type=click.Path(exists=True))
@async_decorator
async def migrate(path: Path) -> None:
    """MIgrate data from sqlite to postgresql.

    Example:
        python3 cli.py migrate "/path/database.db"

    """
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        users = cur.execute("SELECT * FROM users").fetchall()
        await Users.insert(
            *[
                Users(
                    fullname=user["fullname"],
                    username=user["username"],
                    email=user["email"],
                    role=user["role"],
                    passhash=bcrypt.hashpw(DEFAULT_PASSWORD.encode(), bcrypt.gensalt()),
                    blocked=False,
                    deleted=False,
                    attempt=0,
                    change_pswd=True,
                    pswd_create=datetime.now(UTC),
                    created_at=datetime.now(UTC),
                    updated_at=datetime.now(UTC),
                )
                for user in users
            ],
        )

        persons = cur.execute("SELECT * FROM persons").fetchall()
        for person in persons:
            persona = dict(person)
            persona["protected"] = persona["deleted"] = False
            persona["created_at"] = persona["updated_at"] = persona.get("created")
            new_person = Person(**persona).model_dump(
                exclude={"id"},
            )
            new_person = Persons(**new_person)
            await new_person.save()

            for category in ItemCategory:
                table = tables[category.value]
                items = cur.execute(
                    f"SELECT * FROM {category.value} WHERE person_id = ?",  # noqa: S608
                    (persona["id"],),
                ).fetchall()

                for itm in items:
                    data = dict(itm) | {"item": category.value}
                    data["created_at"] = data["updated_at"] = (
                        data["created"] if data.get("created") else datetime.now(UTC)
                    )
                    new_data = ItemModel.model_validate(data).model_dump(
                        exclude={"id", "item"},
                    )
                    await table.insert(table(**new_data, person_id=new_person.id))

        rprint("Migration finished!")


@cli.command("user")
@click.argument("fullname")
@click.argument("username")
@click.argument("email")
@click.argument("role", type=click.Choice(Roles))
@async_decorator
async def user(fullname: str, username: str, email: str, role: Roles) -> None:
    """Create a new user.

    Example:
        python3 cli.py user "Super User" superadmin super@host.ru admin

    """
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
    cli()
