import os

from flask import current_app
from sqlalchemy import desc, select

from ..depends.depend import current_user
from ..model.models import Person
from ..model.tables import Users, db_session, Persons, tables_models
from ..tools.jsonylize import parse_json


def handle_get_item(item, item_id):
    query = db_session.execute(
        select(tables_models[item], Users.fullname)
        .filter(
            tables_models[item].person_id == item_id,
            tables_models[item].user_id == Users.id,
        )
        .order_by(desc(tables_models[item].id))
    ).all()
    result = []
    for row in query:
        item = row[0].to_dict()
        item["user"] = row[1]
        result.append(item)
    return result


def handle_post_resume(data):
    """
    Updates a resume in the database with the provided data.

    Args:
        data (dict): A dictionary containing the resume data.

    Returns:
        int: The ID of the updated resume.

    Raises:
        Exception: If there is an error updating the resume.

    """
    resume = Person(**data).dict()
    resume["standing"] = True
    resume["user_id"] = current_user.id
    if not resume.get("id"):
        person = db_session.execute(
            select(Persons).where(
                Persons.surname.ilike("%{}%".format(resume["surname"])),
                Persons.firstname.ilike("%{}%".format(resume["firstname"])),
                Persons.patronymic.ilike("%{}%".format(resume["patronymic"])),
                Persons.birthday == resume["birthday"],
            )
        ).scalar_one_or_none()
        if person:
            resume["id"] = person.id
    result = db_session.merge(Persons(**resume))
    db_session.flush()

    person_dir = os.path.join(
        current_app.config["BASE_PATH"],
        resume["region"],
        resume["surname"][0].upper(),
        f"{result.id}-{resume['surname'].upper()} "
        f"{resume['firstname'].upper()} "
        f"{resume.get('patronymic', '').upper()}".rstrip(),
    )
    if not os.path.isdir(person_dir):
        os.mkdir(person_dir)
    result.destination = person_dir
    db_session.commit()
    return result.id


def handle_update_person(json_data):
    """
    Updates a person's information in the database.

    Args:
        json_data (str): The JSON data containing the person's information.

    Returns:
        int: The ID of the updated person.

    Raises:
        Exception: If there is an error updating the person's information.

    """
    anketa = parse_json(json_data)
    person_id = None
    if anketa:
        person_id = handle_post_resume(anketa["resume"])
        if person_id:
            for table, contents in anketa.items():
                if table == "resume" or not contents:
                    continue
                [
                    content.update(
                        {"person_id": person_id, "user_id": current_user.id}
                    )
                    for content in contents
                ]
                db_session.add_all(tables_models[table](**item) for item in contents)
            db_session.commit()
    return person_id
