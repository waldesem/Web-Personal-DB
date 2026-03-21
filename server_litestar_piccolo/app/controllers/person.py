"""Person routes."""

import asyncio
from pathlib import Path
from typing import Any

from litestar import Controller, Request, delete, get, patch, post
from litestar.exceptions import NotFoundException, ValidationException
from litestar.security.jwt import Token

from app.classes.classes import Roles
from app.middleware.auth import person_guard, role_guard
from app.models.person import Person, PersonForm, PersonResp
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
    ) -> Person:
        """Retrieve an item from the database based on the provided item ID.

        Args:
            person_id: Person ID.

        Returns:
            Response with status code 200 and serialized PersonOut.

        Raises:
            NotFoundException: If the person is not found.

        """
        person = await Persons.objects().where(Persons.id == person_id).first()
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
                await person.save()
            return Person(**person.to_dict())
        raise NotFoundException

    @post("/", guards=[role_guard], opt={"role": Roles.user.value})
    async def post_person(
        self,
        data: PersonForm,
        request: Request[User, Token, Any],
    ) -> PersonResp:
        """Create a new person or updates an existing person.

        Args:
            data: PersonForm.
            request: Request.

        Returns:
            Response with status code 201.

        """
        person = (
            await Persons.insert(
                Persons(**data.model_dump(), user_id=request.user.id),
            )
            .on_conflict(
                action="DO NOTHING",
                target="constraint_persons_surname_firstname_patronymic_birthday",
            )
            .returning(Persons.id)
        )
        if not person:
            raise ValidationException

        return PersonResp(person_id=person[0]["id"])

    @patch(
        "/{person_id:int}",
        guards=[role_guard, person_guard],
        opt={"role": Roles.user.value},
    )
    async def patch_person(
        self,
        person_id: int,
        data: PersonForm,
        request: Request[User, Token, Any],
    ) -> None:
        """Create a new person or updates an existing person.

        Args:
            person_id: int,
            data: PersonForm.
            request: Request.

        Returns:
            Response with status code 201.

        """
        resume = data.model_dump() | {"user_id": request.user.id}
        await Persons.update(**resume).where(Persons.id == person_id)

    @get(
        "/status/{person_id:int}",
        guards=[role_guard],
        opt={"role": Roles.user.value},
    )
    async def switch_status(
        self,
        person_id: int,
        request: Request[User, Token, Any],
    ) -> None:
        """Toggle the editable status of a person.

        Args:
            person_id: Person ID.
            request: Request.

        Returns:
            Response with status code 200.

        """
        person = await Persons.objects().where(Persons.id == person_id).first()
        if not person or (person and (person.protected or person.deleted)):
            raise NotFoundException

        person.user_id = request.user.id
        person.editable = not person.editable
        await person.save()

    @delete(
        "/{person_id:int}",
        guards=[person_guard, role_guard],
        opt={"role": Roles.user.value},
    )
    async def delete_person(
        self,
        person_id: int,
    ) -> None:
        """Delete an item from the database with provided item name and item ID.

        Args:
            person_id: Person ID.

        Returns:
            Response with status code 204.

        """
        if person := await Persons.objects().where(Persons.id == person_id).first():
            person.deleted = True
            await person.save()
        else:
            raise NotFoundException
