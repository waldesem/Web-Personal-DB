"""Utils module."""

import re
from pathlib import Path

from flask import current_app
from sqlalchemy import select

from app.model.models import AnketaJson
from app.model.tables import (
    Addresses,
    Affilations,
    Contacts,
    Documents,
    Educations,
    Persons,
    Previous,
    Staffs,
    Users,
    Workplaces,
    db_session,
)


def upload_resume(resume: dict, user: Users) -> int:
    """Upload a resume to the database.

    Args:
        resume (dict): The resume to be uploaded.
        user (Users): The user who uploaded the resume.

    Returns:
        int: The ID of the uploaded resume.

    """
    if not re.match(r"^[А-ЯЁ]", resume["surname"]):  # noqa: RUF001
        return None

    resume.update({"editable": True, "user_id": user.id, "region": user.region})
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
        destination.mkdir(exist_ok=True)
        person.destination = str(destination)
        db_session.commit()
        return person.id

    if person.editable or person.region != resume["region"]:
        return None

    for k, v in resume.items():
        setattr(person, k, v)
    db_session.commit()
    return person.id


def get_items(anketa: AnketaJson, person_id: int, user_id: int) -> list:
    """Get the anketa items.

    Args:
        anketa (AnketaSchemaJson): The anketa data.
        person_id (int): The ID of the person.
        user_id (int): The ID of the user.

    Returns:
        list: The anketa items.

    """
    return [
        Staffs(
            position=anketa.position_name,
            department=anketa.department,
            person_id=person_id,
            user_id=user_id,
        ),
        Documents(
            view="Паспорт",
            digits=anketa.digits,
            series=anketa.series,
            issue=anketa.issue,
            agency=anketa.agency,
            person_id=person_id,
            user_id=user_id,
        ),
        Addresses(
            view="Адрес проживания",
            addresses=anketa.valid_address,
            person_id=person_id,
            user_id=user_id,
        ),
        Addresses(
            view="Адрес регистрации",
            addresses=anketa.reg_address,
            person_id=person_id,
            user_id=user_id,
        ),
        Contacts(
            view="Телефон",
            contact=anketa.contact_phone,
            person_id=person_id,
            user_id=user_id,
        ),
        Contacts(
            view="Электронная почта",
            contact=anketa.email,
            person_id=person_id,
            user_id=user_id,
        ),
        *[
            Educations(
                view=edu.education_type,
                institution=edu.institution_name,
                finished=edu.end_year,
                specialty=edu.specialty,
                person_id=person_id,
                user_id=user_id,
            )
            for edu in anketa.education
        ],
        *[
            Workplaces(
                starts=work.begin_date,
                finished=work.end_date,
                now_work=work.current_job,
                workplace=work.name,
                addresses=work.address,
                reason=work.fire_reason,
                position=work.position,
                person_id=person_id,
                user_id=user_id,
            )
            for work in anketa.experience
        ],
        *[
            Previous(
                firstname=prev.first_name,
                surname=prev.last_name,
                patronymic=prev.mid_name,
                changed=prev.year_change,
                reason=prev.reason,
                person_id=person_id,
                user_id=user_id,
            )
            for prev in anketa.name_was_changed
        ],
        *[
            Affilations(
                view="Участвует в деятельности коммерческих организаций",
                organization=aff.name,
                inn=aff.inn,
                person_id=person_id,
                user_id=user_id,
            )
            for aff in anketa.organizations
        ],
        *[
            Affilations(
                view="Являлся государственным должностным лицом",
                organization=aff.name,
                person_id=person_id,
                user_id=user_id,
            )
            for aff in anketa.state_organizations
        ],
        *[
            Affilations(
                view="Связанные лица работают в государственных организациях",
                organization=aff.name,
                person_id=person_id,
                user_id=user_id,
            )
            for aff in anketa.related_organizations
        ],
        *[
            Affilations(
                view="Являлся государственным или муниципальным служащим",
                organization=aff.name,
                person_id=person_id,
                user_id=user_id,
            )
            for aff in anketa.public_organizations
        ],
    ]
