import json
import os
import re
import shutil

from flask import Blueprint, current_app, jsonify
from pydantic import ValidationError
from sqlalchemy import select

from ..depends.depend import current_user, roles_required, validate
from ..model.classes import Roles
from ..model.models import AnketaSchemaJson, Person, Region, File
from ..model.tables import Base, Persons, db_session
from ..utils.utils import json_to_dict


bp = Blueprint("anketa", __name__, url_prefix="/anketa")


def upload(resume: dict):
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


@bp.post("/resume")
@validate()
@roles_required(Roles.user.value)
def post_resume(json_data: Person):
    """
    Creates a new person or updates an existing person based on the provided data.

    Parameters:
        item (str): The name to create or update the person in.

    Returns:
        A JSON response containing the person ID and an HTTP status code of 201.
    """
    person_id = upload(json_data) if json_data else None
    return jsonify({"person_id": person_id})


@bp.post("/json")
@validate()
@roles_required(Roles.user.value)
def post_file(file_data: File):
    if not file_data.filename.endswith(".json"):
        return jsonify({"person_id": None})
    json_dict = json.load(file_data.file)
    try:
        json_dict = AnketaSchemaJson(**json_dict).dict()
    except ValidationError as e:
        current_app.logger.exception(e)
        return jsonify({"person_id": None})

    anketa = json_to_dict(json_dict)
    person_id = upload(anketa.pop("resume"))
    if not person_id:
        current_app.logger.warning("person_id is None")
        return jsonify({"person_id": person_id})

    tablenames = {
        cls.__tablename__: cls
        for cls in Base.__subclasses__()
        if hasattr(cls, "__tablename__")
    }
    items = []
    for tbl, contents in anketa.items():
        if contents:
            for content in contents:
                content["person_id"] = person_id
                content["user_id"] = current_user.get("id")
                table = tablenames.get(tbl)
                items.append(table(**content))
    db_session.bulk_save_objects(items)
    db_session.commit()
    return jsonify({"person_id": person_id}), 201


@bp.get("/region/<int:person_id>")
@validate()
@roles_required(Roles.user.value)
def change_region(person_id, query_data: Region):
    """
    Change a person's region in the database based on their person ID.

    Parameters:
        person_id (int): The ID of the person.

    Returns:
        The HTTP status code is 200.
    """
    person = db_session.get(Persons, person_id)
    if query_data.region != person.region:
        if person.destination and os.path.isdir(person.destination):
            destination = os.path.join(
                current_app.config["BASE_PATH"],
                query_data.region,
                person.surname[0],
                f"{person_id}-{person.surname} {person.firstname} "
                f"{person.patronymic if person.patronymic else ''}".rstrip().upper(),
            )
            shutil.copytree(person.destination, destination, dirs_exist_ok=True)
            person.destination = destination
        person.region = query_data.region
        person.editable = False
        db_session.commit()
        return jsonify({"message": "success"}), 201
    return jsonify({"message": "error"}), 200


@bp.get("/self/<int:person_id>")
@roles_required(Roles.user.value)
def change_self_id(person_id):
    """
    Toggle the editable status of a person with the given item ID.

    The person ID is the ID of the person to toggle the editable status.
    The user ID is the ID of the user currently logged in.

    Returns:
        The HTTP status code is 200.
    """
    person = db_session.get(Persons, person_id)
    person.editable = not person.editable
    person.user_id = current_user.get("id")
    db_session.commit()
    return "", 200
