"""Anketa routes."""

import shutil
from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify

from app.depends.depend import current_user, roles_required, validate
from app.model.classes import Roles
from app.model.models import File, Person, Region
from app.model.tables import Base, Persons, db_session
from app.utils.utils import json_to_dict, upload_resume

bp = Blueprint("anketa", __name__, url_prefix="/anketa")


@bp.post("/resume")
@validate()
@roles_required(Roles.user.value)
def post_resume(json_data: Person) -> Response:
    """Create a new person or updates an existing person based on the provided data.

    Args:
        json_data (Person): The data to create or update the person.

    Returns:
        A JSON response containing the person ID and an HTTP status code of 201.

    """
    person_id = upload_resume(json_data.dict())
    return jsonify({"person_id": person_id})


@bp.post("/json")
@validate()
@roles_required(Roles.user.value)
def post_file(file_data: File) -> Response:
    """Create a new person or updates an existing person based on the provided data.

    Args:
        file_data (File): The data to create or update the person.

    Returns:
        A JSON response containing the person ID and an HTTP status code of 201.

    """
    if not file_data.filename.endswith(".json"):
        return jsonify({"person_id": None})

    anketa = json_to_dict(file_data.file)
    person_id = upload_resume(anketa.pop("resume")) if "resume" in anketa else None
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
def change_region(person_id: int, query_data: Region) -> Response:
    """Change a person's region in the database based on their person ID.

    Args:
        person_id (int): The ID of the person.
        query_data (Region): The data to change the person's region.

    Returns:
        The HTTP status code is 200.

    """
    person = db_session.get(Persons, person_id)
    if query_data.region != person.region:
        if person.destination and Path(person.destination).is_dir():
            destination = Path(
                current_app.config["BASE_PATH"],
                query_data.region,
                person.surname[0],
                f"{person_id}-{person.surname} {person.firstname} "
                f"{person.patronymic if person.patronymic else ''}".rstrip(),
            )
            shutil.copytree(person.destination, destination, dirs_exist_ok=True)
            person.destination = str(destination)
        person.region = query_data.region
        person.editable = False
        db_session.commit()
        return jsonify({"message": "success"}), 201
    return jsonify({"message": "error"}), 200


@bp.get("/self/<int:person_id>")
@roles_required(Roles.user.value)
def change_self_id(person_id: int) -> Response:
    """Toggle the editable status of a person with the given item ID.

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
