from apiflask import EmptySchema
from flask import abort, request
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy import select

from . import bp
from .login import roles_required
from ..models.classes import Roles, Conclusions, Statuses
from ..utils.parsers import parse_previous
from ..models.model import (
    db,
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


class ItemsView(MethodView):

    models_schemas = {
        "previous": [Previous, PreviousSchema()],
        "staff": [Staff, StaffSchema()],
        "document": [Document, DocumentSchema()],
        "address": [Address, AddressSchema()],
        "contact": [Contact, ContactSchema()],
        "workplace": [Workplace, WorkplaceSchema()],
        "relation": [Relation, RelationSchema()],
        "affilation": [Affilation, AffilationSchema()],
        "check": [Check, CheckSchema()],
        "robot": [Robot, RobotSchema()],
        "poligraf": [Poligraf, PoligrafSchema()],
        "investigation": [Investigation, InvestigationSchema()],
        "inquiry": [Inquiry, InquirySchema()],
    }

    def __init__(self):
        self.model = None
        self.schema = None

    def defines(self, item):
        self.model = ItemsView.models_schemas[item][0]
        self.schema = ItemsView.models_schemas[item][1]

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    def get(self, item, item_id):
        self.defines(item)
        query = (
            select(self.model)
            .filter_by(person_id=item_id)
            .order_by(self.model.id.desc())
        )
        result = db.session.execute(query).scalars().all()
        return self.schema.dump(result, many=True), 200

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    @bp.output(EmptySchema)
    def post(self, item, item_id):
        self.defines(item)
        resp = request.get_json()
        json_data = self.schema.load(resp) | {"person_id": item_id}

        if item == "previous":
            person = db.session.get(Person, item_id)
            prev = db.session.execute(
                select(Person).filter(
                    Person.surname.ilike(json_data["surname"]),
                    Person.firstname.ilike(json_data["firstname"]),
                    Person.patronymic.ilike(json_data.get("patronymic")),
                    Person.birthday == person.birthday,
                )
            ).one_or_none()
            if prev:
                addition = f"Кандидат ранее проверялся ID: {prev.id}"
                db.session.add(Message(addition, user_id=current_user.id))
                person.addition = person.addition + "\n" + addition \
                    if person.addition else addition

        if item == "relation":
            db.session.add(
                Relation(
                    relation=json_data["relation"],
                    relation_id=item_id,
                    person_id=json_data["relation_id"],
                )
            )

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

        result = self.model(**json_data)
        db.session.add(result)
        db.session.commit()
        return "", 201

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    def patch(self, item, item_id):
        self.defines(item)
        resp = request.get_json()
        json_data = self.schema.load(resp)
        if item == "workplace":
            json_data["now_work"] = (
                bool(json_data.pop("now_work")) if "now_work" in json_data else False
            )
        result = db.session.get(self.model, item_id)
        if result:
            for k, v in json_data.items():
                setattr(result, k, v)
            db.session.commit()
            return "", 201
        return abort(403)

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    def delete(self, item, item_id):
        self.defines(item)
        result = db.session.get(self.model, item_id)
        if result:
            db.session.delete(result)
            db.session.commit()
            return "", 204
        return abort(403)


bp.add_url_rule("/<item>/<int:item_id>", view_func=ItemsView.as_view("items"))
