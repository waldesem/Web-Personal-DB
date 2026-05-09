"""Upload a json to the server."""

from typing import Any

from litestar import Controller, Request, post
from litestar.exceptions import ValidationException
from litestar.security.jwt import Token

from app.classes.classes import Roles
from app.middleware.auth import role_guard
from app.models.jsons import AnketaJson
from app.models.person import PersonForm, PersonResp
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
    ) -> PersonResp:
        """Create a new person or updates an existing person from json.

        Args:
            data: AnketaJson.
            request: Request.

        Returns:
            Response with status code 201.

        """
        resume = PersonForm.model_validate(data, from_attributes=True)
        person = (
            await Persons.insert(
                Persons(**resume.model_dump(), user_id=request.user.id),
            )
            .on_conflict(
                action="DO NOTHING",
                target="constraint_surname_firstname_patronymic_birthday",
            )
            .returning(Persons.id)
        )
        if not person:
            raise ValidationException

        person_id = person[0]["id"]
        # Сохранение дополнительной информации о кандидате в БД
        await Documents.insert(
            Documents(
                digits=data.digits,
                series=data.series,
                issue=data.issue,
                agency=data.agency,
                person_id=person_id,
            ),
        )
        await Staffs.insert(
            Staffs(
                position=data.position,
                department=data.department,
                person_id=person_id,
            ),
        )
        await Addresses.insert(
            Addresses(
                view="Адрес проживания",
                address=data.valid_address,
                person_id=person_id,
            ),
            Addresses(
                view="Адрес регистрации",
                address=data.reg_address,
                person_id=person_id,
            ),
        )
        await Contacts.insert(
            Contacts(
                view="Телефон",
                contact=data.contact_phone,
                person_id=person_id,
            ),
            Contacts(
                view="Электронная почта",
                contact=data.email,
                person_id=person_id,
            ),
        )
        if data.education:
            await Educations.insert(
                *[
                    Educations(**education.model_dump(), person_id=person_id)
                    for education in data.education
                ],
            )
        if data.experience:
            await Workplaces.insert(
                *[
                    Workplaces(**workplace.model_dump(), person_id=person_id)
                    for workplace in data.experience
                ],
            )
        if data.name_was_changed:
            await Previous.insert(
                *[
                    Previous(**prev.model_dump(), person_id=person_id)
                    for prev in data.name_was_changed
                ],
            )
        if data.organizations:
            await Affilations.insert(
                *[
                    Affilations(
                        view=aff.view,
                        organization=aff.organization,
                        inn=aff.inn,
                        person_id=person_id,
                    )
                    for aff in data.organizations
                ],
            )
        return PersonResp(person_id=person_id)
