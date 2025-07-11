"""Anketa routes."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from flask import Blueprint, current_app, request
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.decorators.depend import auth_required, current_user
from app.decorators.validate import serialize, validate
from app.models.models import PersonOut, Region
from app.tables.tables import Persons
from app.utils.utilities import Roles, check_filename, create_destination

bp = Blueprint("anketa", __name__, url_prefix="/anketa")


@bp.post("/region/<int:person_id>")
@serialize()
@validate
@auth_required(Roles.user.value)
def change_region(person_id: int, json_data: Region) -> tuple[str, int]:
    """Change a person's region in the database based on their person ID.

    Args:
        person_id (int): The ID of the person.
        json_data (Region): The data to change the person's region.

    Returns:
        The HTTP status code is 200.

    """
    try:
        person = db.session.get(Persons, person_id)
        person.region = json_data.region
        destination = create_destination(person)
        if person.destination:
            Path(person.destination).rename(destination)
        person.destination = destination
        person.editable = False
        db.session.commit()
    except SQLAlchemyError:
        current_app.logger.exception("Exception in change_region")
        return "error", 500
    else:
        return "success", 201


@bp.get("/self/<int:person_id>")
@serialize(PersonOut)
@auth_required(Roles.user.value)
def change_self_id(person_id: int) -> tuple[str | Persons, int]:
    """Toggle the editable status of a person with the given item ID.

    The person ID is the ID of the person to toggle the editable status.
    The user ID is the ID of the user currently logged in.

    Returns:
        The HTTP status code is 200.

    """
    try:
        person = db.session.get(Persons, person_id)
        if not person.destination or not Path(person.destination).is_dir():
            person.destination = create_destination(person)
            db.session.commit()
        if person.user_id != current_user.id:
            if person.editable:
                person.editable = False
            else:
                person.user_id = current_user.id
                person.editable = True
        else:
            person.editable = not person.editable
        db.session.commit()
    except SQLAlchemyError:
        current_app.logger.exception("Exception in change_self_id")
        return "error", 500
    else:
        return person, 201


@bp.post("/files/<int:person_id>")
@serialize()
@auth_required(Roles.user.value)
def post_files(person_id: int) -> tuple[str, int]:
    """Upload a file to the server.

    Args:
        item (str): The name of the item.
        person_id (int): The ID of the person.
        file_data (list[File]): The file data.

    Returns:
        The HTTP status code is 200.

    """
    file_data = request.files.getlist("file")
    person = db.session.get(Persons, person_id)
    try:
        subfolder = Path(
            person.destination,
            datetime.now().strftime("%d-%m-%Y %H-%M-%S"),
        )
        subfolder.mkdir(parents=True, exist_ok=True)

        for data in file_data:
            secure_filename = check_filename(data.filename)
            if secure_filename:
                file_path = Path(subfolder, secure_filename)
                if not file_path.is_file():
                    data.save(file_path)
    except (TypeError, ValueError, AttributeError):
        current_app.logger.exception("Exception in post_files")
        return "error", 500
    else:
        return "success", 201
