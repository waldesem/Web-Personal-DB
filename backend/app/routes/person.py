from datetime import datetime
import json
from flask import jsonify, request, abort
from flask.views import MethodView
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
        result = person.anketa.__dict__
        del result["_sa_instance_state"]
        return jsonify({"message": person.anketa.__dict__})

    def delete(self, person_id):
        person = ResumeAction(person_id)
        person.del_person()
        return "", 204

    def patch(self, person_id):
        json_data = request.get_json()
        json_data["birthday"] = datetime.strptime(
            json_data["birthday"], "%Y-%m-%d"
        ).date()
        resume = Resume(json_data)
        with Session(engine) as session:
            resume.update_resume(session.get(Person, person_id))
            return jsonify({"message": person_id}), 201

    def post(self):
        json_data = request.get_json()
        json_data["birthday"] = datetime.strptime(
            json_data["birthday"], "%Y-%m-%d"
        ).date()
        resume = Resume(json_data)
        person_id = resume.check_resume()
        return jsonify({"message": person_id}), 201


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
    def get(self, item, item_id):
        with Session(engine) as session:
            model = self.define_model(item)
            query = select(model).filter_by(person_id=item_id).order_by(model.id.desc())
            results = session.execute(query).all()
            results = [r.__dict__ for r in results]
            for r in results:
                del r["_sa_instance_state"]
            return jsonify(results)

    @roles_required(Roles.user.value)
    def post(self, item, item_id):
        model = self.define_model(item)
        json_data = request.get_json() | {"person_id": item_id}

        with Session(engine) as session:
            if item == "previous":
                json_data["date_change"] = datetime.strptime(
                    json_data["date_change"], "%Y-%m-%d"
                )
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
                    session.add(
                        Message(
                            message=f"Кандидат ранее проверялся ID: {prev.id}",
                            user_id=Token.current_user.id,
                        )
                    )
                    Anketa.add_relation("Одно лицо", prev.id, item_id)

            if item == "relation":
                Anketa.add_relation(
                    json_data["relation"], item_id, json_data["relation_id"]
                )
            if item == "document":
                json_data["issue"] = datetime.strptime(json_data["issue"], "%Y-%m-%d")
            if item == "workplace":
                json_data["start_date"] = datetime.strptime(
                    json_data["start_date"], "%Y-%m-%d"
                )
                if json_data.get("end_date"):
                    json_data["end_date"] = datetime.strptime(
                        json_data["end_date"], "%Y-%m-%d"
                    )
                if json_data.get("now_work"):
                    json_data["now_work"] = True
            if item == "affilation":
                json_data["deadline"] = datetime.strptime(
                    json_data["deadline"], "%Y-%m-%d"
                )
            if item in ["check", "poligraf", "inquiry", "investigation"]:
                json_data = json_data | {"user_id": Token.current_user.id}
                json_data["deadline"] = datetime.strptime(
                    json_data["deadline"], "%Y-%m-%d"
                )
                if item == "check":
                    if json_data.get("pfo"):
                        json_data["pfo"] = True
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
            return "", 201

    @roles_required(Roles.user.value)
    def patch(self, item, item_id):
        model = self.define_model(item)
        resp = request.get_json()
        json_data = json.load(resp)

        with Session(engine) as session:
            if item == "workplace":
                json_data["now_work"] = (
                    bool(json_data.pop("now_work"))
                    if "now_work" in json_data
                    else False
                )
            result = session.get(model, item_id)
            if result:
                for k, v in json_data.items():
                    setattr(result, k, v)
                session.commit()
                return "", 201
            return abort(403)

    @roles_required(Roles.user.value)
    def delete(self, item, item_id):
        model = self.define_model(item)
        with Session(engine) as session:
            result = session.get(model, item_id)
            if result:
                session.delete(result)
                session.commit()
                return "", 204
            return abort(403)


bp.add_url_rule("/<item>/<int:item_id>", view_func=ItemsView.as_view("items"))
