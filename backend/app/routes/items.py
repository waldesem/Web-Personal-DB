import os
import shutil

from flask import abort, request
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy import select

from . import bp
from .login import roles_required
from ..utils.create_folders import create_folders
from ..models.classes import Roles, Conclusions, Statuses
from ..models.model import (
    db,
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
    Poligraf,
    Investigation,
    Inquiry,
    Status,
    Message,
    Robot,
)
from ..models.schema import (
    RelationSchema,
    StaffSchema,
    AddressSchema,
    ContactSchema,
    DocumentSchema,
    WorkplaceSchema,
    AffilationSchema,
    CheckSchema,
    InquirySchema,
    InvestigationSchema,
    PoligrafSchema,
    RobotSchema,
)

class ItemsView(MethodView):

    models_schemas = {
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

    @roles_required(Roles.user.value, Roles.api.value)
    @bp.doc(hide=True)
    def post(self, item, item_id):
        self.defines(item)
        resp = request.get_json()
        json_data = self.schema.load(resp)

        if item == 'workplace':
            json_data["now_work"] = (
            bool(json_data.pop("now_work")) if "now_work" in json_data else False
            )

        if item == 'check':
            json_data["pfo"] = (
                bool(json_data.pop("pfo")) if "pfo" in json_data else False
            )

        json_data = json_data | {"person_id": item_id}
        if item in ['check', 'poligraf', 'inquiry', 'investigation']:
            json_data | {"officer": current_user.fullname}
        
        result = self.model(**json_data)

        if item == 'relation':
            db.session.add(
            Relation(
                relation=json_data["relation"],
                relation_id=item_id,
                person_id=json_data["relation_id"],
            )
        )
            
        if item == "check":
            person = db.session.get(Person, item_id)
            if json_data["conclusion_id"] == Conclusion.get_id(Conclusions.saved.value):
                person.status_id = Status.get_id(Statuses.save.value)
            else:
                person.status_id = (
                    Status.get_id(Statuses.poligraf.value)
                    if json_data["pfo"]
                    else Status.get_id(Statuses.finish.value)
                )
                person.user_id = None

        if item == "poligraf":
            person = db.session.get(Person, item_id)
            if person.status_id == Status.get_id(Statuses.poligraf.value):
                person.status_id = Status.get_id(Statuses.finish.value)

        if item == "robot":
            self.post_robot(json_data)
        else:
            db.session.add(result)
            db.session.commit()
            return "", 201

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    def patch(self, item, item_id):
        self.defines(item)
        resp = request.get_json()
        json_data = self.schema.load(resp)
        if item == 'workplace':
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
            if item == "check":
                person = db.session.get(Person, result.person_id)
                person.status = Status.get_id(Statuses.update.value)
                person.user_id = ""
            db.session.commit()
            return "", 204
        return abort(403)

    def post_robot(json_data):
        user_id = json_data.pop("user_id")
        robot_path = json_data.pop("path")
        candidate = db.session.get(Person, json_data["id"])

        del json_data["id"]

        if candidate.status_id == Status.get_id(Statuses.robot.value):
            if os.path.isdir(json_data["path"]):
                check_path = create_folders(
                    candidate.id,
                    candidate.surname,
                    candidate.firstname,
                    candidate.patronymic,
                    "robot",
                )
                try:
                    for item in os.listdir(robot_path):
                        if os.path.isfile(os.path.join(robot_path, item)):
                            shutil.copyfile(item, check_path)
                        elif os.path.isdir(os.path.join(robot_path, item)):
                            shutil.copytree(item, os.path.join(check_path, item))
                except FileNotFoundError as e:
                    db.session.add(Message(report=f"{e}", user_id=user_id))

            db.session.add(Robot(**json_data | {"person_id": candidate.id}))
            db.session.add(
                Message(
                    report=f"Автоматическая проверка {candidate.surname} окончена",
                    user_id=user_id,
                )
            )
            candidate.status_id = Status().get_id(Statuses.reply.value)

        else:
            db.session.add(
                Message(
                    report=f"Результат проверки {candidate.surname} не может быть записан."
                    f"Материал проверки находится в {robot_path}",
                    user_id=user_id,
                )
            )
        db.session.commit()
        return "", 201

bp.add_url_rule("/<item>/<int:item_id>", view_func=ItemsView.as_view("items"))

