import os
import subprocess
from datetime import datetime

from flask import Blueprint, current_app, request
from flask.views import MethodView

from ..depends.depend import current_user, jwt_required, roles_required, validate
from ..model.classes import Roles
from ..model.models import File
from ..model.tables import Persons, db_session

bp = Blueprint("file", __name__, url_prefix="/file")


class FileView(MethodView):
    @jwt_required()
    def get(self, person_id):
        destination = request.args.get("destination")
        if not destination:
            person = db_session.get(Persons, person_id)
            destination = os.path.join(
                current_app.config["BASE_PATH"],
                current_user.get("region"),
                person.surname[0],
                f"{person.id}-{person.surname} {person.firstname} "
                f"{person.patronymic}".rstrip(),
            )
            person.destination = destination
            db_session.commit()
        try:
            subprocess.run(f'explorer "{destination}"', timeout=10)
        except subprocess.CalledProcessError as e:
            current_app.logger.exception(e)
        return "", 200

    @validate()
    @roles_required(Roles.user.value)
    def post(self, item, file_data: list[File]):
        destination = request.args.get("destination")
        if not destination:
            return "", 400
        date_subfolder = os.path.join(
            destination,
            item,
            datetime.now().strftime("%Y-%m-%d"),
        )
        os.makedirs(date_subfolder, exist_ok=True)
        for files in file_data:
            file_path = os.path.join(date_subfolder, files.filename)
            if not os.path.isfile(file_path):
                files.file.save(file_path)
        return "", 201


file_view = FileView.as_view("file_view")
bp.add_url_rule("/<int:person_id>", view_func=file_view, methods=["GET"])
bp.add_url_rule("/<item>", view_func=file_view, methods=["POST"])
