"""Route routes."""

from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify, request, send_file

from app.depends.depend import current_user, roles_required
from app.model.classes import Roles
from app.model.tables import Persons, db_session

bp = Blueprint("explorer", __name__, url_prefix="/explorer")


def get_folders_and_files(path: str) -> tuple:
    """Update the file manager for the user.

    Returns:
        tuple: A tuple containing the file manager and a 200 status code.

    """
    if path and Path(path).is_dir():
        folders = [
            {
                "name": folder.name,
                "path": str(folder),
            }
            for folder in Path(path).iterdir()
            if folder.is_dir()
        ]
        files = [
            {
                "name": file.name,
                "path": str(file),
            }
            for file in Path(path).iterdir()
            if file.is_file()
        ]
        return folders, files
    return [], []


@bp.get("/home/<int:person_id>")
@roles_required(Roles.user.value)
def get_explorer(person_id: int) -> Response:
    """Update the file manager for the user.

    Returns:
        tuple: A tuple containing the file manager and a 200 status code.

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
        person.destination = str(destination)
        db_session.commit()
    if not Path(person.destination).is_dir():
        Path(person.destination).mkdir(exist_ok=True)
    folders, files = get_folders_and_files(person.destination)
    return jsonify({"folders": folders, "files": files}), 200


@bp.get("/folder")
@roles_required(Roles.user.value)
def get_explorer_folder() -> Response:
    """Update the file manager for the user.

    Returns:
        tuple: A tuple containing the file manager and a 200 status code.

    """
    path = request.args.get("path")
    folders, files = get_folders_and_files(path)
    return jsonify({"folders": folders, "files": files}), 200


@bp.get("/file")
@roles_required(Roles.user.value)
def get_explorer_file() -> Response:
    """Retrieve a file from the server.

    Args:
        path (str): The path to the file.

    Returns:
        tuple: A tuple containing the file and a 200 status code.

    """
    path = request.args.get("path")
    if not Path(path).is_file():
        return "", 404
    return send_file(path, as_attachment=True), 200
