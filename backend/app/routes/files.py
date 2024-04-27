import os

from flask import abort, request, send_file
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy import select
from PIL import Image

from config import Config
from . import bp
from .login import roles_required
from ..utils.folders import create_folders
from ..utils.json_parser import parse_json
from ..routes.resume import add_resume
from ..models.classes import Roles
from ..models.model import (
    Previous,
    db,
    Staff,
    Document,
    Address,
    Contact,
    Workplace,
    Affilation,
    Person,
    Message,
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
        if action in ["anketa", "image"]:
            file = request.files["file"]
            if not file.filename:
                return abort(400)

            if action == "anketa":
                person_id = parse_anketa(file)
                return {"message": person_id}, 201

            if action == "image":
                person = db.session.get(Person, item_id)
                folder = create_folders(
                    item_id,
                    person.surname,
                    person.firstname,
                    person.patronymic,
                    "image",
                )
                im = Image.open(file)
                rgb_im = im.convert("RGB")
                image_path = os.path.join(folder, "image.jpg")
                if os.path.isfile(image_path):
                    os.remove(image_path)
                rgb_im.save(image_path)

        else:
            person = db.session.get(Person, item_id)
            if person:
                folder = create_folders(
                    item_id,
                    person.surname,
                    person.firstname,
                    person.patronymic,
                    action,
                )
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
    file_path = os.path.join(
        Config.BASE_PATH,
        person.surname[0].upper(),
        f"{person.id}-{person.surname.upper()} {person.firstname.upper()} {person.patronymic.upper()}".rstrip(),
        "image",
        "image.jpg",
    )
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True, mimetype="image/jpg")
    return send_file("static/no-photo.png", as_attachment=True, mimetype="image/jpg")



def parse_anketa(file_json):
    anketa = parse_json(file_json)
    person_id = add_resume(anketa["resume"], "create")

    person = db.session.get(Person, person_id)
    if person.path:
        if not os.path.isdir(person.path):
            os.mkdir(person.path)
    else:
        person.path = create_folders(
            person_id,
            person.surname,
            person.firstname,
            person.patronymic,
            "anketa",
        )
    models = [Previous, Staff, Document, Address, Contact, Workplace, Affilation]
    items_lists = [
        anketa["previous"],
        anketa["staff"],
        anketa["document"],
        anketa["address"],
        anketa["contact"],
        anketa["workplace"],
        anketa["affilation"],
    ]
    for model, items in zip(models, items_lists):
        for item in items:
            if item:
                db.session.add(model(**item | {"person_id": person_id}))
    db.session.commit()
    check_previous(anketa, person_id)
    
    return person_id


def check_previous(anketa, person_id):
    additional = ""
    if len(anketa["previous"]):
        for item in anketa["previous"]:
            surname = item["surname"] if item.get("surname") else anketa["surname"]
            firstname = (
                item["firstname"] if item.get("firstname") else anketa["firstname"]
            )
            patronymic = (
                item["patronymic"]
                if item.get("patronymic")
                else anketa["patronymic"]
            )

            result = db.session.execute(
                select(Person).filter(
                    Person.surname.ilike(surname),
                    Person.firstname.ilike(firstname),
                    Person.patronymic.ilike(patronymic),
                    Person.birthday == anketa["birthday"],
                )
            ).one_or_none()

            if result:
                message = (
                    f"Кандидат {anketa.surname} ID: {anketa.id} "
                    f"ранее проверялся как {result.surname} ID: {result.id}"
                )
                db.session.add(Message(message=message, user_id=current_user.id))
                additional = additional + message + "\n "
    person = db.session.get(Person, person_id)
    person.addition = (
        person.addition + "\n " + additional if person.addition else additional
    )
    db.session.commit()
