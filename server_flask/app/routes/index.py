"""Route routes."""

from __future__ import annotations

from flask import Blueprint, Response, g, json, jsonify, request
from sqlalchemy import func, not_, select, update

from app import db
from app.classes.classes import Roles
from app.decorators.depend import auth_required
from app.decorators.pydantify import validize
from app.models.models import (
    AnketaJson,
    Candidates,
    Index,
)
from app.tables.tables import Persons, Users
from app.utils.utilities import post_json

bp = Blueprint("route", __name__)


@bp.get("/candidates")
@validize()
@auth_required()
def get_index(json_query: Index) -> Response:
    """Retrieve a paginated list of persons from the database."""
    stmt = select(
        db.metatables["persons"],
        Users.fullname.label("username"),
        func.count().over().label("total"),
    )
    if json_query.search:
        stmt = stmt.filter(Persons.surname == json_query.search[0])
        if len(json_query.search) > 1:
            stmt = stmt.filter(Persons.firstname == json_query.search[1])
            if len(json_query.search) > 2:
                stmt = stmt.filter(Persons.patronymic == json_query.search[2])
    # Пагинация списка кандидатов
    candidates = db.session.execute(
        stmt.filter(Users.id == Persons.user_id)
        .order_by(Persons.id.desc())
        .offset((json_query.page - 1) * json_query.per_page)
        .limit(json_query.per_page),
    ).all()
    return jsonify(
        [Candidates.model_validate(cand).model_dump() for cand in candidates],
    ), 200


@bp.get("/self/<int:person_id>")
@validize()
@auth_required(Roles.user.value)
def switch_status(person_id: int) -> Response:
    """Toggle the editable status of a person."""
    stmt = (
        update(Persons)
        .where(Persons.id == person_id)
        .values(editable=not_(Persons.editable))
    )
    db.session.execute(stmt, {"user_id": g.user.id, "id": person_id})
    db.session.commit()
    return jsonify({"message": "success"}), 201


@bp.post("/json")
@validize()
@auth_required(Roles.user.value)
def post_json_file() -> Response:
    """Create a new person or updates an existing person from file."""
    # Чтение файла JSON и создание объектов классов для сохранения в БД
    if not (file := request.data):
        return {"person_id": None, "exists": False}, 200
    try:
        json_data = json.loads(file)
        anketa = AnketaJson(**json_data)
    except (AttributeError, TypeError):
        return {"person_id": None, "exists": False}, 200
    result = post_json(anketa)
    return result, 201 if result.get("person_id") else 200
