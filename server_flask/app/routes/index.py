"""Route routes."""

import gzip
import json

from flask import Blueprint, Response, current_app, jsonify, request
from pydantic import ValidationError
from sqlalchemy import desc, select
from sqlalchemy.exc import SQLAlchemyError

from app.depends.depend import auth_required, current_user, validate
from app.model.classes import Regions, Roles
from app.model.models import AnketaJson, Person
from app.model.tables import (
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
    db_session,
)
from app.utils.utils import upload_resume

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
    stmt = select(
        Persons.id,
        Persons.surname,
        Persons.firstname,
        Persons.patronymic,
        Persons.region,
        Persons.birthday,
        Persons.editable,
        Persons.created,
        Users.fullname.label("username"),
    ).filter(
        Persons.user_id == Users.id,
        Persons.region == current_user.region
        if current_user.region != Regions.main.value
        else True,
    )
    query = db_session.execute(stmt.order_by(desc(Persons.id))).all()
    resp = jsonify([row._asdict() for row in query])
    compressed_data = gzip.compress(resp.data)
    return Response(
        compressed_data,
        mimetype="application/json",
        headers={"Content-Encoding": "gzip", "Content-Length": len(compressed_data)},
        status=200,
    )


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
        file_data = request.files.get("file")
        json_data = json.load(file_data)
        anketa = AnketaJson(**json_data)
        resume = Person(**anketa.dict())
        person_id, existed = upload_resume(resume)
        if person_id:
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
                        organization=aff.name,
                        inn=aff.inn,
                    )
                    for aff in anketa.organizations
                ],
                *[
                    Affilations(
                        view="Являлся государственным должностным лицом",
                        organization=aff.name,
                    )
                    for aff in anketa.state_organizations
                ],
                *[
                    Affilations(
                        view="Связанные лица работают в государственных организациях",
                        organization=aff.name,
                    )
                    for aff in anketa.related_organizations
                ],
                *[
                    Affilations(
                        view="Являлся государственным или муниципальным служащим",
                        organization=aff.name,
                    )
                    for aff in anketa.public_organizations
                ],
            ]

            for item in items:
                item.person_id = person_id
                item.user_id = current_user.id

            db_session.add_all(items)
            db_session.commit()
        return jsonify({"person_id": person_id, "exists": existed}), 201
    except (ValidationError, json.JSONDecodeError, SQLAlchemyError, TypeError):
        current_app.logger.exception("JSON Error")
        return jsonify({"person_id": None, "exists": False}), 200
