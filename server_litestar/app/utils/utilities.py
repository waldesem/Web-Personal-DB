"""Utils module."""

from pathlib import Path
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.models.models import AnketaJson, Items, PersonIn, models
from app.tables.tables import (
    Addresses,
    Affilations,
    Base,
    Contacts,
    Documents,
    Educations,
    Persons,
    Previous,
    Staffs,
    Workplaces,
)
from config import Config

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


def create_destination(person: Persons) -> str:
    """Create destination."""
    destination = Path(
        Config.BASE_PATH,
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


async def post_json(anketa: AnketaJson, user_id: int, db_session: AsyncSession) -> dict:
    """Create a new person or updates an existing person based on the provided data."""
    resume = PersonIn(**anketa.model_dump(exclude_none=True))
    # Загрузка резюме в БД
    person_id, existed = upload_resume(resume, user_id, db_session)

    # Сохранение дополнительной информации о кандидате в БД
    if person_id:
        async with db_session.begin():
            items = upload_items(anketa, person_id)
            db_session.bulk_save_objects(items)
    return {"person_id": person_id, "exists": existed}


def upload_items(anketa: AnketaJson, person_id: int) -> list:
    """Organze additional information about a person for database uploads."""
    return [
        Documents(
            digits=anketa.digits,
            series=anketa.series,
            issue=anketa.issue,
            agency=anketa.agency,
            person_id=person_id,
        ),
        Staffs(
            position=anketa.position,
            department=anketa.department,
            person_id=person_id,
        ),
        Addresses(
            view="Адрес проживания",
            address=anketa.valid_address,
            person_id=person_id,
        ),
        Addresses(
            view="Адрес регистрации",
            address=anketa.reg_address,
            person_id=person_id,
        ),
        Contacts(
            view="Телефон",
            contact=anketa.contact_phone,
            person_id=person_id,
        ),
        Contacts(
            view="Электронная почта",
            contact=anketa.email,
            person_id=person_id,
        ),
        *[
            Educations(**education.model_dump(), person_id=person_id)
            for education in anketa.education
        ],
        *[
            Workplaces(**workplace.model_dump(), person_id=person_id)
            for workplace in anketa.experience
        ],
        *[
            Previous(**prev.model_dump(), person_id=person_id)
            for prev in anketa.name_was_changed
        ],
        *[
            Affilations(
                view="Участвует в деятельности коммерческих организаций",
                organization=aff.organization,
                inn=aff.inn,
                person_id=person_id,
            )
            for aff in anketa.organizations
        ],
        *[
            Affilations(
                view="Являлся государственным должностным лицом",
                organization=aff.organization,
                person_id=person_id,
            )
            for aff in anketa.state_organizations
        ],
        *[
            Affilations(
                view="Связанные лица работают в государственных организациях",
                organization=aff.organization,
                person_id=person_id,
            )
            for aff in anketa.related_organizations
        ],
        *[
            Affilations(
                view="Являлся государственным или муниципальным служащим",
                organization=aff.organization,
                person_id=person_id,
            )
            for aff in anketa.public_organizations
        ],
    ]


async def select_item(item: Items, person_id: int, db_session: AsyncSession) -> list:
    """Retrieve an item from the database based on the provided item."""
    async with db_session.begin():
        table = Base.metadata.tables[item]
        stmt = (
            table.select()
            .filter(table.c.person_id == person_id)
            .order_by(table.c.id.desc())
        )
        items = await db_session.execute(stmt).all()
        return [models[item].model_validate(table).model_dump() for table in items]
