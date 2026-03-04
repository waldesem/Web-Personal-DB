"""Person routes."""

from pathlib import Path
from typing import Any

from litestar import Controller, Request, delete, get, patch, post
from litestar.exceptions import NotFoundException
from litestar.security.jwt import Token
from sqlalchemy import not_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.middleware.auth import role_guard
from app.structures.classes import Roles
from app.structures.models import AnketaJson, Person, PersonResponse, User
from app.structures.tables import (
    Addresses,
    Affilations,
    Contacts,
    Documents,
    Educations,
    Persons,
    Previous,
    Staffs,
    Workplaces,
)
from constants import BASE_PATH


class PersonController(Controller):
    """Controller for person routes."""

    path = "/persons"

    @classmethod
    def create_destination(cls, person: Persons) -> str:
        """Create destination."""
        destination = Path(
            BASE_PATH,
            "Главный офис",
            person.surname[0],
            (
                f"{person.id}-{person.surname} {person.firstname} {person.patronymic or ''}"  # noqa: E501
            ).rstrip(),
        )
        destination.mkdir(parents=True, exist_ok=True)
        return str(destination)

    @classmethod
    async def upload_resume(
        cls,
        cand: Person,
        user_id: int | None,
        db_session: AsyncSession,
    ) -> tuple[int | None, bool]:
        """Upload a resume to the database."""
        person = (
            await db_session.execute(
                select(Persons).where(
                    Persons.surname == cand.surname,
                    Persons.firstname == cand.firstname,
                    Persons.patronymic == cand.patronymic,
                    Persons.birthday == cand.birthday,
                ),
            )
        ).scalar_one_or_none()

        if person and person.editable and user_id and person.user_id == user_id:
            return None, True

        resume = cand.model_dump(exclude_none=True) | {"user_id": user_id}

        if not person:
            person = Persons(**resume)
            db_session.add(person)
            await db_session.flush()
            person.destination = cls.create_destination(person)
            return person.id, False

        if not person.destination:
            resume["destination"] = cls.create_destination(person)
        for k, v in resume.items():
            setattr(person, k, v)
        return person.id, True

    @get("/{person_id:int}")
    async def get_person(
        self,
        person_id: int,
        db_session: AsyncSession,
    ) -> Person:
        """Retrieve an item from the database based on the provided item ID."""
        person = await db_session.get(Persons, person_id)
        if person:
            if not person.destination:
                person.destination = self.create_destination(person)
            return Person.model_validate(person, from_attributes=True)
        raise NotFoundException

    @post("/", guards=[role_guard], opt={"role": Roles.user.value})
    async def post_person(
        self,
        data: Person,
        request: Request[User, Token, Any],
        db_session: AsyncSession,
    ) -> PersonResponse:
        """Replace a record in persons table."""
        cand_id, existed = await self.upload_resume(data, request.user.id, db_session)
        return PersonResponse(person_id=cand_id, exists=existed)

    @patch(
        "/status/{person_id:int}",
        guards=[role_guard],
        opt={"role": Roles.user.value},
        status_code=201,
    )
    async def switch_status(
        self,
        person_id: int,
        request: Request[User, Token, Any],
        db_session: AsyncSession,
    ) -> None:
        """Toggle the editable status of a person."""
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
    async def delete_person(self, person_id: int, db_session: AsyncSession) -> None:
        """Delete an item from the database with provided item name and item ID."""
        person = await db_session.get(Persons, person_id)
        db_session.delete(person)

    @post("/json", guards=[role_guard], opt={"role": Roles.user.value})
    async def post_json_file(
        self,
        data: AnketaJson,
        db_session: AsyncSession,
        request: Request[User, Token, Any],
    ) -> dict:
        """Create a new person or updates an existing person from file."""
        resume = Person(**data.model_dump(exclude={"id", "created_at", "updated_at"}))
        # Загрузка резюме в БД
        cand_id, existed = await self.upload_resume(resume, request.user.id, db_session)

        # Сохранение дополнительной информации о кандидате в БД
        if cand_id:
            items = [
                Documents(
                    digits=data.digits,
                    series=data.series,
                    issue=data.issue,
                    agency=data.agency,
                    person_id=cand_id,
                ),
                Staffs(
                    position=data.position,
                    department=data.department,
                    person_id=cand_id,
                ),
                Addresses(
                    view="Адрес проживания",
                    address=data.valid_address,
                    person_id=cand_id,
                ),
                Addresses(
                    view="Адрес регистрации",
                    address=data.reg_address,
                    person_id=cand_id,
                ),
                Contacts(
                    view="Телефон",
                    contact=data.contact_phone,
                    person_id=cand_id,
                ),
                Contacts(
                    view="Электронная почта",
                    contact=data.email,
                    person_id=cand_id,
                ),
                *[
                    Educations(
                        **education.model_dump(
                            exclude={"id", "item", "created_at", "updated_at"},
                        ),
                        person_id=cand_id,
                    )
                    for education in data.education
                ],
                *[
                    Workplaces(
                        **workplace.model_dump(
                            exclude={"id", "item", "created_at", "updated_at"},
                        ),
                        person_id=cand_id,
                    )
                    for workplace in data.experience
                ],
                *[
                    Previous(
                        **prev.model_dump(
                            exclude={"id", "item", "created_at", "updated_at"},
                        ),
                        person_id=cand_id,
                    )
                    for prev in data.name_was_changed
                ],
                *[
                    Affilations(
                        view="Участвует в деятельности коммерческих организаций",
                        organization=aff.organization,
                        inn=aff.inn,
                        person_id=cand_id,
                    )
                    for aff in data.organizations
                ],
                *[
                    Affilations(
                        view="Являлся государственным должностным лицом",
                        organization=aff.organization,
                        person_id=cand_id,
                    )
                    for aff in data.state_organizations
                ],
                *[
                    Affilations(
                        view="Связанные лица работают в госструктурах",
                        organization=aff.organization,
                        person_id=cand_id,
                    )
                    for aff in data.related_organizations
                ],
                *[
                    Affilations(
                        view="Являлся государственным/муниципальным служащим",
                        organization=aff.organization,
                        person_id=cand_id,
                    )
                    for aff in data.public_organizations
                ],
            ]
            db_session.add_all(items)
        return {"person_id": cand_id, "exists": existed}
