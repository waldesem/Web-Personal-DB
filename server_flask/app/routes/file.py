"""File routes."""

import subprocess
from datetime import datetime
from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify
from flask.views import MethodView

from app.depends.depend import current_user, jwt_required, roles_required, validate
from app.model.classes import Roles
from app.model.models import File
from app.model.tables import Persons, db_session

bp = Blueprint("file", __name__, url_prefix="/file")


class FileView(MethodView):
    """View for handling file uploads.

    Methods:
        get: Retrieve a file from the server.
        post: Upload a file to the server.

    """

    @validate()
    @jwt_required()
    def get(self, person_id: int) -> Response:
        """Retrieve a file from the server.

        Args:
            person_id (int): The ID of the person.

        Returns:
            The HTTP status code is 200.

        """
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
        try:
            Path(person.destination).mkdir(parents=True, exist_ok=True)
            subprocess.run(f'explorer "{person.destination}"', check=False)  # noqa: S603
        except subprocess.CalledProcessError:
            current_app.logger.exception("Error opening folder")
        return "", 200

    @validate()
    @roles_required(Roles.user.value)
    def post(self, item: str, person_id: int, file_data: list[File]) -> Response:
        """Upload a file to the server.

        Args:
            item (str): The name of the item.
            person_id (int): The ID of the person.
            file_data (list[File]): The file data.

        Returns:
            The HTTP status code is 200.

        """
        destination = db_session.get(Persons, person_id).destination
        if not destination:
            return jsonify({"message": "error"}), 200
        subfolder = Path(
            Path(destination, item),
            datetime.now().strftime("%Y-%m-%d"),  # noqa: DTZ005
        )
        Path(subfolder).mkdir(parents=True, exist_ok=True)
        for files in file_data:
            if not files:
                continue
            file_path = Path(subfolder, files.filename)
            if not file_path.is_file():
                files.file.save(file_path)
        return jsonify({"message": "success"}), 201


file_view = FileView.as_view("file_view")
bp.add_url_rule("/<int:person_id>", view_func=file_view, methods=["GET"])
bp.add_url_rule("/<item>/<int:person_id>", view_func=file_view, methods=["POST"])
