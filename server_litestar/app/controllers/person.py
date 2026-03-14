"""Person routes."""

import asyncio
from pathlib import Path
from typing import Any

from litestar import Controller, Request, delete, get, patch, post
from litestar.exceptions import NotFoundException, ValidationException
from litestar.security.jwt import Token
from sqlalchemy import not_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.classes.classes import Roles
from app.middleware.auth import person_guard, role_guard
from app.models.person import PersonIn, PersonOut, PersonResponse
from app.models.user import User
from app.tables.tables import Persons
from constants import BASE_PATH


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
        if person and not person.deleted:
            if not person.destination and not person.protected:
                destination = Path(
                    BASE_PATH,
                    "Главный офис",
                    person.surname[0],
                    (
                        f"{person_id}-{person.surname} {person.firstname} {
                            person.patronymic or ''
                        }"
                    ).rstrip(),
                )
                await asyncio.to_thread(destination.mkdir, parents=True, exist_ok=True)
                person.destination = str(destination)
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
        stmt = select(Persons).where(
            Persons.surname == data.surname,
            Persons.firstname == data.firstname,
            Persons.patronymic == data.patronymic,
            Persons.birthday == data.birthday,
        )
        if person := (await db_session.execute(stmt)).scalar_one_or_none():
            raise ValidationException

        person = Persons(**data.model_dump() | {"user_id": request.user.id})
        db_session.add(person)
        return PersonResponse(person_id=person.id)

    @patch(
        "/{person_id:int}",
        guards=[role_guard, person_guard],
        opt={"role": Roles.user.value},
    )
    async def patch_person(
        self,
        person_id: int,
        data: PersonIn,
        request: Request[User, Token, Any],
        db_session: AsyncSession,
    ) -> None:
        """Create a new person or updates an existing person.

        Args:
            person_id: int,
            data: PersonIn.
            request: Request.
            db_session: AsyncSession.

        Returns:
            Response with status code 201.

        """
        resume = data.model_dump(exclude_none=True) | {"user_id": request.user.id}
        await db_session.execute(
            update(Persons).values(resume).where(Persons.id == person_id),
        )

    @get(
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
            .where(Persons.id == person_id, not_(Persons.protected and Persons.deleted))
            .values(editable=True, user_id=request.user.id),
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
        if not person or person.protected or person.deleted:
            raise NotFoundException
        person.deleted = True
