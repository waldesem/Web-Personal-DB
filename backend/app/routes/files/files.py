import os
from datetime import datetime

from flask import request, send_file, abort
from flask.views import MethodView
from werkzeug.utils import secure_filename
from PIL import Image

from config import Config
from . import bp_files
from ... import db
from ...utils.folders import create_folders
from ..login.login import roles_required, group_required
from ...models.classes import Roles, Groups
from ...models.model import (
    Person,
    Check,
    Poligraf,
    Investigation,
)
from ...models.schema import ActionSchema


class FileView(MethodView):
    decorators = [
        group_required(Groups.staffsec.value),
        roles_required(Roles.user.value),
        bp_files.doc(hide=True),
    ]

    def get(self, item_id):
        """
        Retrieves a file from the server and sends it as a response.
        """
        person = db.session.get(Person, item_id)
        file_path = os.path.join(Config.BASE_PATH, person.path, "images", "image.jpg")
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True)
        return abort(404)

    @bp_files.input(ActionSchema, location="query")
    def post(self, query_data, item_id=0):
        action = query_data.get("action")
        if not request.files["file"].filename and action:
            return {"result": False, "item_id": item_id}

        model_mapping = {
            "check": Check,
            "investigation": Investigation,
            "poligraf": Poligraf,
            "image": Person,
        }
        files = request.files.getlist("file")
        model = model_mapping.get(action)
        item = db.session.get(model, item_id)
        person = db.session.get(Person, item.person_id)
        folder = create_folders(person.id, person.fullname, action)
        if action == "image":
            im = Image.open(files[0])
            rgb_im = im.convert("RGB")
            images = os.path.join(Config.BASE_PATH, folder, "images")
            if not os.path.isdir(images):
                os.mkdir(images)
            image_path = os.path.join(images, "image.jpg")
            if os.path.isfile(image_path):
                os.remove(image_path)
            rgb_im.save(image_path)
        else:
            for file in files:
                filename = secure_filename(file.filename)
                for file in files:
                    file.save(
                        os.path.join(
                            Config.BASE_PATH,
                            folder,
                            f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}-{filename}',
                        )
                    )
        return {"message": item_id}


bp_files.add_url_rule("/file/<int:item_id>", view_func=FileView.as_view("file"))
