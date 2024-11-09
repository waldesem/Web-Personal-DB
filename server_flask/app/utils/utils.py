import os
import re

from flask import current_app
from pydantic import ValidationError
from sqlalchemy import select

from ..depends.depend import current_user
from ..model.models import Person
from ..model.tables import Persons, db_session


def upload_resume(resume: dict):
    """
    Updates a resume in the database with the provided data.

    Args:
        data (dict): A dictionary containing the resume data.

    Returns:
        int: The ID of the updated resume.

    Raises:
        Exception: If there is an error updating the resume.

    """
    try:
        resume = Person(**resume).dict()
    except ValidationError as e:
        current_app.logger.warning(e)
        return None
    if not re.match(r"[А-ЯЁЙ]", resume["surname"][0]):
        return None
    resume["editable"] = True
    resume["user_id"] = current_user.get("id")
    resume["region"] = current_user.get("region")
    person = db_session.execute(
        select(Persons).where(
            Persons.surname.ilike("%{}%".format(resume["surname"])),
            Persons.firstname.ilike("%{}%".format(resume["firstname"])),
            Persons.patronymic.ilike("%{}%".format(resume["patronymic"])),
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
            f"{person.id}-{resume["surname"]} {resume["firstname"]} "
            f"{resume.get("patronymic", "")}".rstrip().upper(),
        )
        if not os.path.isdir(person.destination):
            os.mkdir(person.destination)
        db_session.commit()
        return person.id

    if person.editable or resume["region"] != person.region:
        return None

    resume["id"] = person.id
    resume["user_id"] = current_user.get("id")
    db_session.merge(Persons(**resume))
    db_session.commit()
    return person.id


def json_to_dict(json_dict: dict):
    return {
        "resume": {
            "region": current_user.get("region"),
            "surname": json_dict.get("lastName"),
            "firstname": json_dict.get("firstName"),
            "patronymic": json_dict.get("midName"),
            "birthday": json_dict.get("birthday"),
            "birthplace": json_dict.get("birthplace"),
            "citizenship": json_dict.get("citizen"),
            "dual": json_dict.get("additionalCitizenship"),
            "marital": json_dict.get("maritalStatus"),
            "inn": json_dict.get("inn"),
            "snils": json_dict.get("snils"),
        },
        "staffs": [
            {
                "position": json_dict.get("positionName"),
                "department": json_dict.get("department"),
            }
        ],
        "documents": [
            {
                "view": "Паспорт",
                "digits": json_dict.get("passportNumber"),
                "series": json_dict.get("passportSerial"),
                "issue": json_dict.get("passportIssueDate"),
                "agency": json_dict.get("passportIssuedBy"),
            }
        ],
        "addresses": [
            {
                "view": "Адрес проживания",
                "addresses": json_dict.get("validAddress"),
            },
            {
                "view": "Адрес регистрации",
                "addresses": json_dict.get("regAddress"),
            },
        ],
        "contacts": [
            {"view": "Телефон", "contact": json_dict.get("contactPhone")},
            {"view": "Электронная почта", "contact": json_dict.get("email")},
        ],
        "educations": [
            {
                "view": edu.get("educationType"),
                "institution": edu.get("institutionName"),
                "finished": edu.get("endYear"),
                "specialty": edu.get("specialty"),
            }
            for edu in json_dict.get("education")
            if json_dict.get("education")
        ],
        "workplaces": [
            {
                "starts": work.get("beginDate"),
                "finished": work.get("endDate"),
                "now_work": work.get("currentJob"),
                "workplace": work.get("name"),
                "addresses": work.get("address"),
                "reason": work.get("fireReason"),
                "position": work.get("position"),
            }
            for work in json_dict.get("experience")
            if json_dict.get("experience")
        ],
        "previous": [
            {
                "firstname": prev.get("firstNameBeforeChange"),
                "surname": prev.get("lastNameBeforeChange"),
                "patronymic": prev.get("midNameBeforeChange"),
                "changed": prev.get("yearOfChange"),
                "reason": prev.get("reason"),
            }
            for prev in json_dict.get("nameWasChanged")
            if json_dict.get("nameWasChanged")
        ],
        "affilations": (
            [
                {
                    "view": "Участвует в деятельности коммерческих организаций",
                    "organization": aff.get("name"),
                    "inn": aff.get("inn"),
                }
                for aff in json_dict.get("organizations")
                if json_dict.get("organizations")
            ]
            + [
                {
                    "view": "Являлся государственным должностным лицом",
                    "organization": aff.get("name"),
                }
                for aff in json_dict.get("stateOrganizations")
                if json_dict.get("stateOrganizations")
            ]
            + [
                {
                    "view": "Связанные лица работают в государственных организациях",
                    "organization": aff.get("name"),
                }
                for aff in json_dict.get("relatedPersonsOrganizations")
                if json_dict.get("relatedPersonsOrganizations")
            ]
            + [
                {
                    "view": "Являлся государственным или муниципальным служащим",
                    "organization": aff.get("name"),
                }
                for aff in json_dict.get("publicOfficeOrganizations")
                if json_dict.get("publicOfficeOrganizations")
            ]
        ),
    }

