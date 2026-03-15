"""Migration from sqlite to postgresql."""

import asyncio
import sqlite3
from datetime import UTC, datetime
from functools import wraps
from typing import TYPE_CHECKING

import bcrypt
import click
from advanced_alchemy.base import BigIntAuditBase
from rich import print as rprint

from app.classes.classes import ItemCategory
from app.models.items import ItemModelOut
from app.models.person import PersonOut
from app.models.user import User
from app.tables.tables import Persons, Users, config
from constants import DEFAULT_PASSWORD

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

tables = BigIntAuditBase.metadata.tables


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
        python3 migrator.py "/path/database.db"

    """
    async with config.get_engine().begin() as async_conn:
        await async_conn.run_sync(BigIntAuditBase.metadata.drop_all)
        await async_conn.run_sync(BigIntAuditBase.metadata.create_all)

    with sqlite3.connect(path) as conn:
        async with config.get_session() as db_session:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            users = cur.execute("SELECT * FROM users").fetchall()
            new_users = []
            for user in users:
                new_user = User(
                    id=user["id"],
                    fullname=user["fullname"],
                    username=user["username"],
                    email=user["email"],
                    role=user["role"],
                    blocked=False,
                    deleted=False,
                    attempt=0,
                    change_pswd=True,
                    pswd_create=datetime.now(UTC),
                    created_at=datetime.now(UTC),
                    updated_at=datetime.now(UTC),
                ).model_dump(exclude={"id"})
                new_user["passhash"] = bcrypt.hashpw(
                    DEFAULT_PASSWORD.encode(),
                    bcrypt.gensalt(),
                )
                new_users.append(Users(**new_user))
            db_session.add_all(new_users)

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
                db_session.add(new_person)
                await db_session.flush()

                for table in ItemCategory:
                    items = cur.execute(
                        f"SELECT * FROM {table.value} WHERE person_id = ?",  # noqa: S608
                        (persona["id"],),
                    ).fetchall()

                    inserts: list[dict] = []
                    for itm in items:
                        if itm:
                            data = dict(itm)
                            data["item"] = table.value
                            if data.get("created"):
                                data["created_at"] = data["updated_at"] = data[
                                    "created"
                                ]
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
                            inserts.append(new_data)

                    if inserts:
                        stmt = tables[table.value].insert().values(inserts)
                        await db_session.execute(stmt)

            await db_session.commit()
            rprint("Migration finished!")


if __name__ == "__main__":
    migrate()
