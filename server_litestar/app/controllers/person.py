"""Person routes."""

from typing import Any

from litestar import Controller, Request, delete, get, patch, post
from litestar.exceptions import NotFoundException
from litestar.security.jwt import Token
from sqlalchemy import not_, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.classes.classes import Roles
from app.middleware.auth import role_guard
from app.models.person import PersonIn, PersonOut, PersonResponse
from app.models.user import User
from app.tables.tables import Persons
from app.utilities.person import create_destination, upload_resume


class PersonController(Controller):
    """Controller for person routes."""

    path = "/persons"

    @get("/{person_id:int}")
    async def get_person(
        self,
        person_id: int,
        db_session: AsyncSession,
    ) -> PersonOut:
        """Retrieve an item from the database based on the provided item ID.

        Args:
            person_id: Person ID.
            db_session: AsyncSession.

        Returns:
            Response with status code 200 and serialized PersonOut.

        Raises:
            NotFoundException: If the person is not found.

        """
        person = await db_session.get(Persons, person_id)
        if person:
            if not person.destination:
                person.destination = await create_destination(
                    person.id,
                    person.surname,
                    person.firstname,
                    person.patronymic,
                )
            return PersonOut.model_validate(person, from_attributes=True)
        raise NotFoundException

    @post("/", guards=[role_guard], opt={"role": Roles.user.value})
    async def post_person(
        self,
        data: PersonIn,
        request: Request[User, Token, Any],
        db_session: AsyncSession,
    ) -> PersonResponse:
        """Create a new person or updates an existing person.

        Args:
            data: PersonIn.
            request: Request.
            db_session: AsyncSession.

        Returns:
            Response with status code 201.

        """
        cand_id, existed = await upload_resume(data, request.user.id, db_session)
        return PersonResponse(person_id=cand_id, exists=existed)

    @patch(
        "/status/{person_id:int}",
        guards=[role_guard],
        opt={"role": Roles.user.value},
    )
    async def switch_status(
        self,
        person_id: int,
        request: Request[User, Token, Any],
        db_session: AsyncSession,
    ) -> None:
        """Toggle the editable status of a person.

        Args:
            person_id: Person ID.
            request: Request.
            db_session: AsyncSession.

        Returns:
            Response with status code 200.

        """
        await db_session.execute(
            update(Persons)
            .where(Persons.id == person_id)
            .values(editable=not_(Persons.editable), user_id=request.user.id),
        )

    @delete(
        "/{person_id:int}",
        guards=[role_guard],
        opt={"role": Roles.user.value},
    )
    async def delete_person(
        self,
        person_id: int,
        db_session: AsyncSession,
    ) -> None:
        """Delete an item from the database with provided item name and item ID.

        Args:
            person_id: Person ID.
            db_session: AsyncSession.

        Returns:
            Response with status code 204.

        """
        person = await db_session.get(Persons, person_id)
        if not person:
            raise NotFoundException
        await db_session.delete(person)
