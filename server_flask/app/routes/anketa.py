"""Anketa routes."""

import shutil
from datetime import datetime
from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from app.depends.depend import auth_required, current_user, validate
from app.model.classes import Roles
from app.model.models import Region
from app.model.tables import Persons, db_session
from app.utils.utils import check_filename, create_destination

bp = Blueprint("anketa", __name__, url_prefix="/anketa")


@bp.get("/region/<int:person_id>")
@validate
@auth_required(Roles.user.value)
def change_region(person_id: int, query_data: Region) -> Response:
    """Change a person's region in the database based on their person ID.

    Args:
        person_id (int): The ID of the person.
        query_data (Region): The data to change the person's region.

    Returns:
        The HTTP status code is 200.

    """
    try:
        person = db_session.get(Persons, person_id)
        person.region = query_data.region
        destination = create_destination(person)
        if person.destination:
            Path(person.destination).rename(destination)
        person.destination = destination
        person.editable = False
        db_session.commit()
        return jsonify({"message": "success"}), 201
    except (shutil.Error, SQLAlchemyError):
        current_app.logger.exception("Exception in change_region")
    return jsonify({"message": "error"}), 200


@bp.get("/self/<int:person_id>")
@auth_required(Roles.user.value)
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


@bp.post("/files/<int:person_id>")
@validate
@auth_required(Roles.user.value)
def post_files(person_id: int) -> Response:
    """Upload a file to the server.

    Args:
        item (str): The name of the item.
        person_id (int): The ID of the person.
        file_data (list[File]): The file data.

    Returns:
        The HTTP status code is 200.

    """
    file_data = request.files.getlist("file")
    person = db_session.get(Persons, person_id)
    if not person.destination:
        person.destination = create_destination(person)
        db_session.commit()
    try:
        subfolder = Path(
            person.destination,
            datetime.now().strftime("%d-%m-%Y %H-%M-%S"),
        )
        subfolder.mkdir(parents=True, exist_ok=True)

        for data in file_data:
            file_path = Path(subfolder, check_filename(data.filename))
            if not file_path.is_file():
                data.save(file_path)

        return jsonify({"message": "success"}), 201
    except Exception:
        current_app.logger.exception("Exception in post_files")
        return jsonify({"message": "error"}), 200
