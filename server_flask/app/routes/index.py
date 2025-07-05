"""Route routes."""

import json

from flask import Blueprint, Response, current_app, jsonify, request
from pydantic import ValidationError
from sqlalchemy import desc, func, select
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.depends.depend import auth_required, current_user
from app.structures.classes import Regions, Roles
from app.structures.models import AnketaJson, Person
from app.structures.tables import (
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


@bp.get("/index")
@auth_required()
def get_index() -> Response:
    """Retrieve a paginated list of persons from the database.

    Arguments:
        None

    Returns:
        A JSON response containing a list of persons and an HTTP status code of 200.

    """
    # Создание SQL-запроса для получения списка кандидатов с учетом региона пользователя
    try:
        stmt = select(
            Persons.id,
            # Получение полного имени кандидата
            (
                Persons.surname
                + " "
                + Persons.firstname
                + " "
                + func.coalesce(Persons.patronymic, "")
            ).label("name"),
            Persons.birthday.label("birth"),
            Persons.editable.label("edit"),
            Persons.created.label("data"),
            Persons.region,
            Users.fullname.label("user"),
        ).filter(
            Users.id == Persons.user_id,
            Persons.region == current_user.region
            if current_user.region != Regions.main.value
            else True,
        )
        if search_str := request.args.get("search"):
            search = search_str.upper().split(maxsplit=3)[:3]
            stmt = stmt.where(
                Persons.surname == search[0],
                Persons.firstname == search[1] if len(search) > 1 else True,
                Persons.patronymic == search[2] if len(search) > 2 else True,
            )
        # Пагинация списка кандидатов
        result = db.paginate(stmt.order_by(desc(Persons.id)))
        return jsonify(result), 200
    except SQLAlchemyError:
        current_app.logger.exception("SQL Error")
        return jsonify([]), 500


@bp.post("/json")
@auth_required(roles=[Roles.user.value, Roles.api.value])
def post_json() -> Response:
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
            return jsonify({"person_id": None, "exists": False}), 500

        json_data = json.load(file)
        anketa = AnketaJson(**json_data)

        # Валидация данных и создание объекта класса Person
        resume = Person(**anketa.dict(exclude_none=True))
        # Загрузка резюме в БД
        person_id, existed = upload_resume(resume)

        # Сохранение дополнительной информации о кандидате в БД
        if person_id:
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
                item.person_id = person_id
                item.user_id = current_user.id

            db.session.bulk_save_objects(items)
            db.session.commit()
        return jsonify({"person_id": person_id, "exists": existed}), 201
    except (ValidationError, json.JSONDecodeError, SQLAlchemyError, TypeError):
        current_app.logger.exception("JSON Error")
        return jsonify({"person_id": None, "exists": False}), 500
