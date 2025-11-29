"""Route routes."""

from __future__ import annotations

import json
from typing import Any

from flask import Blueprint, g, request
from sqlalchemy import Row, Sequence, func, select, text

from app import db
from app.classes.classes import Roles
from app.decorators.depend import auth_required
from app.decorators.pydantify import serialize, validize
from app.models.models import (
    AnketaJson,
    Candidates,
    Index,
    PersonIn,
    ResumeResponse,
)
from app.tables.tables import (
    Addresses,
    Affilations,
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

bp = Blueprint("route", __name__)


@bp.get("/candidates")
@serialize(Candidates, orm=True, many=True)
@validize()
@auth_required()
def get_index(json_query: Index) -> tuple[Sequence[Row[Any]], int]:
    """Retrieve a paginated list of persons from the database."""
    stmt = select(
        db.metatables["persons"],
        Users.fullname.label("username"),
        select(func.count(Persons.id)).scalar_subquery().label("total"),
    )
    if json_query.search:
        stmt = stmt.filter(Persons.surname == json_query.search[0])
        if len(json_query.search) > 1:
            stmt = stmt.filter(Persons.firstname == json_query.search[1])
            if len(json_query.search) > 2:
                stmt = stmt.filter(Persons.patronymic == json_query.search[2])
    # Пагинация списка кандидатов
    result = db.session.execute(
        stmt.filter(Users.id == Persons.user_id)
        .order_by(Persons.id.desc())
        .offset((json_query.page - 1) * json_query.per_page)
        .limit(json_query.per_page),
    ).all()
    return result, 200


@bp.get("/self/<int:person_id>")
@serialize()
@validize()
@auth_required(Roles.user.value)
def switch_status(person_id: int) -> tuple[dict, int]:
    """Toggle the editable status of a person."""
    stmt = text(
        "UPDATE persons SET user_id = :user_id, editable = NOT editable WHERE id = :id",
    )
    db.session.execute(stmt, {"user_id": g.user.id, "id": person_id})
    db.session.commit()
    return {"message": "success"}, 201


@bp.post("/json")
@serialize(ResumeResponse)
@validize()
@auth_required(Roles.user.value)
def post_json_file() -> tuple[dict, int]:
    """Create a new person or updates an existing person from file."""
    # Чтение файла JSON и создание объектов классов для сохранения в БД
    if not (file := request.data):
        return {"person_id": None, "exists": False}, 200
    try:
        json_data = json.loads(file)
        anketa = AnketaJson(**json_data)
    except (TypeError, json.JSONDecodeError):
        return {"person_id": None, "exists": False}, 200
    result = post_json(anketa)
    return result, 201 if result.get("person_id") else 200


def post_json(anketa: AnketaJson) -> dict:
    """Create a new person or updates an existing person based on the provided data."""
    resume = PersonIn(**anketa.dict(exclude_none=True))
    # Загрузка резюме в БД
    person_id, existed = upload_resume(resume, g.user.id)

    # Сохранение дополнительной информации о кандидате в БД
    if person_id:
        items = upload_items(anketa, person_id)
        db.session.bulk_save_objects(items)
        db.session.commit()
    return {"person_id": person_id, "exists": existed}


def upload_items(anketa: AnketaJson, person_id: int) -> list:
    """Organze additional information about a person for database uploads."""
    return [
        Documents(
            digits=anketa.digits,
            series=anketa.series,
            issue=anketa.issue,
            agency=anketa.agency,
            person_id=person_id,
        ),
        Staffs(
            position=anketa.position,
            department=anketa.department,
            person_id=person_id,
        ),
        Addresses(
            view="Адрес проживания",
            address=anketa.valid_address,
            person_id=person_id,
        ),
        Addresses(
            view="Адрес регистрации",
            address=anketa.reg_address,
            person_id=person_id,
        ),
        Contacts(
            view="Телефон",
            contact=anketa.contact_phone,
            person_id=person_id,
        ),
        Contacts(
            view="Электронная почта",
            contact=anketa.email,
            person_id=person_id,
        ),
        *[
            Educations(**education.dict(), person_id=person_id)
            for education in anketa.education
        ],
        *[
            Workplaces(**workplace.dict(), person_id=person_id)
            for workplace in anketa.experience
        ],
        *[
            Previous(**prev.dict(), person_id=person_id)
            for prev in anketa.name_was_changed
        ],
        *[
            Affilations(
                view="Участвует в деятельности коммерческих организаций",
                organization=aff.organization,
                inn=aff.inn,
                person_id=person_id,
            )
            for aff in anketa.organizations
        ],
        *[
            Affilations(
                view="Являлся государственным должностным лицом",
                organization=aff.organization,
                person_id=person_id,
            )
            for aff in anketa.state_organizations
        ],
        *[
            Affilations(
                view="Связанные лица работают в государственных организациях",
                organization=aff.organization,
                person_id=person_id,
            )
            for aff in anketa.related_organizations
        ],
        *[
            Affilations(
                view="Являлся государственным или муниципальным служащим",
                organization=aff.organization,
                person_id=person_id,
            )
            for aff in anketa.public_organizations
        ],
    ]
