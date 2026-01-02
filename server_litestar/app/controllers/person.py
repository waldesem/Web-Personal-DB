"""Person routes."""

from pathlib import Path
from typing import Any

from litestar import Controller, Request, delete, get, post
from litestar.security.jwt import Token  # noqa: TC002
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: TC002

from app.classes.classes import Roles
from app.depends.auth import role_guard
from app.models.models import PersonIn, PersonOut, User
from app.tables.tables import Persons
from app.utils.utilities import create_destination, upload_resume


class PersonController(Controller):
    """Controller for person routes."""

    @get("/persons/{person_id:int}")
    async def get_person(
        self,
        person_id: int,
        db_session: AsyncSession,
    ) -> dict:
        """Retrieve an item from the database based on the provided item ID."""
        async with db_session.begin():
            person = await db_session.get(Persons, person_id)
            if not person.destination or not Path(person.destination).exists():
                person.destination = create_destination(person)
            return PersonOut.model_validate(person).model_dump()

    @post("/persons", guards=[role_guard], opt={"roles": Roles.user.value})
    async def post_person(
        self,
        data: PersonIn,
        request: Request[User, Token, Any],
        db_session: AsyncSession,
    ) -> dict:
        """Replace a record in persons table."""
        async with db_session.begin():
            cand_id, existed = upload_resume(data, request.user.id, db_session)
            return {"person_id": cand_id, "exists": existed}

    @delete(
        "/persons/{person_id:int}",
        guards=[role_guard],
        opt={"roles": Roles.user.value},
    )
    async def delete_person(self, person_id: int, db_session: AsyncSession) -> None:
        """Delete an item from the database with provided item name and item ID."""
        async with db_session.begin():
            person = await db_session.get(Persons, person_id)
            db_session.delete(person)
