"""Migration from sqlite to postgresql."""

import asyncio
from functools import wraps
from typing import TYPE_CHECKING

import click
from piccolo.conf.apps import table_finder
from piccolo.table import Table, create_db_tables, drop_db_tables
from rich import print as rprint

if TYPE_CHECKING:
    from collections.abc import Callable


def async_cmd(f: Callable) -> Callable:
    """Async command decorator."""

    @wraps(f)
    def wrapper(*args: tuple, **kwargs: dict) -> None:
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.command()
@async_cmd
async def create() -> None:
    """MIgrate data from sqlite to postgresql.

    Example:
        python3 cli_create.py

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

    await Table.raw(
        """CREATE INDEX idx_persons_search_active
            ON persons(surname, firstname, patronymic)
            WHERE NOT deleted;
        """,
    )

    rprint("DB tables creations finished!")


if __name__ == "__main__":
    create()
