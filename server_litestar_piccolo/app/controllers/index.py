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
    params = []
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
    if query.last_seen_id:
        stmt += " p.id < {}"
        params.append(query.last_seen_id)
    if query.search:
        stmt += " AND p.surname = {}"
        params.append(query.search[0])
        if query.search and len(query.search) > 1:
            stmt += " AND p.firstname = {}"
            params.append(query.search[1])
            if query.search and len(query.search) > 2:
                stmt += " AND p.patronymic = {}"
                params.append(query.search[2])
    stmt += f" ORDER BY p.id DESC LIMIT {query.per_page}"
    candidates = await Persons.raw(stmt, *params)
    return ta.validate_python(candidates)
