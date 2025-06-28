"""Route routes."""

import json

from flask import Blueprint, Response, current_app, jsonify, request
from pydantic import ValidationError
from sqlalchemy import case, func, select
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.depends.depend import auth_required, current_user
from app.depends.validate import validate
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
@validate
@auth_required()
def get_index() -> Response:
    """Retrieve a paginated list of persons from the database.

    Arguments:
        None

    Returns:
        tuple: A tuple containing the list of persons, a boolean indicating if
        there are more results, and a 200 status code.

    """
    # Создание SQL-запроса для получения списка кандидатов с учетом региона пользователя
    stmt = select(
        Persons.id,
        (Persons.surname + " " + Persons.firstname + " " + Persons.patronymic).label(
            "name",
        ),
        func.strftime("%d.%m.%Y", Persons.birthday).label("birth"),
        case(
            (
                Persons.editable, 0,
            ),
            else_=1,
        ).label("edit"),
        func.strftime("%d.%m.%Y", Persons.created).label("data"),
        case(
            (
                func.instr(Users.fullname, " ") > 0,
                func.substr(Users.fullname, 1, func.instr(Users.fullname, " ") - 1),
            ),
            else_=Users.fullname,
        ).label(
            "user",
        ),
    ).filter(
        Persons.user_id == Users.id,
        Persons.region == current_user.region
        if current_user.region != Regions.main.value
        else True,
    )
    query = db.session.execute(stmt).all()
    # Создание списка словарей с данными кандидатов и сериализация их в JSON
    return jsonify([row._asdict() for row in query[::-1]]), 200


@bp.post("/resume")
@validate
@auth_required(Roles.user.value)
def post_resume(json_data: Person) -> Response:
    """Create a new person or updates an existing person based on the provided data.

    Args:
        json_data (Person): The data to create or update the person.

    Returns:
        A JSON response containing the person ID and an HTTP status code of 201.

    """
    # Загузка резюме в БД
    person_id, existed = upload_resume(json_data)
    return jsonify({"person_id": person_id, "exists": existed}), 201


@bp.post("/json")
@auth_required(roles=[Roles.user.value, Roles.api.value])
def post_json() -> Response:
    """Create a new person or updates an existing person based on the provided data.

    Args:
        file_data (File): The data to create or update the person.

    Returns:
        A JSON response containing the person ID and an HTTP status code of 201.

    """
    try:
        # Чтение файла JSON и создание объектов классов для сохранения в БД
        file_data = request.files.get("file")
        json_data = json.load(file_data)
        anketa = AnketaJson(**json_data)
        resume = Person(**anketa.dict(exclude_none=True))
        # Загузка резюме в БД
        person_id, existed = upload_resume(resume)
        if person_id:
            # Сохранение дополнительной информации о кандидате в БД
            items = [
                Documents(
                    view="Паспорт",
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
            # Добавление объектов в сессию и сохранение изменений в БД
            for item in items:
                item.person_id = person_id
                item.user_id = current_user.id

            db.session.add_all(items)
            db.session.commit()
        return jsonify({"person_id": person_id, "exists": existed}), 201
    except (ValidationError, json.JSONDecodeError, SQLAlchemyError, TypeError):
        current_app.logger.exception("JSON Error")
        return jsonify({"person_id": None, "exists": False}), 200
