import json
from flask import jsonify, request, abort
from flask.views import MethodView
import requests
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import bp
from ..utils.dependencies import Token, roles_required
from ..utils.parsers import Resume, Anketa
from ..models.classes import Roles, Statuses, Conclusions
from ..models.model import (
    engine, 
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
    Check,
    Robot,
    Poligraf,
    Investigation,
    Inquiry,
    Status,
    Message,
)


class AnketaView(MethodView):

    decorators = [roles_required(Roles.user.value)]

    def get(self, person_id):
        action = request.args.get("action")
        person = ResumeAction(person_id)
        if action == "status":
            person.change_status(Statuses.update.value)
            return {"message": action}, 201
        with Session(engine) as session:
            if action == "self" and not person.anketa.user_id:
                session.add(
                    Message(
                        message=f"Aнкета ID #{person_id} принята в работу",
                        user_id=Token.current_user.id,
                    )
                )
                session.commit()
                person.change_status(Statuses.manual.value, Token.current_user.id)
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
                        person.change_status(Statuses.robot.value, Token.current_user.id)
                    return {"message": status}, 201
                else:
                    return abort, 400
        return {"message": person.anketa.__dict__}

    def delete(self, person_id):
        person = ResumeAction(person_id)
        person.del_person()
        return "", 204

    def patch(self, person_id):
        json_data = request.get_json()
        resume = Resume(json_data)
        with Session(engine) as session:
            resume.update_resume(session.get(Person, person_id))
            return {"message": person_id}

    def post(self):
        json_data = request.get_json()
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

class ResumeAction:

    def __init__(self, person_id):
        with Session(engine) as session:
            self.anketa = session.get(Person, person_id)

    def change_status(self, status, user_id=None):
        with Session(engine) as session:
            self.anketa.status_id = Status.get_id(status)
            self.anketa.user_id = user_id
            session.commit()

    def del_person(self):
        with Session(engine) as session:
            session.delete(self.anketa)
            session.commit()

    def send_anketa(self):
        with Session(engine) as session:
            docum = session.execute(
                select(Document)
                .filter_by(person_id=self.anketa.id)
                .order_by(Document.id.desc())
            ).scalar_one_or_none()
            addr = session.execute(
                select(Address)
                .filter(
                    Address.person_id == self.anketa.id,
                    Address.view.ilike("%регистрац%"),
                )
                .order_by(Address.id.desc())
            ).scalar_one_or_none()
            if not docum or not addr:
                return "error"
            serial = json.dump(
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
                response = requests.post(
                    url="http://127.0.0.1:5001", json=serial, timeout=5
                )
                response.raise_for_status()
                return "send"
            except requests.HTTPError as e:
                print(e)
                return "error"


class ItemsView(MethodView):

    MODELS_SCHEMAS = {
        "previous": Previous,
        "staff": Staff,
        "document": Document,
        "address": Address,
        "contact": Contact,
        "education": Education,
        "workplace": Workplace,
        "relation": Relation,
        "affilation": Affilation,
        "check": Check,
        "robot": Robot,
        "poligraf": Poligraf,
        "investigation": Investigation,
        "inquiry": Inquiry,
    }

    @classmethod
    def define_model(cls, item):
        return cls.MODELS_SCHEMAS[item]

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    def get(self, item, item_id):
        with Session(engine) as session:
            model = self.define_model(item)
            query = (
                select(model)
                .filter_by(person_id=item_id)
                .order_by(model.id.desc())
            )
            results = session.execute(query).all()
            return jsonify(result.__dict__ for result in results)

    @roles_required(Roles.user.value)
    def post(self, item, item_id):
        model = self.define_model(item)
        resp = request.get_json()
        json_data = json.load(resp) | {"person_id": item_id}

        with Session(engine) as session:
            if item == "previous":
                person = session.get(Person, item_id)
                prev = session.execute(
                    select(Person).filter(
                        Person.surname.ilike(json_data["surname"]),
                        Person.firstname.ilike(json_data["firstname"]),
                        Person.patronymic.ilike(json_data.get("patronymic")),
                        Person.birthday == person.birthday,
                    )
                ).scalar_one_or_none()
                if prev:
                    session.add(Message(
                        message=f"Кандидат ранее проверялся ID: {prev.id}",
                        user_id=Token.current_user.id,
                    ))
                    Anketa.add_relation("Одно лицо", prev.id, item_id)

            if item == "relation":
                Anketa.add_relation(json_data["relation"], item_id, json_data["relation_id"])


            if item in ["check", "poligraf", "inquiry", "investigation"]:
                json_data = json_data | {"user_id": Token.current_user.id}

                if item == "check":
                    person = session.get(Person, item_id)
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
                    person = session.get(Person, item_id)
                    if person.status_id == Status.get_id(Statuses.poligraf.value):
                        person.status_id = Status.get_id(Statuses.finish.value)

            result = model(**json_data)
            session.add(result)
            session.commit()
            return ""

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    def patch(self, item, item_id):
        model = self.define_model(item)
        resp = request.get_json()
        json_data = json.load(resp)

        with Session(engine) as session:
            if item == "workplace":
                json_data["now_work"] = (
                    bool(json_data.pop("now_work")) if "now_work" in json_data else False
                )
            result = session.get(model, item_id)
            if result:
                for k, v in json_data.items():
                    setattr(result, k, v)
                session.commit()
                return ""
            return abort(403)

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    def delete(self, item, item_id):
        model = self.define_model(item)
        with Session(engine) as session:
            result = session.get(model, item_id)
            if result:
                session.delete(result)
                session.commit()
                return ""
            return abort(403)


bp.add_url_rule("/<item>/<int:item_id>", view_func=ItemsView.as_view("items"))
