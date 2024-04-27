import json
import os

from flask import abort, request, send_file
from flask.views import MethodView
from PIL import Image

from config import Config
from . import bp
from .login import roles_required
from ..utils.folders import Folders
from ..utils.parsers import parse_anketa
from ..models.classes import Roles
from ..models.model import db, Person


class FileView(MethodView):

    decorators = [roles_required(Roles.user.value), bp.doc(hide=True)]

    def get(self, item_id):
        """
        Retrieves a file from the server and sends it as a response.
        """
        person = db.session.get(Person, item_id)
        if person.path:
            file_path = os.path.join(
                Config.BASE_PATH, person.path, "image", "image.jpg"
            )
            if os.path.isfile(file_path):
                return send_file(file_path, as_attachment=True)
        return abort(404)

    def post(self, action, item_id=None):
        file = request.files["file"]
        if not file.filename:
            return abort(400)

        if action == "anketa":
            json_dict = json.load(file)
            person_id = parse_anketa(json_dict)
            return {"message": person_id}, 201

        person = db.session.get(Person, item_id)
        folders = Folders(
            person.id, person.surname, person.firstname, person.patronymic
        )
        if action == "image":
            folder = folders.create_parent_folder("image")
            im = Image.open(file)
            rgb_im = im.convert("RGB")
            image_path = os.path.join(folder, "image.jpg")
            if os.path.isfile(image_path):
                os.remove(image_path)
            rgb_im.save(image_path)
            return "", 201

        folder = folders.create_subfolder(action)
        files = request.files.getlist("file")
        for file in files:
            if file.filename:
                if not os.path.isfile(os.path.join(folder, file.filename)):
                    file.save(os.path.join(folder, file.filename))
        return "", 201


file_view = FileView.as_view("file")
bp.add_url_rule("/file/<action>/<int:item_id>", view_func=file_view, methods=["POST"])


@roles_required(Roles.user.value)
@bp.route("/image/<int:item_id>")
@bp.doc(hide=True)
def get_image(item_id):
    """
    Retrieves a file from the server and sends it as a response.
    """
    person = db.session.get(Person, item_id)
    folders = Folders(
        person.id, person.surname, person.firstname, person.patronymic
    )
    file_path = os.path.join(folders.create_main_folder(), "image", "image.jpg")
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True, mimetype="image/jpg")
    return send_file("static/no-photo.png", as_attachment=True, mimetype="image/jpg")
