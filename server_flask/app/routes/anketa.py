"""Anketa routes."""

from datetime import datetime
from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from app.depends.depend import auth_required, current_user, validate
from app.structures.classes import Roles
from app.structures.models import Region
from app.structures.tables import Base, Persons, db_session
from app.utils.utilities import check_filename, create_destination

bp = Blueprint("anketa", __name__, url_prefix="/anketa")


@bp.get("/profile/<int:person_id>")
@auth_required()
def get_profile(person_id: int) -> Response:
    """Get candidate profile.

    Args:
        person_id (int): The ID of the person.

    Returns:
        Tuple[Response, int]: A tuple containing the JSON response containing
            the retrieved item(s) and an HTTP status code of 200.

    """
    person = db_session.get(Persons, person_id)
    if not person.destination or not Path(person.destination).is_dir():
        person.destination = create_destination(person)
        db_session.commit()
    profile = {"person": person.to_dict()}

    # Получаем все связанные таблицы из метаданных SQLAlchemy
    for name, table in Base.metadata.tables.items():
        if name not in ["persons", "phones", "users"]:
            # Получаем все записи из таблицы и добавляем их в словарь profile
            profile[name] = sorted(
                [item.to_dict() for item in getattr(person, table.name)],
                key=lambda x: x["id"],
                reverse=True,
            )
    return jsonify(profile), 200


@bp.post("/region/<int:person_id>")
@validate
@auth_required(Roles.user.value)
def change_region(person_id: int, json_data: Region) -> Response:
    """Change a person's region in the database based on their person ID.

    Args:
        person_id (int): The ID of the person.
        json_data (Region): The data to change the person's region.

    Returns:
        The HTTP status code is 200.

    """
    try:
        person = db_session.get(Persons, person_id)
        person.region = json_data.region
        destination = create_destination(person)
        if person.destination:
            Path(person.destination).rename(destination)
        person.destination = destination
        person.editable = False
        db_session.commit()
        return jsonify({"message": "success"}), 201
    except SQLAlchemyError:
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
    try:
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
    except SQLAlchemyError:
        current_app.logger.exception("Exception in change_self_id")
        return jsonify({"message": "error"}), 200


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
