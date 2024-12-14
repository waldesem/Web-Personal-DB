"""File routes."""

import subprocess
from datetime import datetime
from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify, request
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
        destination = request.args.get("destination")
        if not destination:
            person = db_session.get(Persons, person_id)
            destination = Path(
                current_app.config["BASE_PATH"],
                current_user.get("region"),
                person.surname[0],
                f"{person.id}-{person.surname} {person.firstname} "
                f"{person.patronymic}".rstrip(),
            )
            person.destination = str(destination)
            db_session.commit()
        try:
            subprocess.run(f'explorer "{destination}"', check=False)  # noqa: S603
        except subprocess.CalledProcessError:
            current_app.logger.exception("Error opening folder")
        return "", 200

    @validate()
    @roles_required(Roles.user.value)
    def post(self, item: str, file_data: list[File]) -> Response:
        """Upload a file to the server.

        Args:
            item (str): The name of the item.
            file_data (list[File]): The file data.

        Returns:
            The HTTP status code is 200.

        """
        destination = request.args.get("destination")
        if not destination:
            return jsonify({"message": "error"}), 200
        item_path = Path(destination, item)
        Path.mkdir(item_path, exist_ok=True)
        date_subfolder = Path(
            item_path,
            datetime.now().strftime("%Y-%m-%d"),  # noqa: DTZ005
        )
        Path.mkdir(date_subfolder, exist_ok=True)
        for files in file_data:
            file_path = Path(date_subfolder, files.filename)
            if not file_path.is_file():
                files.file.save(file_path)
        return jsonify({"message": "success"}), 201


file_view = FileView.as_view("file_view")
bp.add_url_rule("/<int:person_id>", view_func=file_view, methods=["GET"])
bp.add_url_rule("/<item>", view_func=file_view, methods=["POST"])
