"""Migration from sqlite to postgresql."""

import asyncio
import sqlite3
from datetime import UTC
from pathlib import Path
from typing import TYPE_CHECKING

import typer
from advanced_alchemy.base import BigIntAuditBase
from pydantic import TypeAdapter, ValidationError
from rich import print as rprint

from app.structures.classes import ItemCategory
from app.structures.models import ItemModel, ItemType, Person, User
from app.structures.tables import Persons, Users, config

if TYPE_CHECKING:
    from datetime import datetime

cli = typer.Typer()

tables = BigIntAuditBase.metadata.tables
ta = TypeAdapter(list[ItemType])


def _check_tz(data: datetime) -> datetime:
    return data if data.tzinfo else data.replace(tzinfo=UTC)


async def migrate(path: str) -> None:
    """MIgrate data from sqlite to postgresql.

    Example:
        python.exe migrator.py "/path/database.db"

    """
    async with config.get_engine().begin() as async_conn:
        await async_conn.run_sync(BigIntAuditBase.metadata.drop_all)
        await async_conn.run_sync(BigIntAuditBase.metadata.create_all)

    with sqlite3.connect(Path(path)) as conn:
        async with config.get_session() as db_session:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            users = cur.execute("SELECT * FROM users").fetchall()
            new_users = []
            for user in users:
                new_user = User(**dict(user)).model_dump(
                    exclude={"id", "created_at", "updated_at"},
                )
                new_user["pswd_create"] = _check_tz(new_user["pswd_create"])
                new_users.append(Users(**new_user))
            db_session.add_all(new_users)

            persons = cur.execute("SELECT * FROM persons").fetchall()
            for person in persons:
                persona = dict(person)
                persona["created_at"] = persona.pop("created")
                new_person = Person(**persona).model_dump(exclude={"id"})
                new_person["updated_at"] = new_person["created_at"] = _check_tz(
                    new_person["created_at"],
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
                        try:
                            data = dict(itm)
                            data["item"] = table.value
                            data["created_at"] = data["updated_at"] = _check_tz(
                                data.pop("created"),
                            )
                            new_data = ItemModel(**data).item.model_dump(
                                exclude={"id", "item"},
                            )
                            new_data["person_id"] = new_person.id
                            inserts.append(new_data)
                        except ValidationError as e:
                            rprint(e)

                    if inserts:
                        stmt = tables[table.value].insert().values(inserts)
                        await db_session.execute(stmt)

            await db_session.commit()
            rprint("Migration finished!")


@cli.command()
def run_task(path: str) -> None:
    """Type command that runs an async function."""
    asyncio.run(migrate(path))


if __name__ == "__main__":
    cli()
