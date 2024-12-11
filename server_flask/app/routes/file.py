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
    def get(self, item):
        destination = request.args.get("destination")
        if item == "folder" and os.path.isdir(destination):
            try:
                subprocess.run(f'explorer "{destination}"', timeout=10)
            except subprocess.CalledProcessError as e:
                current_app.logger.exception(e)
        return "", 200

    @validate()
    @roles_required(Roles.user.value)
    def post(self, item, item_id, file_data: list[File]):
        person = db_session.get(Persons, item_id)
        if not person.destination:
            person.destination = os.path.join(
                current_app.config["BASE_PATH"],
                current_user.get("region"),
                person.surname[0],
                f"{person.id}-{person.surname} {person.firstname} "
                f"{person.patronymic if person.patronymic else ''}".rstrip().upper(),
            )
            db_session.commit()
        date_subfolder = os.path.join(
            person.destination,
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
bp.add_url_rule("/<item>", view_func=file_view, methods=["GET"])
bp.add_url_rule("/<item>/<int:item_id>", view_func=file_view, methods=["POST"])
