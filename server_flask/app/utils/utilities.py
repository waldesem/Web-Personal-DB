"""Utils module."""

import os
import re
import unicodedata
from pathlib import Path

from flask import current_app
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.decorators.depend import current_user
from app.models.models import PersonIn
from app.tables.tables import Persons


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


def upload_resume(cand: PersonIn) -> tuple[int, bool]:
    """Upload a resume to the database.

    Args:
        cand (Person): The resume to be uploaded.

    Returns:
        int: The ID of the uploaded resume.
        bool: True if the resume existed earlier.

    """
    person = (
        db.session.execute(
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

    resume = cand.dict(exclude_none=True)
    resume["editable"] = True
    resume["user_id"] = current_user.id
    resume["region"] = current_user.region

    try:
        if not person:
            person = Persons(**resume)
            db.session.add(person)
            db.session.flush()
            person.destination = create_destination(person)
            db.session.commit()
            return person.id, False

        for k, v in resume.items():
            if v:
                setattr(person, k, v)
        if not person.destination or not Path(person.destination).is_dir():
            person.destination = create_destination(person)
        db.session.commit()
    except SQLAlchemyError:
        current_app.logger.exception("Database error")
        db.session.rollback()
        return None, False
    else:
        return person.id, True


def check_filename(name: str) -> str:
    """Check filename for valid chars."""
    try:
        filename_ascii_strip_re = re.compile(r"[^A-zА-яЁё0-9_.-]")
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
        if filename and filename.split(".")[0].upper() in windows_device_files:
            filename = f"_{filename}"
    except (TypeError, ValueError, AttributeError):
        current_app.logger.exception()
        return None
    else:
        return filename
