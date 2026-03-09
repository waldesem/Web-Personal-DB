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


def validate_inn(inn: str | None) -> str | None:
    """Check inn."""
    try:
        from rust_module import validate_inn  # ty:ignore[unresolved-import]

        return validate_inn(inn)
    except ImportError:
        if inn:
            inn = inn.replace("-", "").replace(" ", "")
            if len(inn) != 12 and not inn.isdigit():
                return None
            c1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0, 0]
            c2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0]
            check1 = sum([int(inn[i]) * c1[i] for i in range(12)]) % 11 % 10
            check2 = sum([int(inn[i]) * c2[i] for i in range(12)]) % 11 % 10
            if check1 == int(inn[10]) and check2 == int(inn[11]):
                return inn
        return None


def validate_snils(snils: str | None) -> str | None:
    """Check snils."""
    if snils:
        # Получаем первые 9 цифр и контрольное число (последние 2)
        snils = snils.replace("-", "").replace(" ", "")
        if len(snils) != 11 and not snils.isdigit():
            return None
        digits = [int(d) for d in snils]
        main_part = digits[:9]
        check_sum = int(snils[9:])

        # Вычисляем контрольную сумму
        sum_prod = sum(main_part[i] * (9 - i) for i in range(9))

        # Алгоритм проверки контрольного числа
        calculated_sum = 0
        if sum_prod < 100:
            calculated_sum = sum_prod
        elif sum_prod in {100, 101}:
            calculated_sum = 0
        else:
            remainder = sum_prod % 101
            calculated_sum = 0 if remainder == 100 else remainder
        if calculated_sum == check_sum:
            return snils
    return None
