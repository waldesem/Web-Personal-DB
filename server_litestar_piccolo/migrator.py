"""Migration from sqlite to postgresql."""

import asyncio
import sqlite3
from datetime import UTC, datetime
from functools import wraps
from typing import TYPE_CHECKING

import bcrypt
import click
from piccolo.conf.apps import table_finder
from piccolo.table import Table, create_db_tables, drop_db_tables
from pydantic import BaseModel
from rich import print as rprint

from app.classes.classes import ItemCategory
from app.models.items import ItemTypeOut
from app.models.person import PersonForm
from app.tables.tables import Persons, Users
from constants import DEFAULT_PASSWORD

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


class PersonOut(PersonForm):
    """Person schema."""

    id: int
    destination: str | None = None
    editable: bool
    protected: bool | None
    user_id: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def normalize_name(cls, v: str | None) -> str | None:
        """Normalize name."""
        return v

    @classmethod
    def check_inn(cls, inn: str | None) -> str | None:
        """Check inn."""
        return inn

    @classmethod
    def check_snils(cls, snils: str | None) -> str | None:
        """Check snils."""
        return snils


class ItemModelOut(BaseModel):
    """Validation class."""

    item: ItemTypeOut


def async_cmd(f: Callable) -> Callable:
    """Async command decorator."""

    @wraps(f)
    def wrapper(*args: tuple, **kwargs: dict) -> None:
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.command()
@click.argument("path", type=click.Path(exists=True))
@async_cmd
async def migrate(path: Path) -> None:
    """MIgrate data from sqlite to postgresql.

    Example:
        python.exe migrator.py "/path/database.db"

    """
    tables = table_finder(modules=["app.tables.tables"])
    await drop_db_tables(*tables)
    await create_db_tables(*tables)
    await Table.raw(
        """
        ALTER TABLE persons DROP CONSTRAINT IF EXISTS person_data;
        ALTER TABLE persons
        ADD CONSTRAINT person_data
        UNIQUE (surname, firstname, patronymic, birthday)
        """,
    )

    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        users = cur.execute("SELECT * FROM users").fetchall()
        for user in users:
            await Users.insert(
                Users(
                    id=user["id"],
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
                ),
            )

        persons = cur.execute("SELECT * FROM persons").fetchall()
        for person in persons:
            persona = dict(person)
            persona["created_at"] = persona["updated_at"] = persona.pop("created")
            new_person = PersonOut(**persona).model_dump(
                exclude={"id"},
            )
            new_person["created_at"] = new_person["updated_at"] = (
                new_person["updated_at"]
                if new_person["updated_at"].tzinfo
                else new_person["updated_at"].replace(tzinfo=UTC)
            )
            new_person = Persons(**new_person)
            await new_person.save()

            for table in ItemCategory:
                items = cur.execute(
                    f"SELECT * FROM {table.value} WHERE person_id = ?",  # noqa: S608
                    (persona["id"],),
                ).fetchall()

                for itm in items:
                    if itm:
                        data = dict(itm)
                        data["item"] = table.value
                        if data.get("created"):
                            data["created_at"] = data["updated_at"] = data["created"]
                        data = {"item": data}
                        new_data = ItemModelOut.model_validate(
                            data,
                        ).item.model_dump(
                            exclude={"id", "item"},
                        )
                        if "created_at" in new_data and "updated_at" in new_data:
                            new_data["created_at"] = new_data["updated_at"] = (
                                new_data["updated_at"]
                                if new_data["updated_at"].tzinfo
                                else new_data["updated_at"].replace(tzinfo=UTC)
                            )
                        new_data["person_id"] = new_person.id
                        data_table = table_finder(
                            modules=["app.tables.tables"],
                            include_tags=[table],
                        )[0]
                        data_table.insert(data_table(new_data))

        rprint("Migration finished!")


if __name__ == "__main__":
    migrate()
