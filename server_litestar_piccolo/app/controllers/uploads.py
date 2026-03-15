"""Upload a json to the server."""

from typing import Any

from litestar import Controller, Request, post
from litestar.exceptions import NotFoundException
from litestar.security.jwt import Token

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
        request: Request[User, Token, Any],
    ) -> PersonResponse:
        """Create a new person or updates an existing person from json.

        Args:
            data: AnketaJson.
            request: Request.

        Returns:
            Response with status code 201.

        """
        person = await (
            Persons.objects()
            .where(
                Persons.surname == data.surname
                and Persons.firstname == data.firstname
                and Persons.patronymic == data.patronymic
                and Persons.birthday == data.birthday,
            )
            .first()
        )

        if person:
            raise NotFoundException

        resume = PersonIn.model_validate(data, from_attributes=True).model_dump() | {
            "user_id": request.user.id,
        }

        person = Persons(resume)
        await person.save()

        # Сохранение дополнительной информации о кандидате в БД
        await Documents.insert(
            Documents(
                digits=data.digits,
                series=data.series,
                issue=data.issue,
                agency=data.agency,
                person_id=person.id,
            ),
        )
        await Staffs.insert(
            Staffs(
                position=data.position,
                department=data.department,
                person_id=person.id,
            ),
        )
        await Addresses.insert(
            Addresses(
                view="Адрес проживания",
                address=data.valid_address,
                person_id=person.id,
            ),
        )
        await Addresses.insert(
            Addresses(
                view="Адрес регистрации",
                address=data.reg_address,
                person_id=person.id,
            ),
        )
        await Contacts.insert(
            Contacts(
                view="Телефон",
                contact=data.contact_phone,
                person_id=person.id,
            ),
        )
        await Contacts.insert(
            Contacts(
                view="Электронная почта",
                contact=data.email,
                person_id=person.id,
            ),
        )
        [
            await Educations.insert(
                Educations(**education.model_dump(), person_id=person.id),
            )
            for education in data.education
        ]
        [
            await Workplaces.insert(
                Workplaces(**workplace.model_dump(), person_id=person.id),
            )
            for workplace in data.experience
        ]
        [
            await Previous.insert(Previous(**prev.model_dump(), person_id=person.id))
            for prev in data.name_was_changed
        ]
        [
            await Affilations.insert(
                Affilations(
                    view="Участвует в деятельности коммерческих организаций",
                    organization=aff.organization,
                    inn=aff.inn,
                    person_id=person.id,
                ),
            )
            for aff in data.organizations
        ]
        [
            await Affilations.insert(
                Affilations(
                    view="Являлся государственным должностным лицом",
                    organization=aff.organization,
                    person_id=person.id,
                ),
            )
            for aff in data.state_organizations
        ]
        [
            await Affilations.insert(
                Affilations(
                    view="Связанные лица работают в госструктурах",
                    organization=aff.organization,
                    person_id=person.id,
                ),
            )
            for aff in data.related_organizations
        ]
        (
            [
                await Affilations.insert(
                    Affilations(
                        view="Являлся государственным/муниципальным служащим",
                        organization=aff.organization,
                        person_id=person.id,
                    ),
                )
                for aff in data.public_organizations
            ],
        )
        return PersonResponse(person_id=person.id)
