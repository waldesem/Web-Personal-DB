"""Utils module."""

import re
from pathlib import Path

from flask import current_app
from sqlalchemy import select

from app.depends.depend import current_user
from app.model.models import AnketaSchemaJson
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


def upload_resume(resume: dict) -> int:
    """Upload a resume to the database.

    Args:
        resume (dict): The resume to be uploaded.

    Returns:
        int: The ID of the uploaded resume.

    """
    if not re.match(r"[А-ЯЁЙ]", resume["surname"][0]):
        return None
    resume["editable"] = True
    resume["user_id"] = current_user.id
    resume["region"] = current_user.region
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


def get_anketa_items(anketa: AnketaSchemaJson, person_id: int) -> list:  # noqa: D103
    items = [
        Staffs(
            position=anketa.position_name,
            department=anketa.department,
            person_id=person_id,
            user_id=current_user.id,
        ),
        Documents(
            view="Паспорт",
            digits=anketa.passport_number,
            series=anketa.passport_serial,
            issue=anketa.passport_issue,
            agency=anketa.passport_issued,
            person_id=person_id,
            user_id=current_user.id,
        ),
        Addresses(
            view="Адрес проживания",
            addresses=anketa.valid_address,
            person_id=person_id,
            user_id=current_user.id,
        ),
        Addresses(
            view="Адрес регистрации",
            addresses=anketa.reg_address,
            person_id=person_id,
            user_id=current_user.id,
        ),
        Contacts(
            view="Телефон",
            contact=anketa.contact_phone,
            person_id=person_id,
            user_id=current_user.id,
        ),
        Contacts(
            view="Электронная почта",
            contact=anketa.email,
            person_id=person_id,
            user_id=current_user.id,
        ),
    ]
    items.extend(
        [
            Educations(
                view=edu.education_type,
                institution=edu.institution_name,
                finished=edu.end_year,
                specialty=edu.specialty,
                person_id=person_id,
                user_id=current_user.id,
            )
            for edu in anketa.education
        ]
        + [
            Workplaces(
                starts=work.begin_date,
                finished=work.end_date,
                now_work=work.current_job,
                workplace=work.name,
                addresses=work.address,
                reason=work.fire_reason,
                position=work.position,
                person_id=person_id,
                user_id=current_user.id,
            )
            for work in anketa.experience
        ]
        + [
            Previous(
                firstname=prev.first_name,
                surname=prev.last_name,
                patronymic=prev.mid_name,
                changed=prev.year_change,
                reason=prev.reason,
                person_id=person_id,
                user_id=current_user.id,
            )
            for prev in anketa.name_was_changed
        ]
        + [
            Affilations(
                view="Участвует в деятельности коммерческих организаций",
                organization=aff.name,
                inn=aff.inn,
                person_id=person_id,
                user_id=current_user.id,
            )
            for aff in anketa.organizations
        ]
        + [
            Affilations(
                view="Являлся государственным должностным лицом",
                organization=aff.name,
                person_id=person_id,
                user_id=current_user.id,
            )
            for aff in anketa.state_organizations
        ]
        + [
            Affilations(
                view="Связанные лица работают в государственных организациях",
                organization=aff.name,
                person_id=person_id,
                user_id=current_user.id,
            )
            for aff in anketa.related_organizations
        ]
        + [
            Affilations(
                view="Являлся государственным или муниципальным служащим",
                organization=aff.name,
                person_id=person_id,
                user_id=current_user.id,
            )
            for aff in anketa.public_organizations
        ],
    )
    return items
