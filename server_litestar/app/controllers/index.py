"""Route routes."""

from __future__ import annotations

from typing import Any

from litestar import Request, get, post
from litestar.security.jwt import Token
from sqlalchemy import func, not_, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.classes.classes import Roles
from app.depends.auth import role_guard
from app.models.models import AnketaJson, Candidates, Index, PersonIn, User
from app.tables.tables import (
    Addresses,
    Affilations,
    Base,
    Contacts,
    Documents,
    Educations,
    Persons,
    Previous,
    Staffs,
    Users,
    Workplaces,
)
from app.utils.utilities import upload_resume


@get("/candidates")
async def get_index(query: Index, db_session: AsyncSession) -> list[Candidates]:
    """Retrieve a paginated list of persons from the database."""
    async with db_session.begin():
        stmt = select(
            Base.metadata.tables["persons"],
            Users.fullname.label("username"),
            func.count().over().label("total"),
        )
        if query.search:
            stmt = stmt.filter(Persons.surname == query.search[0])
            if len(query.search) > 1:
                stmt = stmt.filter(Persons.firstname == query.search[1])
                if len(query.search) > 2:
                    stmt = stmt.filter(Persons.patronymic == query.search[2])
        # Пагинация списка кандидатов
        candidates = (
            await db_session.execute(
                stmt.filter(Users.id == Persons.user_id)
                .order_by(Persons.id.desc())
                .offset((query.page) * query.per_page)
                .limit(query.per_page),
            )
        ).all()
        return [Candidates.model_validate(cand) for cand in candidates]


@get("/self/{person_id:int}", guards=[role_guard], opt={"roles": Roles.user.value})
async def switch_status(
    person_id: int,
    request: Request[User, Token, Any],
    db_session: AsyncSession,
) -> dict:
    """Toggle the editable status of a person."""
    async with db_session.begin():
        try:
            await db_session.execute(
                update(Persons)
                .where(Persons.id == person_id)
                .values(editable=not_(Persons.editable), user_id=request.user.id),
            )
        except SQLAlchemyError:
            request.logger.exception("Database error")
            return {"message": "error"}
        else:
            return {"message": "success"}


@post("/json", guards=[role_guard], opt={"roles": Roles.user.value})
async def post_json_file(
    data: AnketaJson,
    db_session: AsyncSession,
    request: Request[User, Token, Any],
) -> dict:
    """Create a new person or updates an existing person from file."""
    resume = PersonIn(**data.model_dump(exclude_none=True))
    # Загрузка резюме в БД
    person_id, existed = await upload_resume(resume, request.user.id, db_session)

    # Сохранение дополнительной информации о кандидате в БД
    if person_id:
        async with db_session.begin():
            items = [
                Documents(
                    digits=data.digits,
                    series=data.series,
                    issue=data.issue,
                    agency=data.agency,
                    person_id=person_id,
                ),
                Staffs(
                    position=data.position,
                    department=data.department,
                    person_id=person_id,
                ),
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
                *[
                    Educations(**education.model_dump(), person_id=person_id)
                    for education in data.education
                ],
                *[
                    Workplaces(**workplace.model_dump(), person_id=person_id)
                    for workplace in data.experience
                ],
                *[
                    Previous(**prev.model_dump(), person_id=person_id)
                    for prev in data.name_was_changed
                ],
                *[
                    Affilations(
                        view="Участвует в деятельности коммерческих организаций",
                        organization=aff.organization,
                        inn=aff.inn,
                        person_id=person_id,
                    )
                    for aff in data.organizations
                ],
                *[
                    Affilations(
                        view="Являлся государственным должностным лицом",
                        organization=aff.organization,
                        person_id=person_id,
                    )
                    for aff in data.state_organizations
                ],
                *[
                    Affilations(
                        view="Связанные лица работают в государственных организациях",
                        organization=aff.organization,
                        person_id=person_id,
                    )
                    for aff in data.related_organizations
                ],
                *[
                    Affilations(
                        view="Являлся государственным или муниципальным служащим",
                        organization=aff.organization,
                        person_id=person_id,
                    )
                    for aff in data.public_organizations
                ],
            ]
            db_session.add_all(items)
    return {"person_id": person_id, "exists": existed}
