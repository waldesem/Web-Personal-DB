"""Upload a json to the server."""

from typing import Any

from litestar import Controller, Request, post
from litestar.security.jwt import Token
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
    Previous,
    Staffs,
    Workplaces,
)
from app.utilities.utils import upload_resume


class JsonController(Controller):
    """Controller for uploading a json."""

    @post("/json", guards=[role_guard], opt={"role": Roles.user.value})
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
        resume = PersonIn(**data.model_dump())
        # Загрузка резюме в БД
        cand_id, existed = await upload_resume(resume, request.user.id, db_session)

        # Сохранение дополнительной информации о кандидате в БД
        if cand_id:
            items_to_add = [
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
                    Educations(**education.model_dump(), person_id=cand_id)
                    for education in data.education
                ],
                *[
                    Workplaces(**workplace.model_dump(), person_id=cand_id)
                    for workplace in data.experience
                ],
                *[
                    Previous(**prev.model_dump(), person_id=cand_id)
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
            db_session.add_all(items_to_add)
        return PersonResponse(person_id=cand_id, exists=existed)
