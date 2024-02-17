import os
import shutil
from datetime import datetime

import requests
from flask import abort, request
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy import select
from werkzeug.utils import secure_filename

from config import Config
from . import bp_resume
from ... import db
from ...utils.jsonparser import parse_json
from ...utils.folders import create_folders
from ..login.login import roles_required, group_required
from ...models.classes import Roles, Groups, Statuses
from ...models.model import (
    Person,
    Document,
    Address,
    Status,
    Staff,
    Workplace,
    Contact,
    Affilation,
)
from ...models.schema import (
    AnketaSchemaApi,
    PersonSchema,
    ActionSchema,
)


class ResumeView(MethodView):

    @roles_required(Groups.staffsec.value)
    @bp_resume.input(ActionSchema, location="query")
    @bp_resume.doc(hide=True)
    def get(self, person_id, query_data):
        action = query_data.get("action")
        person = db.session.get(Person, person_id)
        if person:
            if action == "status":
                person.status_id = Status.get_id(Statuses.update.value)
                db.session.commit()
                return self.get(person_id), 201

            elif action == "send":
                if person.has_status(
                    Statuses.new.value,
                    Statuses.update.value,
                    Statuses.repeat.value,
                ):
                    docum = db.session.execute(
                        select(Document)
                        .filter_by(person_id=person_id)
                        .order_by(Document.id.desc())
                        .one_or_none()
                    )
                    addr = db.session.execute(
                        select(Address)
                        .filter(
                            Address.person_id == person_id,
                            Address.view.ilike("%регистрац%"),
                        )
                        .order_by(Address.id.desc())
                        .one_or_none()
                    )
                    serial = AnketaSchemaApi().dump(
                        {
                            "id": person_id,
                            "fullname": person.fullname,
                            "birthday": person.birthday,
                            "birthplace": person.birthplace,
                            "snils": person.snils,
                            "inn": person.inn,
                            "series": docum.series,
                            "number": docum.number,
                            "agency": docum.agency,
                            "issue": docum.issue,
                            "address": addr.address,
                            "user_id": current_user.id,
                        }
                    )
                    try:
                        response = requests.post(
                            url="https://httpbin.org/post", json=serial, timeout=5
                        )
                        response.raise_for_status()
                        if response.status_code == 200:
                            person.status_id = Status.get_id(Statuses.robot.value)
                            person.user_id = current_user.id
                            db.session.commit()
                            return self.get(person_id)

                        return abort(response.status_code)
                    except requests.exceptions.RequestException as e:
                        print(e)
                return abort(403)
            return PersonSchema().dump(person), 200
        return abort(403)

    @roles_required(Roles.user.value)
    @group_required(Groups.staffsec.value)
    @bp_resume.doc(hide=True)
    def delete(self, person_id):
        person = db.session.get(Person, person_id)
        try:
            shutil.rmtree(os.path.join(Config.BASE_PATH, person.path))
        except Exception as e:
            print(e)
        db.session.delete(person)
        db.session.commit()
        return "", 204

    @roles_required(Roles.user.value, Roles.api.value)
    @group_required(Groups.staffsec.value, Groups.rest.value)
    @bp_resume.input(PersonSchema)
    def post(self, action, json_data):
        person_id = ResumeView.add_resume(json_data, action)
        return {"message": person_id}

    @staticmethod
    def add_resume(resume: dict, action):
        """
        Adds a resume to the database.
        """
        person = db.session.execute(
            select(Person).filter(
                Person.fullname.ilike(resume["fullname"]),
                Person.birthday == resume["birthday"],
            )
        ).one_or_none()

        if person:
            person_id = person.id
            for k, v in resume.items():
                setattr(person, k, v)
            if action == "api":
                person.status_id = Status().get_id(Statuses.update.value)
        else:
            person = Person(**resume)
            db.session.add(person)
            db.session.flush()
            person_id = person.id
            if action == "api":
                person.status_id = Status().get_id(Statuses.new.value)

        if action == "create":
            person.status_id = Status().get_id(Statuses.manual.value)

        person.path = os.path.join(resume["fullname"][0].upper(), f"{person_id}-{resume['fullname']}")
        url = os.path.join(Config.BASE_PATH, person.path)
        if not os.path.isdir(url):
            os.mkdir(url)
        person.user_id = current_user.id
        db.session.commit()
        return person_id

resume_view = ResumeView.as_view("resume")
bp_resume.add_url_rule(
    "/resume/<action>",
    view_func=resume_view,
    methods=["POST"],
)
bp_resume.add_url_rule(
    "/resume/<int:person_id>",
    view_func=resume_view,
    methods=["GET", "DELETE"],
)


class JsonView(MethodView):
    decorators = [
        group_required(Groups.staffsec.value),
        roles_required(Roles.user.value),
        bp_resume.doc(hide=True),
    ]

    @bp_resume.input(ActionSchema, location="query")
    def post(self, query_data, item_id=0):
        action = query_data.get("action")
        if not request.files["file"].filename and action:
            return {"result": False, "item_id": item_id}

        file = request.files["file"]
        filename = secure_filename(file.filename)
        temp_path = os.path.join(
            Config.BASE_PATH,
            f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}\
                                    -{filename}',
        )
        file.save(temp_path)

        anketa = parse_json(temp_path)
        person_id = ResumeView.add_resume(anketa.resume, "create")
        self.fill_items(anketa, person_id)

        person = db.session.get(Person, person_id)
        if person.path:
            full_path = os.path.join(Config.BASE_PATH, person.path)
            if not os.path.isdir(full_path):
                os.mkdir(full_path)
        else:
            person.path = os.path.join(person.fullname[0].upper(), f"{person_id}-{person.fullname}")
            url = os.path.join(Config.BASE_PATH, person.path)
            if not os.path.isdir(url):
                os.mkdir(url)
        db.session.commit()

        action_folder = create_folders(person_id, person.fullname, action)

        save_path = os.path.join(
            Config.BASE_PATH, action_folder, filename
        )
        if not os.path.isfile(save_path):
            try:
                shutil.move(temp_path, save_path)
            except Exception as e:
                print(e)
        return {"message": person_id}

    def fill_items(self, anketa, person_id):
        models = [Staff, Document, Address, Contact, Workplace, Affilation]
        items_lists = [
            anketa.staff,
            anketa.passport,
            anketa.addresses,
            anketa.contacts,
            anketa.workplaces,
            anketa.affilation,
        ]
        for model, items in zip(models, items_lists):
            for item in items:
                if item:
                    db.session.add(model(**item | {"person_id": person_id}))
        db.session.commit()

bp_resume.add_url_rule("/json", view_func=JsonView.as_view("json"))
