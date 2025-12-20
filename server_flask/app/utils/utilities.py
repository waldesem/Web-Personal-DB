"""Utils module."""

from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from flask import current_app, g
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.models import AnketaJson, PersonIn
from app.tables.tables import (
    Addresses,
    Affilations,
    Contacts,
    Documents,
    Educations,
    Persons,
    Previous,
    Staffs,
    Workplaces,
)


def create_token(user_id: int, item: str = "ACCESS") -> str:
    """Create token."""
    return jwt.encode(
        {
            "id": user_id,
            "exp": datetime.now(tz=timezone.utc)  # noqa: UP017
            + timedelta(minutes=current_app.config[f"{item}_SECRET_KEY_LIVE"]),
        },
        current_app.config[f"{item}_SECRET_KEY"],
        algorithm="HS256",
    )


def decode_token(header: str, *, refresh: bool = False) -> dict | None:
    """Decode JWT token and return payload."""
    try:
        return jwt.decode(
            header[7:],
            current_app.config[f"{'REFRESH' if refresh else 'ACCESS'}_SECRET_KEY"],
            algorithms=["HS256"],
            options={"verify_exp": True},
        )
    except (InvalidTokenError, IndexError, AttributeError):
        return None


def create_destination(person: Persons) -> str:
    """Create destination."""
    destination = Path(
        current_app.config["BASE_PATH"],
        "Главный офис",
        person.surname[0],
        f"{person.id}-{person.surname} {person.firstname} {person.patronymic}".rstrip(),
    )
    destination.mkdir(parents=True, exist_ok=True)
    return str(destination)


def upload_resume(cand: PersonIn) -> tuple[int | None, bool]:
    """Upload a resume to the database."""
    person = (
        db.session.get(Persons, cand.id)
        if cand.id
        else db.session.execute(
            select(Persons).where(
                Persons.surname == cand.surname,
                Persons.firstname == cand.firstname,
                Persons.patronymic == cand.patronymic,
                Persons.birthday == cand.birthday,
            ),
        ).scalar_one_or_none()
        if not cand.id
        else db.session.get(Persons, cand.id)
    )

    resume = cand.model_dump(
        exclude_none=True,
        exclude={"created"},
    ) | {"user_id": g.user.id}

    try:
        if not person:
            person = Persons(**resume)
            db.session.add(person)
            db.session.flush()
            person.destination = create_destination(person)
            db.session.commit()
            return person.id, False

        if not person.destination or not Path(person.destination).is_dir():
            resume["destination"] = create_destination(person)
        for k, v in resume.items():
            setattr(person, k, v)
        db.session.commit()
    except SQLAlchemyError:
        current_app.logger.exception("Database error")
        db.session.rollback()
        return None, False
    else:
        return person.id, True


def post_json(anketa: AnketaJson) -> dict:
    """Create a new person or updates an existing person based on the provided data."""
    resume = PersonIn(**anketa.model_dump(exclude_none=True))
    # Загрузка резюме в БД
    person_id, existed = upload_resume(resume)

    # Сохранение дополнительной информации о кандидате в БД
    if person_id:
        items = upload_items(anketa, person_id)
        db.session.bulk_save_objects(items)
        db.session.commit()
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
