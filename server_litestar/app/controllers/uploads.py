"""Upload a json to the server."""

from typing import Any

from litestar import Controller, Request, post
from litestar.exceptions import NotAuthorizedException
from litestar.security.jwt import Token
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.classes.classes import Roles
from app.middleware.auth import role_guard
from app.models.jsons import AnketaJson
from app.models.person import PersonIn, PersonResponse
from app.models.user import User
from app.tables.tables import (
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


class JsonController(Controller):
    """Controller for uploading a json."""

    @post(
        "/json",
        guards=[role_guard],
        opt={"role": (Roles.user.value, Roles.api.value)},
    )
    async def post_json_file(
        self,
        data: AnketaJson,
        db_session: AsyncSession,
        request: Request[User, Token, Any],
    ) -> PersonResponse:
        """Create a new person or updates an existing person from json.

        Args:
            data: AnketaJson.
            db_session: AsyncSession.
            request: Request.

        Returns:
            Response with status code 201.

        """
        stmt = select(Persons).where(
            Persons.surname == data.surname,
            Persons.firstname == data.firstname,
            Persons.patronymic == data.patronymic,
            Persons.birthday == data.birthday,
        )
        person = (await db_session.execute(stmt)).scalar_one_or_none()

        if person and (
            person.locked or (person.editable and person.user_id != request.user.id)
        ):
            raise NotAuthorizedException

        resume = PersonIn.model_validate(data, from_attributes=True).model_dump() | {
            "user_id": request.user.id,
        }

        if not person:
            person = Persons(**resume)
            db_session.add(person)
            await db_session.flush()
        else:
            for k, v in resume.items():
                if v:
                    setattr(person, k, v)

        # Сохранение дополнительной информации о кандидате в БД
        items_to_add = [
            Documents(
                digits=data.digits,
                series=data.series,
                issue=data.issue,
                agency=data.agency,
                person_id=person.id,
            ),
            Staffs(
                position=data.position,
                department=data.department,
                person_id=person.id,
            ),
            Addresses(
                view="Адрес проживания",
                address=data.valid_address,
                person_id=person.id,
            ),
            Addresses(
                view="Адрес регистрации",
                address=data.reg_address,
                person_id=person.id,
            ),
            Contacts(
                view="Телефон",
                contact=data.contact_phone,
                person_id=person.id,
            ),
            Contacts(
                view="Электронная почта",
                contact=data.email,
                person_id=person.id,
            ),
            *[
                Educations(**education.model_dump(), person_id=person.id)
                for education in data.education
            ],
            *[
                Workplaces(**workplace.model_dump(), person_id=person.id)
                for workplace in data.experience
            ],
            *[
                Previous(**prev.model_dump(), person_id=person.id)
                for prev in data.name_was_changed
            ],
            *[
                Affilations(
                    view="Участвует в деятельности коммерческих организаций",
                    organization=aff.organization,
                    inn=aff.inn,
                    person_id=person.id,
                )
                for aff in data.organizations
            ],
            *[
                Affilations(
                    view="Являлся государственным должностным лицом",
                    organization=aff.organization,
                    person_id=person.id,
                )
                for aff in data.state_organizations
            ],
            *[
                Affilations(
                    view="Связанные лица работают в госструктурах",
                    organization=aff.organization,
                    person_id=person.id,
                )
                for aff in data.related_organizations
            ],
            *[
                Affilations(
                    view="Являлся государственным/муниципальным служащим",
                    organization=aff.organization,
                    person_id=person.id,
                )
                for aff in data.public_organizations
            ],
        ]
        db_session.add_all(items_to_add)
        return PersonResponse(person_id=person.id)
