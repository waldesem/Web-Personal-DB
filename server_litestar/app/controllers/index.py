"""Route routes."""

from __future__ import annotations

from litestar import get
from pydantic import TypeAdapter
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.person import Candidates, Index
from app.tables.tables import Persons, Users

ta = TypeAdapter(list[Candidates])


@get("/candidates")
async def get_candidates(query: Index, db_session: AsyncSession) -> list[Candidates]:
    """Retrieve a paginated list of persons from the database.

    Args:
        query: Index query parameters: search, page, per_page.
        db_session: Database session.

    Returns:
            List of persons.

    """
    stmt = select(
        Persons.id,
        Persons.surname,
        Persons.firstname,
        Persons.patronymic,
        Persons.birthday,
        Persons.updated_at,
        Persons.editable,
        Users.fullname.label("username"),
        func.count().over().label("total"),
    )
    if query.search:
        stmt = stmt.filter(Persons.surname == query.search[0])
        if len(query.search) > 1:
            stmt = stmt.filter(Persons.firstname == query.search[1])
            if len(query.search) > 2:
                stmt = stmt.filter(Persons.patronymic == query.search[2])

    candidates = (
        await db_session.execute(
            stmt.filter(Users.id == Persons.user_id)
            .order_by(Persons.id.desc())
            .offset((query.page - 1) * query.per_page)
            .limit(query.per_page),
        )
    ).all()
    return ta.validate_python(candidates, from_attributes=True)
