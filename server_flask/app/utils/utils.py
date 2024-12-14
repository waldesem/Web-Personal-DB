"""Utils module."""

import json
import re
from pathlib import Path

from flask import current_app
from pydantic import ValidationError
from sqlalchemy import select

from app.depends.depend import current_user
from app.model.models import AnketaSchemaJson
from app.model.tables import Persons, db_session


def upload_resume(resume: dict) -> int:
    """Upload a resume to the database.

    Args:
        resume (dict): The resume to be uploaded.

    Returns:
        int: The ID of the uploaded resume.

    """
    if not re.match(r"[А-ЯЁЙ]", resume["surname"][0]):  # noqa: RUF001
        return None
    resume["editable"] = True
    resume["user_id"] = current_user.get("id")
    resume["region"] = current_user.get("region")
    person = db_session.execute(
        select(Persons).where(
            Persons.surname == resume["surname"],
            Persons.firstname == resume["firstname"],
            Persons.patronymic == resume["patronymic"],
            Persons.birthday == resume["birthday"],
        ),
    ).scalar_one_or_none()

    if not person:
        person = Persons(**resume)
        db_session.add(person)
        db_session.flush()
        destination = Path(
            current_app.config["BASE_PATH"],
            person.region,
            person.surname[0],
            f"{person.id}-{person.surname} {person.firstname} "
            f"{person.patronymic}".rstrip(),
        )
        if not Path.exists(destination):
            Path.mkdir(destination)
        person.destination = str(destination)
        db_session.commit()
        return person.id

    if person.editable or resume["region"] != person.region:
        return None

    resume["id"] = person.id
    db_session.merge(Persons(**resume))
    db_session.commit()
    return person.id


def json_to_dict(file_data: str) -> dict:
    """Transform a JSON-dictionary into a python-dictionary.

    :param file_data: A JSON-dictionary
    :return: A python-dictionary.
    """
    json_data = json.load(file_data)
    try:
        anketa = AnketaSchemaJson(**json_data)
        return {
            "resume": {
                "surname": anketa.last_name,
                "firstname": anketa.first_name,
                "patronymic": anketa.mid_name,
                "birthday": anketa.birthday,
                "birthplace": anketa.birthplace,
                "citizenship": anketa.citizen,
                "dual": anketa.additional,
                "marital": anketa.marital_status,
                "inn": anketa.inn,
                "snils": anketa.snils,
            },
            "staffs": [
                {
                    "position": anketa.position_name,
                    "department": anketa.department,
                },
            ],
            "documents": [
                {
                    "view": "Паспорт",
                    "digits": anketa.passport_number,
                    "series": anketa.passport_serial,
                    "issue": anketa.passport_issue,
                    "agency": anketa.passport_issued,
                },
            ],
            "addresses": [
                {
                    "view": "Адрес проживания",
                    "addresses": anketa.valid_address,
                },
                {
                    "view": "Адрес регистрации",
                    "addresses": anketa.reg_address,
                },
            ],
            "contacts": [
                {"view": "Телефон", "contact": anketa.contact_phone},
                {"view": "Электронная почта", "contact": anketa.email},
            ],
            "educations": [
                {
                    "view": edu.education_type,
                    "institution": edu.institution_name,
                    "finished": edu.end_year,
                    "specialty": edu.specialty,
                }
                for edu in anketa.education
                if anketa.education
            ],
            "workplaces": [
                {
                    "starts": work.begin_date,
                    "finished": work.end_date,
                    "now_work": work.current_job,
                    "workplace": work.name,
                    "addresses": work.address,
                    "reason": work.fire_reason,
                    "position": work.position,
                }
                for work in anketa.experience
                if anketa.experience
            ],
            "previous": [
                {
                    "firstname": prev.first_name,
                    "surname": prev.last_name,
                    "patronymic": prev.mid_name,
                    "changed": prev.year_change,
                    "reason": prev.reason,
                }
                for prev in anketa.name_was_changed
                if anketa.name_was_changed
            ],
            "affilations": (
                [
                    {
                        "view": "Участвует в деятельности коммерческих организаций",
                        "organization": aff.name,
                        "inn": aff.inn,
                    }
                    for aff in anketa.organizations
                    if anketa.organizations
                ]
                + [
                    {
                        "view": "Являлся государственным должностным лицом",
                        "organization": aff.name,
                    }
                    for aff in anketa.state_organizations
                    if anketa.state_organizations
                ]
                + [
                    {
                        "view": "Связанные лица работают в государственных организациях",
                        "organization": aff.name,
                    }
                    for aff in anketa.related_organizations
                    if anketa.related_organizations
                ]
                + [
                    {
                        "view": "Являлся государственным или муниципальным служащим",
                        "organization": aff.name,
                    }
                    for aff in anketa.public_organizations
                    if anketa.public_organizations
                ]
            ),
        }
    except ValidationError:
        current_app.logger.exception("Validation error")
        return {}
