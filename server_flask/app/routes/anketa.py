"""Anketa routes."""

import shutil
from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify

from app.depends.depend import current_user, roles_required, validate
from app.model.classes import Roles
from app.model.models import Region
from app.model.tables import Persons, db_session

bp = Blueprint("anketa", __name__, url_prefix="/anketa")


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
            person.editable = True
    else:
        person.editable = not person.editable
    db_session.commit()
    return jsonify(person.to_dict()), 201
