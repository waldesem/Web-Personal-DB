"""Command line module."""

import bcrypt
import click
from advanced_alchemy.base import BigIntAuditBase
from rich import print as rprint
from sqlalchemy import select

from app.classes.classes import Roles
from app.models.user import UserForm
from app.tables.tables import Users, config
from app.utilities.utils import async_cmd
from constants import DEFAULT_PASSWORD


@click.command()
@click.argument("fullname")
@click.argument("username")
@click.argument("email")
@click.argument("role", type=click.Choice(Roles.__members__))
@async_cmd
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


if __name__ == "__main__":
    create()
