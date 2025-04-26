"""Anketa routes."""

import json
import shutil
from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify
from pydantic import ValidationError

from app.depends.depend import current_user, roles_required, validate
from app.model.classes import Roles
from app.model.models import AnketaJson, File, Person, Region
from app.model.tables import Persons, db_session
from app.utils.utils import upload_items, upload_resume

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
    person_id, existed = upload_resume(json_data.dict())
    return jsonify(
        {"person_id": person_id, "exists": existed},
    ), 201


@bp.post("/json")
@validate()
@roles_required(Roles.user.value, Roles.api.value)
def post_json(file_data: list[File]) -> Response:
    """Create a new person or updates an existing person based on the provided data.

    Args:
        file_data (File): The data to create or update the person.

    Returns:
        A JSON response containing the person ID and an HTTP status code of 201.

    """
    try:
        json_data = json.load(file_data[0].file)
        anketa = AnketaJson(**json_data)
        resume = {
            "surname": anketa.surname,
            "firstname": anketa.firstname,
            "patronymic": anketa.patronymic,
            "birthday": anketa.birthday,
            "birthplace": anketa.birthplace,
            "citizenship": anketa.citizen,
            "dual": anketa.dual,
            "marital": anketa.marital,
            "inn": anketa.inn,
            "snils": anketa.snils,
        }
        person_id, existed = upload_resume(resume)
        if person_id:
            upload_items(anketa, person_id)
            return jsonify(
                {"person_id": person_id, "exists": existed},
            ), 201
    except ValidationError:
        current_app.logger.exception("Validation error")
    except json.JSONDecodeError:
        current_app.logger.exception("JSONDecodeError")
    except TypeError:
        current_app.logger.exception("TypeError")
    return jsonify({"person_id": None, "exists": False}), 200


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
    destination = Path(
        current_app.config["BASE_PATH"],
        query_data.region,
        person.surname[0],
        f"{person_id}-{person.surname} {person.firstname} "
        f"{person.patronymic}".rstrip(),
    )
    try:
        shutil.copytree(person.destination, destination, dirs_exist_ok=True)
        person.destination = str(destination)
        person.region = query_data.region
        person.editable = False
        db_session.commit()
        return jsonify({"message": "success"}), 201
    except shutil.Error:
        current_app.logger.exception("Exception in change_region")
        db_session.rollback()
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
    if person.user_id != current_user.id:
        if person.editable:
            person.editable = False
        else:
            person.user_id = current_user.id
    else:
        person.editable = not person.editable
    db_session.commit()
    return jsonify(person.to_dict()), 201
