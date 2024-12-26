"""File routes."""

from datetime import datetime
from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify

from app.depends.depend import current_user, jwt_required, roles_required, validate
from app.model.classes import Roles
from app.model.models import File
from app.model.tables import Persons, db_session

bp = Blueprint("file", __name__, url_prefix="/file")


@@bp.post("/<item>/<int:person_id>")
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
                ),
            )
            destination.mkdir(exist_ok=True)
            person.destination = str(destination)
            db_session.commit():
        subfolder = Path(
            person.destination, item,
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
