"""Person routes."""

import asyncio
from pathlib import Path
from typing import Any

from litestar import Controller, Request, delete, get, patch, post
from litestar.di import Provide
from litestar.exceptions import (
    NotAuthorizedException,
    NotFoundException,
    ValidationException,
)
from litestar.security.jwt import Token

from app.classes.classes import Roles
from app.middleware.auth import role_guard
from app.models.person import Person, PersonForm, PersonResp
from app.models.user import User
from app.tables.tables import Persons
from constants import BASE_PATH


async def person_depend(person_id: int) -> Persons:
    """Check person's."""
    person = await Persons.objects().get(Persons.id == person_id)
    if not person:
        raise NotFoundException
    return person


class PersonController(Controller):
    """Controller for person routes."""

    path = "/persons"

    @get("/{person_id:int}", dependencies={"person": Provide(person_depend)})
    async def get_person(
        self,
        person_id: int,  # noqa: ARG002
        person: Persons,
    ) -> Person:
        """Retrieve an item from the database based on the provided item ID.

        Args:
            person_id: Person ID for Dependency Injection.
            person: Persons.

        Returns:
            Response with status code 200 and serialized PersonOut.

        Raises:
            NotFoundException: If the person is not found.

        """
        if not person.destination:
            destination = Path(
                BASE_PATH,
                "Главный офис",
                person.surname[0],
                (
                    f"{person.id}-{person.surname} {person.firstname} {
                        person.patronymic or ''
                    }"
                ).rstrip(),
            )
            await asyncio.to_thread(destination.mkdir, parents=True, exist_ok=True)
            person.destination = str(destination)
            await person.save()
        return Person(**person.to_dict())

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
                target="constraint_surname_firstname_patronymic_birthday",
            )
            .returning(Persons.id)
        )
        if not person:
            raise ValidationException

        return PersonResp(person_id=person[0]["id"])

    @patch(
        "/{person_id:int}",
        guards=[role_guard],
        opt={"role": Roles.user.value},
        dependencies={"person": Provide(person_depend)},
    )
    async def patch_person(
        self,
        person_id: int,  # noqa: ARG002
        data: PersonForm,
        person: Persons,
        request: Request[User, Token, Any],
    ) -> None:
        """Create a new person or updates an existing person.

        Args:
            person_id: Person ID for Dependency Injection.
            data: PersonForm.
            person: Persons.
            request: Request.

        Returns:
            Response with status code 201.

        """
        if request.auth.sub != str(person.user_id):
            raise NotAuthorizedException

        resume = data.model_dump() | {"user_id": request.user.id}
        for k, v in resume.items():
            setattr(person, k, v)
        await person.save()

    @get(
        "/status/{person_id:int}",
        guards=[role_guard],
        opt={"role": Roles.user.value},
        dependencies={"person": Provide(person_depend)},
    )
    async def switch_status(
        self,
        person_id: int,  # noqa: ARG002
        person: Persons,
        request: Request[User, Token, Any],
    ) -> None:
        """Toggle the user status of a person.

        Args:
            person_id: Person ID for Dependency Injection.
            person: Persons.
            request: Request.

        Returns:
            Response with status code 200.

        """
        person.user_id = request.user.id
        await person.save()

    @delete(
        "/{person_id:int}",
        guards=[role_guard],
        opt={"role": Roles.user.value},
        dependencies={"person": Provide(person_depend)},
    )
    async def delete_person(
        self,
        person_id: int,  # noqa: ARG002
        person: Persons,
        request: Request[User, Token, Any],
    ) -> None:
        """Delete an item from the database with provided item name and item ID.

        Args:
            person_id: Person ID for Dependency Injection.
            person: Persons.
            request: Request[User, Token, Any]

        Returns:
            Response with status code 204.

        """
        if request.auth.sub != str(person.user_id):
            raise NotAuthorizedException

        await person.delete()
