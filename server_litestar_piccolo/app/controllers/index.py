"""Route routes."""

from __future__ import annotations

from litestar import get
from pydantic import TypeAdapter

from app.models.person import Candidates, Index
from app.tables.tables import Persons

ta = TypeAdapter(list[Candidates])


@get("/candidates")
async def get_candidates(query: Index) -> list[Candidates]:
    """Retrieve a paginated list of persons from the database.

    Args:
        query: Index query parameters: search, page, per_page.

    Returns:
            List of persons.

    """
    stmt = """
        SELECT
        p.id,
        p.surname,
        p.firstname,
        p.patronymic,
        p.birthday,
        p.updated_at,
        p.editable,
        u.fullname AS username,
        COUNT(*) OVER () AS total
    FROM persons p
    JOIN users u ON u.id = p.user_id
    WHERE NOT p.deleted
    """
    search = []
    if query.search:
        stmt += " AND p.surname = {}"
        search.append(query.search[0])
        if query.search and len(query.search) > 1:
            stmt += " AND p.firstname = {}"
            search.append(query.search[1])
            if query.search and len(query.search) > 2:
                stmt += " AND p.patronymic = {}"
                search.append(query.search[2])
    stmt += f" ORDER BY p.id DESC OFFSET {(query.page - 1) * query.per_page}"
    stmt += f" LIMIT {query.per_page}"
    candidates = await Persons.raw(stmt, *search)
    return ta.validate_python(candidates)
