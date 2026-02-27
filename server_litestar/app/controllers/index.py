"""Route routes."""

from __future__ import annotations

from advanced_alchemy.base import BigIntAuditBase
from litestar import get
from pydantic import TypeAdapter
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Candidates, Index
from app.tables.tables import Persons, Users


@get("/candidates")
async def get_candidates(query: Index, db_session: AsyncSession) -> list[Candidates]:
    """Retrieve a paginated list of persons from the database."""
    tables = BigIntAuditBase.metadata.tables
    stmt = select(
        tables["persons"],
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
            .offset((query.page - 1) * query.per_page)
            .limit(query.per_page),
        )
    ).all()
    return TypeAdapter(list[Candidates]).validate_python(candidates)
