"""Anketa routes."""

import json
import shutil
from datetime import datetime
from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify
from pydantic import ValidationError
from sqlalchemy import text

from app.depends.depend import current_user, roles_required, validate
from app.model.classes import Roles
from app.model.models import AnketaSchemaJson, File, Person, Region
from app.model.tables import Persons, db_session
from app.utils.utils import get_anketa_items, upload_resume

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
        current_app.logger.warning("The file does not have a .json file extension")
        return jsonify({"person_id": None})

    json_data = json.load(file_data.file)
    try:
        anketa = AnketaSchemaJson(**json_data)
        resume = {
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
        }
        person_id = upload_resume(resume)
        if not person_id:
            current_app.logger.warning("person_id is None")
            return jsonify({"person_id": person_id})

        items = get_anketa_items(anketa, person_id)
        if items:
            db_session.add_all(items)
            db_session.commit()
        return jsonify({"person_id": person_id}), 201
    except ValidationError:
        current_app.logger.exception("Validation error")
        return jsonify({"person_id": None}), 200


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
    stmt = text(
        "UPDATE persons SET editable = NOT editable, user_id = :user_id \
                WHERE id = :person_id",
    )
    db_session.execute(stmt, {"user_id": current_user.id, "person_id": person_id})
    db_session.commit()
    return jsonify({"message": "success"}), 201


@bp.post("/files/<item>/<int:person_id>")
@validate()
@roles_required(Roles.user.value)
def post(item: str, person_id: int, file_data: list[File]) -> Response:
    """Upload a file to the server.

    Args:
        item (str): The name of the item.
        person_id (int): The ID of the person.
        file_data (list[File]): The file data.

    Returns:
        The HTTP status code is 200.

    """
    person = db_session.get(Persons, person_id)
    if not person.destination:
        destination = Path(
            current_app.config["BASE_PATH"],
            current_user.region,
            person.surname[0],
            f"{person.id}-{person.surname} {person.firstname} "
            f"{person.patronymic}".rstrip(),
        )
        destination.mkdir(exist_ok=True)
        person.destination = str(destination)
        db_session.commit()
    subfolder = Path(
        person.destination,
        item,
        datetime.now().strftime("%Y-%m-%d"),  # noqa: DTZ005
    )
    subfolder.mkdir(parents=True, exist_ok=True)
    for files in file_data:
        if not files:
            continue
        file_path = Path(subfolder, files.filename)
        if not file_path.is_file():
            files.file.save(file_path)

    return jsonify({"message": "success"}), 201
