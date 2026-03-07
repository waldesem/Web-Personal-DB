"""Migration from sqlite to postgresql."""

import asyncio
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

import typer
from advanced_alchemy.base import BigIntAuditBase
from rich import print as rprint

from app.structures.classes import ItemCategory
from app.structures.models import ItemModelOut, PersonOut, User
from app.structures.tables import Persons, Users, config

cli = typer.Typer()

tables = BigIntAuditBase.metadata.tables


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
                new_user = User(
                    **dict(user),
                    created_at=datetime.now(UTC),
                    updated_at=datetime.now(UTC),
                ).model_dump(exclude={"id"})
                new_users.append(Users(**new_user))
            db_session.add_all(new_users)

            persons = cur.execute("SELECT * FROM persons").fetchall()
            for person in persons:
                persona = dict(person)
                persona["created_at"] = persona["updated_at"] = persona.pop("created")
                new_person = PersonOut(**persona).model_dump(
                    exclude={"id"},
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
                                exclude={"item"},
                            )
                            new_data["person_id"] = new_person.id
                            inserts.append(new_data)

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
