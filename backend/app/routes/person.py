import httpx
from apiflask import Schema, EmptySchema
from apiflask.fields import String, Date
from flask import request, abort
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy import select

from . import bp
from .login import roles_required
from ..utils.parsers import Resume, Anketa
from ..models.classes import Roles, Statuses, Conclusions
from ..models.model import (
    db, 
    Person,
    Education,
    Previous,
    Staff,
    Document,
    Address,
    Contact,
    Workplace,
    Relation,
    Affilation,
    Conclusion,
    Person,
    Check,
    Robot,
    Poligraf,
    Investigation,
    Inquiry,
    Status,
    Message,
)
from ..models.schema import (
    PersonSchema,
    EducationSchema,
    RelationSchema,
    PreviousSchema,
    StaffSchema,
    AddressSchema,
    ContactSchema,
    DocumentSchema,
    WorkplaceSchema,
    AffilationSchema,
    CheckSchema,
    RobotSchema,
    InquirySchema,
    InvestigationSchema,
    PoligrafSchema,
)


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


class ItemsView(MethodView):

    MODELS_SCHEMAS = {
        "previous": [Previous, PreviousSchema()],
        "staff": [Staff, StaffSchema()],
        "document": [Document, DocumentSchema()],
        "address": [Address, AddressSchema()],
        "contact": [Contact, ContactSchema()],
        "education": [Education, EducationSchema()],
        "workplace": [Workplace, WorkplaceSchema()],
        "relation": [Relation, RelationSchema()],
        "affilation": [Affilation, AffilationSchema()],
        "check": [Check, CheckSchema()],
        "robot": [Robot, RobotSchema()],
        "poligraf": [Poligraf, PoligrafSchema()],
        "investigation": [Investigation, InvestigationSchema()],
        "inquiry": [Inquiry, InquirySchema()],
    }

    @classmethod
    def define_schema_model(cls, item):
        return cls.MODELS_SCHEMAS[item]

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    def get(self, item, item_id):
        model, schema = self.define_schema_model(item)
        query = (
            select(model)
            .filter_by(person_id=item_id)
            .order_by(model.id.desc())
        )
        result = db.session.execute(query).scalars().all()
        return schema.dump(result, many=True), 200

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    @bp.output(EmptySchema)
    def post(self, item, item_id):
        model, schema = self.define_schema_model(item)
        resp = request.get_json()
        json_data = schema.load(resp) | {"person_id": item_id}

        if item == "previous":
            person = db.session.get(Person, item_id)
            prev = db.session.execute(
                select(Person).filter(
                    Person.surname.ilike(json_data["surname"]),
                    Person.firstname.ilike(json_data["firstname"]),
                    Person.patronymic.ilike(json_data.get("patronymic")),
                    Person.birthday == person.birthday,
                )
            ).scalar_one_or_none()
            if prev:
                db.session.add(Message(
                    message=f"Кандидат ранее проверялся ID: {prev.id}",
                    user_id=current_user.id,
                ))
                Anketa.add_relation("Одно лицо", prev.id, item_id)

        if item == "relation":
            Anketa.add_relation(json_data["relation"], item_id, json_data["relation_id"])


        if item in ["check", "poligraf", "inquiry", "investigation"]:
            json_data = json_data | {"user_id": current_user.id}

            if item == "check":
                person = db.session.get(Person, item_id)
                if json_data["conclusion_id"] == Conclusion.get_id(
                    Conclusions.saved.value
                ):
                    person.status_id = Status.get_id(Statuses.save.value)
                else:
                    person.status_id = (
                        Status.get_id(Statuses.poligraf.value)
                        if json_data.get("pfo")
                        else Status.get_id(Statuses.finish.value)
                    )
                    person.user_id = None

            if item == "poligraf":
                person = db.session.get(Person, item_id)
                if person.status_id == Status.get_id(Statuses.poligraf.value):
                    person.status_id = Status.get_id(Statuses.finish.value)

        result = model(**json_data)
        db.session.add(result)
        db.session.commit()
        return "", 201

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    def patch(self, item, item_id):
        model, schema = self.define_schema_model(item)
        resp = request.get_json()
        json_data = schema.load(resp)
        if item == "workplace":
            json_data["now_work"] = (
                bool(json_data.pop("now_work")) if "now_work" in json_data else False
            )
        result = db.session.get(model, item_id)
        if result:
            for k, v in json_data.items():
                setattr(result, k, v)
            db.session.commit()
            return "", 201
        return abort(403)

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    def delete(self, item, item_id):
        model, _ = self.define_schema_model(item)
        result = db.session.get(model, item_id)
        if result:
            db.session.delete(result)
            db.session.commit()
            return "", 204
        return abort(403)


bp.add_url_rule("/<item>/<int:item_id>", view_func=ItemsView.as_view("items"))
