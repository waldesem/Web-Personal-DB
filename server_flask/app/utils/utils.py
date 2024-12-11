import json
import os
import re

from flask import current_app
from pydantic import ValidationError
from sqlalchemy import select

from ..depends.depend import current_user
from ..model.models import AnketaSchemaJson
from ..model.tables import Persons, db_session


def upload_resume(resume: dict):
    if not re.match(r"[А-ЯЁЙ]", resume["surname"][0]):
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
        )
    ).scalar_one_or_none()

    if not person:
        person = Persons(**resume)
        db_session.add(person)
        db_session.flush()
        person.destination = os.path.join(
            current_app.config["BASE_PATH"],
            resume["region"],
            resume["surname"][0],
            f"{person.id}-{resume['surname']} {resume['firstname']} "
            f"{resume.get('patronymic', '')}".rstrip().upper(),
        )
        if not os.path.isdir(person.destination):
            os.mkdir(person.destination)
        db_session.commit()
        return person.id

    if person.editable or resume["region"] != person.region:
        return None

    resume["id"] = person.id
    db_session.merge(Persons(**resume))
    db_session.commit()
    return person.id


def json_to_dict(file_data) -> dict:
    """
    Transforms a JSON-dictionary into a python-dictionary.

    :param file_data: A JSON-dictionary
    :return: A python-dictionary
    """
    json_data = json.load(file_data)
    try:
        anketa = AnketaSchemaJson(**json_data)
        return {
            "resume": {
                "surname": anketa.lastName,
                "firstname": anketa.firstName,
                "patronymic": anketa.midName,
                "birthday": anketa.birthday,
                "birthplace": anketa.birthplace,
                "citizenship": anketa.citizen,
                "dual": anketa.additionalCitizenship,
                "marital": anketa.maritalStatus,
                "inn": anketa.inn,
                "snils": anketa.snils,
            },
            "staffs": [
                {
                    "position": anketa.positionName,
                    "department": anketa.department,
                }
            ],
            "documents": [
                {
                    "view": "Паспорт",
                    "digits": anketa.passportNumber,
                    "series": anketa.passportSerial,
                    "issue": anketa.passportIssueDate,
                    "agency": anketa.passportIssuedBy,
                }
            ],
            "addresses": [
                {
                    "view": "Адрес проживания",
                    "addresses": anketa.validAddress,
                },
                {
                    "view": "Адрес регистрации",
                    "addresses": anketa.regAddress,
                },
            ],
            "contacts": [
                {"view": "Телефон", "contact": anketa.contactPhone},
                {"view": "Электронная почта", "contact": anketa.email},
            ],
            "educations": [
                {
                    "view": edu.educationType,
                    "institution": edu.institutionName,
                    "finished": edu.endYear,
                    "specialty": edu.specialty,
                }
                for edu in anketa.education
                if anketa.education
            ],
            "workplaces": [
                {
                    "starts": work.beginDate,
                    "finished": work.endDate,
                    "now_work": work.currentJob,
                    "workplace": work.name,
                    "addresses": work.address,
                    "reason": work.fireReason,
                    "position": work.position,
                }
                for work in anketa.experience
                if anketa.experience
            ],
            "previous": [
                {
                    "firstname": prev.firstNameBeforeChange,
                    "surname": prev.lastNameBeforeChange,
                    "patronymic": prev.midNameBeforeChange,
                    "changed": prev.yearOfChange,
                    "reason": prev.reason,
                }
                for prev in anketa.nameWasChanged
                if anketa.nameWasChanged
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
                    for aff in anketa.stateOrganizations
                    if anketa.stateOrganizations
                ]
                + [
                    {
                        "view": "Связанные лица работают в государственных организациях",
                        "organization": aff.name,
                    }
                    for aff in anketa.relatedPersonsOrganizations
                    if anketa.relatedPersonsOrganizations
                ]
                + [
                    {
                        "view": "Являлся государственным или муниципальным служащим",
                        "organization": aff.name,
                    }
                    for aff in anketa.publicOfficeOrganizations
                    if anketa.publicOfficeOrganizations
                ]
            ),
        }
    except ValidationError as e:
        current_app.logger.exception(e)
        return {}

