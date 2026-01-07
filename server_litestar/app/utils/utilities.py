"""Utils module."""

from pathlib import Path

from litestar import Request
from litestar.security.jwt import Token
from sqlalchemy import label, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import ItemModel, Items, PersonIn
from app.tables.tables import Base, Persons
from constants import BASE_PATH, REFRESH_SECRET_KEY


def create_destination(person: Persons) -> str:
    """Create destination."""
    destination = Path(
        BASE_PATH,
        "Главный офис",
        person.surname[0],
        f"{person.id}-{person.surname} {person.firstname} {person.patronymic}".rstrip(),
    )
    destination.mkdir(parents=True, exist_ok=True)
    return str(destination)


async def upload_resume(
    cand: PersonIn,
    user_id: int,
    db_session: AsyncSession,
) -> tuple[int | None, bool]:
    """Upload a resume to the database."""
    async with db_session.begin():
        person = (
            await db_session.get(Persons, cand.id)
            if cand.id
            else (
                await db_session.execute(
                    select(Persons).where(
                        Persons.surname == cand.surname,
                        Persons.firstname == cand.firstname,
                        Persons.patronymic == cand.patronymic,
                        Persons.birthday == cand.birthday,
                    ),
                )
            ).scalar_one_or_none()
        )

        resume = cand.model_dump(
            exclude_none=True,
            exclude={"created"},
        ) | {"user_id": user_id}

        try:
            if not person:
                person = Persons(**resume)
                db_session.add(person)
                db_session.flush()
                person.destination = create_destination(person)
                return person.id, False

            if not person.destination or not Path(person.destination).is_dir():
                resume["destination"] = create_destination(person)
            for k, v in resume.items():
                setattr(person, k, v)
        except SQLAlchemyError:
            db_session.rollback()
            return None, False
        else:
            return person.id, True


async def select_item(
    item: Items,
    person_id: int,
    db_session: AsyncSession,
) -> list[dict]:
    """Retrieve an item from the database based on the provided item."""
    async with db_session.begin():
        table = Base.metadata.tables[item]
        stmt = (
            select(table, label("item", item))
            .filter(table.c.person_id == person_id)
            .order_by(table.c.id.desc())
        )
        items = (await db_session.execute(stmt)).all()
        return [ItemModel.model_validate({"item": tbl}).item for tbl in items]


async def decode_token(request: Request) -> Token | None:
    """Decode the token."""
    token: dict = await request.json()
    if not token:
        return None
    return Token.decode(
        token.get("refresh_token").split()[1],
        REFRESH_SECRET_KEY,
        "HS256",
    )
