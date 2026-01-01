"""Route routes."""

from __future__ import annotations

from typing import Annotated, Any

import orjson
from litestar import Request, get, post
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body
from litestar.security.jwt import Token
from sqlalchemy import func, not_, select, update
from sqlalchemy.exc import SQLAlchemyError

from app.models.models import AnketaJson, Candidates, Index, User
from app.tables.tables import Base, Persons, Users, session
from app.utils.utilities import post_json


@get("/candidates")
async def get_index(query: Index, sync_to_thread: bool = False) -> list[dict]:
    """Retrieve a paginated list of persons from the database."""
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
    candidates = session.execute(
        stmt.filter(Users.id == Persons.user_id)
        .order_by(Persons.id.desc())
        .offset((query.page) * query.per_page)
        .limit(query.per_page),
    ).all()
    return [Candidates.model_validate(cand).model_dump() for cand in candidates]


@get("/self/<int:person_id>")
async def switch_status(
    request: Request[User, Token, Any],
    person_id: int,
    sync_to_thread: bool = False,
) -> dict:
    """Toggle the editable status of a person."""
    try:
        session.execute(
            update(Persons)
            .where(Persons.id == person_id)
            .values(editable=not_(Persons.editable), user_id=request.user.id),
        )
        session.commit()
        return {"message": "success"}
    except SQLAlchemyError:
        request.logger.exception("Database error")
        return {"message": "error"}


@post("/json")
async def post_json_file(
    data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
    sync_to_thread: bool = False,
) -> dict:
    """Create a new person or updates an existing person from file."""
    # Чтение файла JSON и создание объектов классов для сохранения в БД
    try:
        json_data = orjson.loads(data)
        anketa = AnketaJson(**json_data)
    except (AttributeError, TypeError):
        return {"person_id": None, "exists": False}
    result = post_json(anketa)
    return result
