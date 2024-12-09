import imghdr
import os
import subprocess
from datetime import datetime

from flask import Blueprint, current_app, jsonify, send_file
from flask.views import MethodView
from PIL import Image

from ..depends.depend import current_user, roles_required, validate
from ..model.classes import Roles
from ..model.models import File
from ..model.tables import Persons, db_session


bp = Blueprint("file", __name__, url_prefix="/file")


class FileView(MethodView):
    decorators = [roles_required(Roles.user.value)]

    def __init__(self):
        self.person = None

    def initialize(self, item_id):
        self.person = db_session.get(Persons, item_id)
        if not self.person.destination or not os.path.isdir(self.person.destination):
            self.person.destination = os.path.join(
                current_app.config["BASE_PATH"],
                current_user.get("region"),
                self.person.surname[0],
                f"{self.person.id}-{self.person.surname} {self.person.firstname} "
                f"{self.person.patronymic if self.person.patronymic else ''}".rstrip().upper(),
            )
            os.makedirs(self.person.destination, exist_ok=True)
            db_session.commit()

    def get(self, item, item_id):
        self.initialize(item_id)
        if item == "folder":
            try:
                subprocess.run(f'explorer "{self.person.destination}"', timeout=10)
            except subprocess.CalledProcessError as e:
                current_app.logger.exception(e)
            return "", 200
        elif item == "image":
            file_path = os.path.join(self.person.destination, "image", "image.jpg")
            if os.path.isfile(file_path):
                return send_file(file_path, as_attachment=True, mimetype="image/jpg")
            return send_file(
                "static/no-photo.png", as_attachment=True, mimetype="image/jpg"
            )

    @validate()
    def post(self, item, item_id, file_data: list[File]):
        self.initialize(item_id)
        item_dir = os.path.join(self.person.destination, item)
        os.makedirs(item_dir, exist_ok=True)

        if not file_data:
            return jsonify({"message": "error"}), 200

        if item == "image":
            if imghdr.what(file_data[0].file) is not None:
                image = Image.open(file_data[0].file)
                image = image.convert("RGB")
                new_file = os.path.join(item_dir, "image.jpg")
                if os.path.isfile(new_file):
                    os.remove(new_file)
                image.save(new_file, format="JPEG", quality=90)
                return jsonify({"message": "success"}), 201
            return jsonify({"message": "error"}), 200

        date_subfolder = os.path.join(
            item_dir,
            datetime.now().strftime("%Y-%m-%d"),
        )
        os.makedirs(date_subfolder, exist_ok=True)
        for files in file_data:
            file_path = os.path.join(date_subfolder, files.filename)
            if not os.path.isfile(file_path):
                files.file.save(file_path)
        return "", 201


file_view = FileView.as_view("file_view")
bp.add_url_rule("/<item>/<int:item_id>", view_func=file_view)