"""Command line module."""

import asyncio

import bcrypt
import typer
from advanced_alchemy.base import BigIntAuditBase
from rich import print as rprint
from sqlalchemy import select

from app.classes.classes import Roles
from app.models.user import UserForm
from app.tables.tables import Users, config
from constants import DEFAULT_PASSWORD

app = typer.Typer()


async def create(fullname: str, username: str, email: str, role: Roles) -> None:
    """Create a new user.

    Example:
        python3 create.py "Super User" superadmin super@host.ru admin

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
            rprint(f"User {username} already exists or email is taken")
        else:
            new_user = data.model_dump() | {
                "passhash": bcrypt.hashpw(DEFAULT_PASSWORD.encode(), bcrypt.gensalt()),
            }
            db_session.add(Users(**new_user))
            await db_session.commit()
            rprint(f"User {username} created")


@app.command()
def run_task(fullname: str, username: str, email: str, role: Roles) -> None:
    """Type command that runs an async function."""
    asyncio.run(create(fullname, username, email, role))


if __name__ == "__main__":
    app()
