"""Command line module."""

import asyncio

import typer
from advanced_alchemy.base import BigIntAuditBase
from rich import print  # noqa: A004
from sqlalchemy import select

from app.classes.classes import Roles
from app.models.models import UserForm
from app.tables.tables import Users, config

app = typer.Typer()


async def create(fullname: str, username: str, email: str, role: Roles) -> None:
    """Create a new user.

    Example:
        python3 user.py "Super User" superadmin super@host.ru admin

    """
    async with config.get_engine().begin() as conn:
        await conn.run_sync(BigIntAuditBase.metadata.create_all)

    data = UserForm(fullname=fullname, username=username, email=email, role=role)
    async with config.get_session() as db_session:
        user = (
            await db_session.execute(
                select(Users).filter(Users.username == data.username),
            )
        ).scalar()
        if user:
            print(f"User {username} already exists or email is taken")
        else:
            db_session.add(Users(**data.model_dump()))
            await db_session.commit()
            print(f"User {username} created")


@app.command()
def run_task(fullname: str, username: str, email: str, role: Roles) -> None:
    """Type command that runs an async function."""
    asyncio.run(create(fullname, username, email, role))


if __name__ == "__main__":
    app()
