"""Utils."""

import asyncio
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.person import PersonIn
from app.tables.tables import Persons
from constants import BASE_PATH


async def create_destination(
    person_id: int,
    surname: str,
    firstname: str,
    patronymic: str | None,
) -> str:
    """Create destination.

    Args:
        person_id: Person ID.
        surname: str.
        firstname: str.
        patronymic: str.

    Returns:
        Destination string.

    """
    destination = Path(
        BASE_PATH,
        "Главный офис",
        surname[0],
        (f"{person_id}-{surname} {firstname} {patronymic or ''}").rstrip(),
    )
    await asyncio.to_thread(destination.mkdir, parents=True, exist_ok=True)
    return str(destination)


async def upload_resume(
    cand: PersonIn,
    user_id: int | None,
    db_session: AsyncSession,
) -> tuple[int | None, bool]:
    """Upload a resume to the database.

    Args:
        cand: PersonIn.
        user_id: User ID.
        db_session: AsyncSession.

    Returns:
        Tuple of person ID and boolean indicating if the person already existed.

    """
    stmt = select(Persons).where(
        Persons.surname == cand.surname,
        Persons.firstname == cand.firstname,
        Persons.patronymic == cand.patronymic,
        Persons.birthday == cand.birthday,
    )
    person = (await db_session.execute(stmt)).scalar_one_or_none()

    if person and person.editable and user_id and person.user_id != user_id:
        return None, True

    resume = cand.model_dump(exclude_none=True) | {"user_id": user_id}

    if not person:
        person = Persons(**resume)
        db_session.add(person)
        await db_session.flush()

        person.destination = await create_destination(
            person.id,
            person.surname,
            person.firstname,
            person.patronymic,
        )
        return person.id, False

    if not person.destination:
        resume["destination"] = create_destination(
            person.id,
            person.surname,
            person.firstname,
            person.patronymic,
        )
    for k, v in resume.items():
        if v:
            setattr(person, k, v)
    return person.id, True
