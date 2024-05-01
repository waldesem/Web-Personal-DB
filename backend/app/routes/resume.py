import httpx
from apiflask import Schema, EmptySchema
from apiflask.fields import String, Date
from flask import request, abort
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy import select

from . import bp
from .login import roles_required
from ..utils.parsers import Resume
from ..models.classes import Roles, Statuses
from ..models.schema import  PersonSchema
from ..models.model import  Status, db, Person, Message, Document, Address


class AnketaView(MethodView):

    decorators = [roles_required(Roles.user.value), bp.doc(hide=True)]

    def get(self, person_id):
        action = request.args.get("action")
        person = ResumeAction(person_id)
        if action == "status":
            person.change_status(Statuses.update.value)
            return {"message": action}, 201

        if action == "self" and not person.anketa.user_id:
            db.session.add(
                Message(
                    message=f"Aнкета ID #{person_id} принята в работу",
                    user_id=current_user.id,
                )
            )
            db.session.commit()
            person.change_status(Statuses.manual.value, current_user.id)
            return {"message": action}, 201

        elif action == "send":
            if person.anketa.status_id in (
                Status.get_id(Statuses.new.value),
                Status.get_id(Statuses.update.value),
                Status.get_id(Statuses.repeat.value),
                Status.get_id(Statuses.manual.value),
                Status.get_id(Statuses.robot.value),
            ):
                status = person.send_anketa()
                if status == "send":
                    person.change_status(Statuses.robot.value, current_user.id)
                return {"message": status}, 201
            else:
                return abort, 400
        return {"message": PersonSchema().dump(person.anketa)}, 200

    @bp.output(EmptySchema)
    def delete(self, person_id):
        person = ResumeAction(person_id)
        person.del_person()
        return "", 204

    @bp.input(PersonSchema)
    def patch(self, person_id, json_data):
        resume = Resume(json_data)
        resume.update_resume(db.session.get(Person, person_id))
        return {"message": person_id}

    @bp.input(PersonSchema)
    def post(self, json_data):
        resume = Resume(json_data)
        person_id = resume.check_resume()
        return {"message": person_id}


resume_view = AnketaView.as_view("resume")
bp.add_url_rule(
    "/resume",
    view_func=resume_view,
    methods=["POST"],
)
bp.add_url_rule(
    "/resume/<int:person_id>",
    view_func=resume_view,
    methods=["GET", "DELETE", "PATCH"],
)


class ResumeSchemaApi(Schema):
    """Create schema for sending anketa to api for robot check"""

    id = String()
    surname = String()
    firstname = String()
    patronymic = String()
    birthday = Date()
    birthplace = String()
    snils = String()
    inn = String()
    series = String()
    number = String()
    agency = String()
    issue = Date()
    address = String()


class ResumeAction:

    def __init__(self, person_id):
        self.anketa = db.session.get(Person, person_id)

    def change_status(self, status, user_id=None):
        self.anketa.status_id = Status.get_id(status)
        self.anketa.user_id = user_id
        db.session.commit()

    def del_person(self):
        db.session.delete(self.anketa)
        db.session.commit()

    def send_anketa(self):
        docum = db.session.execute(
            select(Document)
            .filter_by(person_id=self.anketa.id)
            .order_by(Document.id.desc())
        ).scalar_one_or_none()
        addr = db.session.execute(
            select(Address)
            .filter(
                Address.person_id == self.anketa.id,
                Address.view.ilike("%регистрац%"),
            )
            .order_by(Address.id.desc())
        ).scalar_one_or_none()
        if not docum or not addr:
            return "error"
        serial = ResumeSchemaApi().dump(
            {
                "id": self.anketa.id,
                "surname": self.anketa.surname,
                "firstname": self.anketa.firstname,
                "patronymic": self.anketa.patronymic,
                "birthday": self.anketa.birthday,
                "birthplace": self.anketa.birthplace,
                "snils": self.anketa.snils,
                "inn": self.anketa.inn,
                "series": docum.series,
                "number": docum.number,
                "agency": docum.agency,
                "issue": docum.issue,
                "address": addr.address,
            }
        )
        try:
            response = httpx.post(
                url="http://127.0.0.1:5001", json=serial, timeout=5
            )
            response.raise_for_status()
            return "send"
        except httpx.HTTPError as e:
            return "error"
        