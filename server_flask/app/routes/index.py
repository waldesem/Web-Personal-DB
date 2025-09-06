"""Route routes."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from flask import Blueprint, current_app, g, request
from pydantic import ValidationError
from sqlalchemy import desc, func, select
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.classes.classes import Roles
from app.decorators.depend import auth_required
from app.decorators.validize import pydantify
from app.models.models import (
    AnketaJson,
    BaseResponse,
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
from app.utils.utilities import check_filename, create_destination, upload_resume

bp = Blueprint("route", __name__)


@bp.get("/persons")
@pydantify(Candidates, orm=True, many=True)
@auth_required()
def get_index(json_query: Index) -> tuple[list[Persons], int]:
    """Retrieve a paginated list of persons from the database."""
    try:
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
            search = json_query.search.upper().split(maxsplit=3)[:3]
            stmt = stmt.where(
                Persons.surname == search[0],
                Persons.firstname == search[1] if len(search) > 1 else True,
                Persons.patronymic == search[2] if len(search) > 2 else True,
            )
        # Пагинация списка кандидатов
        result = db.session.execute(
            stmt.order_by(desc(Persons.id)).slice(
                (json_query.page - 1) * json_query.per_page,
                json_query.per_page * json_query.page,
            ),
        ).all()

    except SQLAlchemyError:
        current_app.logger.exception("SQL Error")
        return [], 200
    else:
        return result, 200


@bp.get("/self/<int:person_id>")
@pydantify()
@auth_required(Roles.user.value)
def change_self_id(person_id: int) -> tuple[dict, int]:
    """Toggle the editable status of a person."""
    if person := db.session.get(Persons, person_id):
        try:
            if not person.destination or not Path(person.destination).is_dir():
                person.destination = create_destination(person)
            if person.user_id != g.user.id:
                if person.editable:
                    person.editable = False
                else:
                    person.user_id = g.user.id
                    person.editable = True
            else:
                person.editable = not person.editable
            db.session.commit()
        except SQLAlchemyError:
            current_app.logger.exception("Exception in change_self_id")
            return {"message": "error"}, 200
        else:
            return {"message": "success"}, 201
    return {"message": "error"}, 200


@bp.post("/files/<int:person_id>")
@pydantify()
@auth_required(Roles.user.value)
def post_files(person_id: int) -> tuple[dict, int]:
    """Upload a file to the server."""
    file_data = request.files.getlist("file")
    if person := db.session.get(Persons, person_id):
        try:
            subfolder = Path(
                person.destination,
                datetime.now().strftime("%d-%m-%Y %H-%M-%S"),
            )
            subfolder.mkdir(parents=True, exist_ok=True)

            for data in file_data:
                secure_filename = check_filename(data.filename)
                if secure_filename:
                    file_path = Path(subfolder, secure_filename)
                    if not file_path.is_file():
                        data.save(file_path)
        except (TypeError, ValueError, AttributeError):
            current_app.logger.exception("Exception in post_files")
            return {"message": "error"}, 200
        else:
            return {"message": "success"}, 201
    return {"message": "error"}, 200


@bp.post("/json")
@pydantify(ResumeResponse)
@auth_required(Roles.user.value)
def post_json_file() -> tuple[dict, int]:
    """Create a new person or updates an existing person from file."""
    # Чтение файла JSON и создание объектов классов для сохранения в БД
    if not (file := request.data):
        return {"person_id": None, "exists": False}, 200
    try:
        json_data = json.loads(file)
        anketa = AnketaJson(**json_data)
    except (TypeError, json.JSONDecodeError, ValidationError):
        return {"person_id": None, "exists": False}, 200
    result = post_json(anketa)
    return result, 201 if result.get("person_id") else 200


def post_json(anketa: AnketaJson) -> dict:
    """Create a new person or updates an existing person based on the provided data."""
    try:
        # Валидация данных и создание объекта класса Person
        resume = PersonIn(**anketa.dict(exclude_none=True))
        # Загрузка резюме в БД
        person_id, existed = upload_resume(resume, g.user.id)

        # Сохранение дополнительной информации о кандидате в БД
        if person_id:
            upload_items(anketa, person_id)
    except (ValidationError, json.JSONDecodeError, TypeError):
        current_app.logger.exception("JSON Error")
        return {"person_id": None, "exists": False}
    else:
        return {"person_id": person_id, "exists": existed}


def upload_items(anketa: AnketaJson, person_id: int) -> None:
    """Save additional information about a person in the database."""
    try:
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
    except SQLAlchemyError:
        current_app.logger.exception("Add items Error")



@bp.get("/test")
@pydantify(BaseResponse)
@auth_required()
def test() -> tuple[dict, int]:
    """Test route."""
    return {"message": "success"}, 200
