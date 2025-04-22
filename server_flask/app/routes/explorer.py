"""Route routes."""

from datetime import datetime
from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify, request, send_file

from app.depends.depend import current_user, roles_required, validate
from app.model.classes import Roles
from app.model.models import File
from app.model.tables import Persons, db_session

bp = Blueprint("explorer", __name__, url_prefix="/explorer")


@bp.get("/folder/<int:person_id>")
@roles_required(Roles.user.value)
def get_folder(person_id: int) -> Response:
    """Update the file manager for the user.

    Returns:
        tuple: A tuple containing the file manager and a 200 status code.

    """
    path = request.args.get("path")
    if not path:
        person = db_session.get(Persons, person_id)
        if not person.destination:
            person.destination = str(
                Path(
                    current_app.config["BASE_PATH"],
                    current_user.region,
                    person.surname[0],
                    f"{person.id}-{person.surname} {person.firstname} "
                    f"{person.patronymic}".rstrip(),
                ),
            )
            db_session.commit()
        path = person.destination
    path = Path(path).resolve()
    if not path.is_dir():
        path.mkdir(parents=True, exist_ok=True)
    try:
        folders = [
            {
                "name": folder.name,
                "path": str(folder),
            }
            for folder in path.iterdir()
            if folder.is_dir()
        ]
        files = [
            {
                "name": file.name,
                "path": str(file),
            }
            for file in path.iterdir()
            if file.is_file()
        ]
        return jsonify({"path": str(path), "folders": folders, "files": files}), 200
    except PermissionError:
        return jsonify({"path": str(path), "folders": [], "files": []}), 200


@bp.get("/file")
@roles_required(Roles.user.value)
def get_file() -> Response:
    """Retrieve a file from the server.

    Args:
        path (str): The path to the file.

    Returns:
        tuple: A tuple containing the file and a 200 status code.

    """
    path = request.args.get("path")
    if not Path(path).is_file():
        return "", 404
    return send_file(path, as_attachment=True, mimetype="application/octet-stream"), 200


@bp.post("/files/<item>/<int:person_id>")
@validate()
@roles_required(Roles.user.value)
def post_files(item: str, person_id: int, file_data: list[File]) -> Response:
    """Upload a file to the server.

    Args:
        item (str): The name of the item.
        person_id (int): The ID of the person.
        file_data (list[File]): The file data.

    Returns:
        The HTTP status code is 200.

    """
    person = db_session.get(Persons, person_id)
    subfolder = Path(
        person.destination,
        item,
        datetime.now().strftime("%Y-%m-%d"),
    )
    subfolder.mkdir(parents=True, exist_ok=True)
    for data in file_data:
        file_path = Path(subfolder, data.filename)
        if not file_path.is_file():
            data.file.save(file_path)

    return jsonify({"message": "success"}), 201
