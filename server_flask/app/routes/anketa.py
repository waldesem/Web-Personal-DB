"""Anketa routes."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from flask import Blueprint, current_app, request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.classes.classes import Roles
from app.decorators.depend import auth_required, current_user
from app.decorators.validate import serialize
from app.models.models import AnketaJson, PersonIn
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
from app.utils.utilities import check_filename, create_destination, upload_resume

bp = Blueprint("anketa", __name__, url_prefix="/anketa")


@bp.get("/self/<int:person_id>")
@serialize()
@auth_required(Roles.user.value)
def change_self_id(person_id: int) -> tuple[str, int]:
    """Toggle the editable status of a person with the given item ID.

    The person ID is the ID of the person to toggle the editable status.
    The user ID is the ID of the user currently logged in.

    Returns:
        The HTTP status code is 200.

    """
    try:
        person = db.session.get(Persons, person_id)
        if not person.destination or not Path(person.destination).is_dir():
            person.destination = create_destination(person)
        if person.user_id != current_user.id:
            if person.editable:
                person.editable = False
            else:
                person.user_id = current_user.id
                person.editable = True
        else:
            person.editable = not person.editable
        db.session.commit()
    except SQLAlchemyError:
        current_app.logger.exception("Exception in change_self_id")
        return "error", 500
    else:
        return "success", 201


@bp.post("/files/<int:person_id>")
@serialize()
@auth_required(Roles.user.value)
def post_files(person_id: int) -> tuple[str, int]:
    """Upload a file to the server.

    Args:
        item (str): The name of the item.
        person_id (int): The ID of the person.
        file_data (list[File]): The file data.

    Returns:
        The HTTP status code is 200.

    """
    file_data = request.files.getlist("file")
    person = db.session.get(Persons, person_id)
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
        return "error", 500
    else:
        return "success", 201


@bp.post("/json")
@serialize()
@auth_required(roles=[Roles.user.value, Roles.api.value])
def post_json() -> tuple[dict, int]:
    """Create a new person or updates an existing person based on the provided data.

    Args:
        file (file): A JSON file containing the person data.

    Returns:
        A JSON response containing the person ID and an HTTP status code of 201.

    """
    try:
        # Чтение файла JSON и создание объектов классов для сохранения в БД
        file = request.files.get("file")
        if not file:
            return {"person_id": None, "exists": False}, 500

        json_data = json.load(file)
        anketa = AnketaJson(**json_data)

        # Валидация данных и создание объекта класса Person
        resume = PersonIn(**anketa.dict(exclude_none=True))
        # Загрузка резюме в БД
        person_id, existed = upload_resume(resume)

        # Сохранение дополнительной информации о кандидате в БД
        if person_id:
            upload_items(anketa, person_id)
    except (ValidationError, json.JSONDecodeError, TypeError):
        current_app.logger.exception("JSON Error")
        return {"person_id": None, "exists": False}, 500
    else:
        return {"person_id": person_id, "exists": existed}, 201


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
            Addresses(view="Адрес проживания", addresses=anketa.valid_address),
            Addresses(view="Адрес регистрации", addresses=anketa.reg_address),
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
