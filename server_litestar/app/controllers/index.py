"""Route routes."""

from __future__ import annotations

from typing import Any

from litestar import Request, get
from litestar.security.jwt import Token
from pydantic import TypeAdapter
from sqlalchemy import func, not_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.classes.classes import Roles
from app.depends.auth import role_guard
from app.models.models import Candidates, Index, User
from app.tables.tables import Persons, Users, config


@get("/candidates")
async def get_candidates(query: Index, db_session: AsyncSession) -> list[Candidates]:
    """Retrieve a paginated list of persons from the database."""
    async with db_session.begin():
        stmt = select(
            config.metadata.tables["persons"],
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


@get(
    "/status/{person_id:int}",
    guards=[role_guard],
    opt={"roles": Roles.user.value},
)
async def switch_status(
    person_id: int,
    request: Request[User, Token, Any],
    db_session: AsyncSession,
) -> dict:
    """Toggle the editable status of a person."""
    async with db_session.begin():
        await db_session.execute(
            update(Persons)
            .where(Persons.id == person_id)
            .values(editable=not_(Persons.editable), user_id=request.user.id),
        )
        return {"message": "success"}
