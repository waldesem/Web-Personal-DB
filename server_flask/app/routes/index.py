"""Route routes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from flask import Blueprint, g, request
from sqlalchemy import Row, Sequence, desc, func, select, text

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
from app.utils.utilities import check_filename, upload_resume

bp = Blueprint("route", __name__)


@bp.get("/candidates")
@serialize(Candidates, orm=True, many=True)
@validize()
@auth_required()
def get_index(json_query: Index) -> tuple[Sequence[Row[Any]], int]:
    """Retrieve a paginated list of persons from the database."""
    stmt = select(
        Persons.id,
        Persons.birthday,
        Persons.surname,
        Persons.firstname,
        Persons.patronymic,
        Persons.birthplace,
        Persons.citizenship,
        Persons.dual,
        Persons.snils,
        Persons.inn,
        Persons.marital,
        Persons.addition,
        Persons.destination,
        Persons.editable,
        Persons.created,
        Persons.user_id,
        Users.fullname.label("username"),
        func.count().over().label("total"),
    ).filter(
        Users.id == Persons.user_id,
    )
    if json_query.search:
        stmt = stmt.filter(Persons.surname == json_query.search[0])
        if len(json_query.search) > 1:
            stmt = stmt.filter(Persons.surname == json_query.search[1])
            if len(json_query.search) > 2:
                stmt = stmt.filter(Persons.surname == json_query.search[2])
    # Пагинация списка кандидатов
    result = db.session.execute(
        stmt.order_by(desc(Persons.id)).slice(
            (json_query.page - 1) * json_query.per_page,
            json_query.per_page * json_query.page,
        ),
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


@bp.post("/files/<int:person_id>")
@serialize()
@validize()
@auth_required(Roles.user.value)
def post_files(person_id: int) -> tuple[dict, int]:
    """Upload files to the server."""
    if (person := db.session.get(Persons, person_id)) and person.destination:
        subfolder = Path(
            person.destination,
            datetime.now().strftime("%d-%m-%Y %H-%M-%S"),
        )
        subfolder.mkdir(parents=True, exist_ok=True)
        for data in request.files.getlist("file"):
            if secure_filename := check_filename(data.filename):
                file_path = Path(subfolder, secure_filename)
                if not file_path.is_file():
                    data.save(file_path)
        return {"message": "success"}, 201
    return {"message": "error"}, 200


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
        upload_items(anketa, person_id)
    return {"person_id": person_id, "exists": existed}


def upload_items(anketa: AnketaJson, person_id: int) -> None:
    """Save additional information about a person in the database."""
    items = [
        Documents(
            digits=anketa.digits,
            series=anketa.series,
            issue=anketa.issue,
            agency=anketa.agency,
        ),
        Staffs(position=anketa.position, department=anketa.department),
        Addresses(view="Адрес проживания", address=anketa.valid_address),
        Addresses(view="Адрес регистрации", address=anketa.reg_address),
        Contacts(view="Телефон", contact=anketa.contact_phone),
        Contacts(view="Электронная почта", contact=anketa.email),
        *[Educations(**edu.dict()) for edu in anketa.education],
        *[Workplaces(**work.dict()) for work in anketa.experience],
        *[Previous(**prev.dict()) for prev in anketa.name_was_changed],
        *[
            Affilations(
                view="Участвует в деятельности коммерческих организаций",
                organization=aff.organization,
                inn=aff.inn,
            )
            for aff in anketa.organizations
        ],
        *[
            Affilations(
                view="Являлся государственным должностным лицом",
                organization=aff.organization,
            )
            for aff in anketa.state_organizations
        ],
        *[
            Affilations(
                view="Связанные лица работают в государственных организациях",
                organization=aff.organization,
            )
            for aff in anketa.related_organizations
        ],
        *[
            Affilations(
                view="Являлся государственным или муниципальным служащим",
                organization=aff.organization,
            )
            for aff in anketa.public_organizations
        ],
    ]
    # Добавляем аттибуты person_id и user_id к объектам
    for item in items:
        if item:
            item.person_id = person_id

    db.session.bulk_save_objects(items)
    db.session.commit()
