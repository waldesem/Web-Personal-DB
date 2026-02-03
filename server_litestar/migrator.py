"""Migration from sqlite to postgresql."""

import asyncio
import sqlite3

import typer
from rich import print  # noqa: A004

from app.classes.classes import ItemCategory
from app.models.models import ItemModel, PersonOut, User
from app.tables.tables import Persons, Users, config

cli = typer.Typer()

tables = config.metadata.tables


def make_dicts(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
    """Convert SQL row to dictionary."""
    return {cursor.description[idx][0]: value for idx, value in enumerate(row)}


async def migrate(path: str) -> None:
    """MIgrate data from sqlite to postgresql.

    Example:
        python3 migrator.py 'database.db'

    """
    async with config.get_engine().begin() as conn:
        await conn.run_sync(config.metadata.create_all)

    with sqlite3.connect(path) as conn:
        async with config.get_session() as db_session:
            conn.row_factory = make_dicts
            cur = conn.cursor()
            users: list[dict] = cur.execute("SELECT * FROM users").fetchall()
            new_users = [Users(**User(**user).model_dump()) for user in users]
            await db_session.add_all(new_users)

            persons: list[dict] = cur.execute("SELECT * FROM persons").fetchall()
            for person in persons:
                person["created_at"] = person.pop("created", None)
                valid_person = PersonOut(person)
                new_person = Persons(**valid_person.model_dump(exclude={"id"}))
                db_session.add(new_person)
                await db_session.flush()

                for table in ItemCategory:
                    items: list[dict] = cur.execute(
                        f"SELECT * FROM {table.value} WHERE person_id = ?",  # noqa: S608
                        (person["id"],),
                    ).fetchall()

                    insertions = []
                    for data in items:
                        data["item"] = table.value
                        data["created_at"] = data.pop("created", None)
                        data["person_id"] = new_person.id
                        new_data = ItemModel(**data).model_dump(exclude={"id", "item"})
                        insertions.append(new_data)

                    if insertions:
                        stmt = tables[table.value].insert().values(insertions)
                        await db_session.execute(stmt)

            await db_session.commit()
            print("Migration fifnished!")


@cli.command()
def run_task(path: str) -> None:
    """Type command that runs an async function."""
    asyncio.run(migrate(path))


if __name__ == "__main__":
    cli()
