"""Utils module."""

import os
import re
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from flask import current_app
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app import db, revoked
from app.models.models import PersonIn, User
from app.tables.tables import Persons, Users


def create_access_token(user: Users | User) -> str:
    """Create token."""
    return jwt.encode(
        {
            "id": user.id,
            "fullname": user.fullname,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "exp": datetime.now(tz=timezone.utc)  # noqa: UP017
            + timedelta(minutes=current_app.config["JWT_SECRET_KEY_LIVE"]),
        },
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256",
    )


def create_refresh_token(user: Users) -> str:
    """Create refresh token."""
    return jwt.encode(
        {
            "id": user.id,
            "exp": datetime.now(tz=timezone.utc)  # noqa: UP017
            + timedelta(days=current_app.config["REFRESH_SECRET_KEY_LIVE"]),
        },
        current_app.config["REFRESH_SECRET_KEY"],
        algorithm="HS256",
    )


def decode_token(header: str, *, refresh: bool = False) -> dict | None:
    """Decode JWT token and return payload."""
    decoded = None
    try:
        if (bearer := header[7:]) and bearer.split(".")[-1] not in revoked.data:
            decoded = jwt.decode(
                bearer,
                current_app.config["JWT_SECRET_KEY"]
                if not refresh
                else current_app.config["REFRESH_SECRET_KEY"],
                algorithms=["HS256"],
                options={"verify_exp": True},
            )
    except (InvalidTokenError, ValidationError, IndexError, ValueError):
        current_app.logger.exception("JWT decode failed")
        return None
    else:
        return decoded


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


def upload_resume(cand: PersonIn, user_id: int) -> tuple[int | None, bool]:
    """Upload a resume to the database."""
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

    resume = cand.dict(exclude_none=True, exclude={"created"})
    resume["editable"] = True
    resume["user_id"] = user_id

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


def check_filename(name: str) -> str | None:
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
