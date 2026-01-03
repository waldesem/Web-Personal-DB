"""Route routes."""

from __future__ import annotations

from typing import Any

from litestar import Request, get, post
from litestar.security.jwt import Token  # noqa: TC002
from sqlalchemy import func, not_, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: TC002

from app.classes.classes import Roles
from app.depends.auth import role_guard
from app.models.models import AnketaJson, Candidates, Index, PersonIn, User
from app.tables.tables import Base, Persons, Users
from app.utils.utilities import upload_items, upload_resume


@get("/candidates")
async def get_index(query: Index, db_session: AsyncSession) -> list[dict]:
    """Retrieve a paginated list of persons from the database."""
    async with db_session.begin():
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
        candidates = (
            await db_session.execute(
                stmt.filter(Users.id == Persons.user_id)
                .order_by(Persons.id.desc())
                .offset((query.page) * query.per_page)
                .limit(query.per_page),
            )
        ).all()
        return [Candidates.model_validate(cand).model_dump() for cand in candidates]


@get("/self/{person_id:int}", guards=[role_guard], opt={"roles": Roles.user.value})
async def switch_status(
    person_id: int,
    request: Request[User, Token, Any],
    db_session: AsyncSession,
) -> dict:
    """Toggle the editable status of a person."""
    async with db_session.begin():
        try:
            await db_session.execute(
                update(Persons)
                .where(Persons.id == person_id)
                .values(editable=not_(Persons.editable), user_id=request.user.id),
            )
        except SQLAlchemyError:
            request.logger.exception("Database error")
            return {"message": "error"}
        else:
            return {"message": "success"}


@post("/json", guards=[role_guard], opt={"roles": Roles.user.value})
async def post_json_file(
    data: AnketaJson,
    db_session: AsyncSession,
    request: Request[User, Token, Any],
) -> dict:
    """Create a new person or updates an existing person from file."""
    resume = PersonIn(**data.model_dump(exclude_none=True))
    # Загрузка резюме в БД
    person_id, existed = await upload_resume(resume, request.user.id, db_session)

    # Сохранение дополнительной информации о кандидате в БД
    if person_id:
        async with db_session.begin():
            items = upload_items(data, person_id)
            db_session.add_all(items)
    return {"person_id": person_id, "exists": existed}
