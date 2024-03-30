from datetime import datetime
import os
import shutil

from flask import abort, request, send_file
from flask.views import MethodView
from werkzeug.utils import secure_filename
from PIL import Image

from config import Config
from . import bp
from .login import roles_required
from ..utils.create_folders import create_folders
from ..utils.json_parser import parse_json
from .resume import ResumeView
from ..models.classes import Roles
from ..models.model import (
    db,
    Staff,
    Document,
    Address,
    Contact,
    Workplace,
    Affilation,
    Person,
)

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
        if not request.files["file"].filename:
            return abort(400)

        if action == "anketa":
            file = request.files["file"]
            filename = secure_filename(file.filename)
            temp_path = os.path.join(
                Config.BASE_PATH,
                f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}\
                                        -{filename}',
            )
            file.save(temp_path)
            anketa = parse_json(temp_path)
            person_id = ResumeView.add_resume(anketa["resume"], "create")
            self.fill_items(anketa, person_id)

            person = db.session.get(Person, person_id)
            if person.path:
                full_path = os.path.join(Config.BASE_PATH, person.path)
                if not os.path.isdir(full_path):
                    os.mkdir(full_path)
            else:
                person.path = os.path.join(
                    person.surname[0].upper(),
                    f"{person_id}-{person.surname} {person.firstname} {person.patronymic}",
                )
                url = os.path.join(Config.BASE_PATH, person.path)
                if not os.path.isdir(url):
                    os.mkdir(url)
            db.session.commit()

            action_folder = create_folders(
                person_id, person.surname, person.firstname, person.patronymic, action
            )

            save_path = os.path.join(Config.BASE_PATH, action_folder, filename)
            if not os.path.isfile(save_path):
                try:
                    shutil.move(temp_path, save_path)
                except Exception as e:
                    print(e)
            return {"message": person_id}

        else:
            files = request.files.getlist("file")
            person = db.session.get(Person, item_id)
            folder = create_folders(
                item_id, person.surname, person.firstname, person.patronymic, action
            )
            if action == "image":
                im = Image.open(files[0])
                rgb_im = im.convert("RGB")
                image_path = os.path.join(folder, "image", "image.jpg")
                if os.path.isfile(image_path):
                    os.remove(image_path)
                rgb_im.save(image_path)
                person.path = folder
                db.session.commit()
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
            return "", 201

    def fill_items(self, anketa, person_id):
        models = [Staff, Document, Address, Contact, Workplace, Affilation]
        items_lists = [
            anketa["staff"],
            anketa["passport"],
            anketa["addresses"],
            anketa["contacts"],
            anketa["workplaces"],
            anketa["affilation"],
        ]
        for model, items in zip(models, items_lists):
            for item in items:
                if item:
                    db.session.add(model(**item | {"person_id": person_id}))
        db.session.commit()


file_view = FileView.as_view("file")
bp.add_url_rule("/file/<action>/<int:item_id>", view_func=file_view, methods=["POST"])
