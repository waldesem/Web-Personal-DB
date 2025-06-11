"""Utils module."""

import os
import platform
import re
import unicodedata
from pathlib import Path

from flask import current_app
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.depends.depend import current_user
from app.model.models import AnketaJson, Person
from app.model.tables import (
    Addresses,
    Affilations,
    Contacts,
    Documents,
    Educations,
    Persons,
    Previous,
    Staffs,
    Workplaces,
    db_session,
)


def create_destination(person: Persons) -> str:
    """Create destination."""
    destination = Path(
        current_app.config["BASE_PATH"],
        person.region,
        person.surname[0],
        f"{person.id}-{person.surname} {person.firstname} {person.patronymic}".rstrip(),
    )
    destination.mkdir(parents=True, exist_ok=True)
    return str(destination)


def upload_resume(cand: Person) -> tuple[int, bool]:
    """Upload a resume to the database.

    Args:
        cand (Person): The resume to be uploaded.

    Returns:
        int: The ID of the uploaded resume.
        bool: True if the resume existed earlier.

    """
    person = (
        db_session.execute(
            select(Persons).where(
                Persons.surname == cand.surname,
                Persons.firstname == cand.firstname,
                Persons.patronymic == cand.patronymic,
                Persons.birthday == cand.birthday,
            ),
        ).scalar_one_or_none()
        if not cand.id
        else db_session.get(Persons, cand.id)
    )

    resume = cand.dict()
    resume["editable"] = True
    resume["user_id"] = current_user.id
    resume["region"] = current_user.region

    try:
        if not person:
            person = Persons(**resume)
            db_session.add(person)
            db_session.flush()
            person.destination = create_destination(person)
            db_session.commit()
            return person.id, False

        if person.user_id != current_user.id:
            return None, True

        for k, v in resume.items():
            if v:
                setattr(person, k, v)
        if not person.destination or not Path(person.destination).is_dir():
            person.destination = create_destination(person)
        db_session.commit()
    except SQLAlchemyError:
        current_app.logger.exception("Database error")
        db_session.rollback()
        return None, False
    else:
        return person.id, True


def upload_items(anketa: AnketaJson, person_id: int) -> None:
    """Get the anketa items.

    Args:
        anketa (AnketaSchemaJson): The anketa data.
        person_id (int): The ID of the person.

    Returns:
        None

    """
    try:
        items = [
            Documents(
                view="Паспорт",
                digits=anketa.digits,
                series=anketa.series,
                issue=anketa.issue,
                agency=anketa.agency,
            ),
            Staffs(position=anketa.position_name, department=anketa.department),
            Addresses(view="Адрес проживания", addresses=anketa.valid_address),
            Addresses(view="Адрес регистрации", addresses=anketa.reg_address),
            Contacts(view="Телефон", contact=anketa.contact_phone),
            Contacts(view="Электронная почта", contact=anketa.email),
            *[Educations(**edu.dict()) for edu in anketa.education],
            *[Workplaces(**work.dict()) for work in anketa.experience],
            *[Previous(**prev.dict()) for prev in anketa.name_was_changed],
            *[
                Affilations(
                    view="Участвует в деятельности коммерческих организаций",
                    organization=aff.name,
                    inn=aff.inn,
                )
                for aff in anketa.organizations
            ],
            *[
                Affilations(
                    view="Являлся государственным должностным лицом",
                    organization=aff.name,
                )
                for aff in anketa.state_organizations
            ],
            *[
                Affilations(
                    view="Связанные лица работают в государственных организациях",
                    organization=aff.name,
                )
                for aff in anketa.related_organizations
            ],
            *[
                Affilations(
                    view="Являлся государственным или муниципальным служащим",
                    organization=aff.name,
                )
                for aff in anketa.public_organizations
            ],
        ]

        for item in items:
            item.person_id = person_id
            item.user_id = current_user.id

        db_session.add_all(items)
        db_session.commit()
    except SQLAlchemyError:
        current_app.logger.exception("SQLAlchemyError in post json items")
        db_session.rollback()


def check_filename(name: str) -> str:
    """Check filename for valid chars."""
    filename_ascii_strip_re = re.compile(r"[^A-zА-яЁё0-9_.-]")  # noqa: RUF001
    windows_device_files = (
        "CON",
        "AUX",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "LPT1",
        "LPT2",
        "LPT3",
        "PRN",
        "NUL",
    )
    filename = unicodedata.normalize("NFKD", name)
    for sep in os.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")
    filename = str(
        filename_ascii_strip_re.sub("", "_".join(filename.split())),
    ).strip("._")
    if (
        platform.system().lower() == "windows"
        and filename
        and filename.split(".")[0].upper() in windows_device_files
    ):
        filename = f"_{filename}"
    return filename
