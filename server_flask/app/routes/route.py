"""Route routes."""

import json

from flask import Blueprint, Response, current_app, jsonify, request
from pydantic import ValidationError
from sqlalchemy import desc, select

from app.depends.depend import auth_required, current_user, validate
from app.model.classes import Regions, Roles
from app.model.models import AnketaJson, Person, Search
from app.model.tables import Persons, Users, db_session
from app.utils.utils import upload_items, upload_resume

bp = Blueprint("route", __name__)


@bp.get("/index/<int:page>")
@validate
@auth_required()
def get_index(page: int, query_data: Search) -> Response:
    """Retrieve a paginated list of persons from the database.

    Arguments:
        page (int): The page number of the results.
        query_data (Search): The search criteria, pagination, and sorting options.

    Returns:
        tuple: A tuple containing the list of persons, a boolean indicating if
        there are more results, and a 200 status code.

    """
    stmt = select(Persons, Users.fullname).filter(
        Persons.user_id == Users.id,
        Persons.region == current_user.region
        if current_user.region != Regions.main.value
        else True,
    )
    if query_data.search:
        fio = query_data.search.upper().split()[:3]
        stmt = stmt.filter(
            Persons.surname == fio[0] if fio else True,
            Persons.firstname == fio[1] if len(fio) > 1 else True,
            Persons.patronymic == fio[2] if len(fio) > 2 else True,  # noqa: PLR2004
        )
    if query_data.editable:
        stmt = stmt.filter(Persons.editable == query_data.editable)

    query = db_session.execute(
        stmt.order_by(desc(Persons.id))
        .offset((page - 1) * query_data.pagination)
        .limit(query_data.pagination + 1),
    ).all()

    result = [row[0].to_dict() | {"username": row[1]} for row in query]
    has_next = len(result) > query_data.pagination
    return jsonify(
        {
            "results": result[: query_data.pagination] if has_next else result,
            "has_next": has_next,
        },
    ), 200


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
    return jsonify(
        {"person_id": person_id, "exists": existed},
    ), 201


@bp.post("/json")
@auth_required(roles=(Roles.user.value, Roles.api.value))
def post_json() -> Response:
    """Create a new person or updates an existing person based on the provided data.

    Args:
        file_data (File): The data to create or update the person.

    Returns:
        A JSON response containing the person ID and an HTTP status code of 201.

    """
    file_data = request.files.get("file")
    try:
        json_data = json.load(file_data)
        anketa = AnketaJson(**json_data)
        resume = Person(**anketa.dict())
        person_id, existed = upload_resume(resume)
        if person_id:
            upload_items(anketa, person_id)
        return jsonify(
            {"person_id": person_id, "exists": existed},
        ), 201
    except (ValidationError, json.JSONDecodeError, TypeError):
        current_app.logger.exception("JSON Error")
        return jsonify({"person_id": None, "exists": False}), 200
