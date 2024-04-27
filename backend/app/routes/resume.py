import httpx
from apiflask import EmptySchema
from flask import abort
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy import select

from . import bp
from .login import roles_required
from ..utils.folders import create_folders
from ..models.classes import Roles, Statuses
from ..models.model import (
    db,
    Document,
    Address,
    Person,
    Status,
    Message,
)
from ..models.schema import (
    ActionSchema,
    ResumeSchemaApi,
    PersonSchema,
)


class ResumeView(MethodView):

    decorators = [roles_required(Roles.user.value), bp.doc(hide=True)]

    @bp.input(ActionSchema, location="query")
    def get(self, person_id, query_data):
        action = query_data.get("action")
        person = db.session.get(Person, person_id)
        if person:
            if action == "status":
                person.status_id = Status.get_id(Statuses.update.value)
                person.user_id = None
                db.session.commit()
                return {"message": action}, 201

            if action == "self":
                if not person.user_id:
                    db.session.add(
                        Message(
                            message=f"Aнкета ID #{person_id} принята в работу",
                            user_id=current_user.id,
                        )
                    )
                    person.status_id = Status.get_id(Statuses.manual.value)
                    person.user_id = current_user.id
                    db.session.commit()
                    return {"message": action}, 201

            elif action == "send":
                return {"message": send_resume(person)}, 201

            return {"message": PersonSchema().dump(person)}, 200
        return abort(403)

    @bp.output(EmptySchema)
    def delete(self, person_id):
        person = db.session.get(Person, person_id)
        db.session.delete(person)
        db.session.commit()
        return "", 204

    @bp.input(PersonSchema)
    def patch(self, person_id, json_data):
        person = db.session.get(Person, person_id)
        for k, v in json_data.items():
            setattr(person, k, v)
            db.session.commit()
        return {"message": person_id}

    @bp.input(PersonSchema)
    def post(self, action, json_data):
        person_id = ResumeView.add_resume(json_data, action)
        return {"message": person_id}


resume_view = ResumeView.as_view("resume")
bp.add_url_rule(
    "/resume/<action>",
    view_func=resume_view,
    methods=["POST"],
)
bp.add_url_rule(
    "/resume/<int:person_id>",
    view_func=resume_view,
    methods=["GET", "DELETE", "PATCH"],
)


def add_resume(resume: dict, action):
    """
    Adds a resume to the database.
    """
    person = db.session.execute(
        select(Person).filter(
            Person.surname.ilike(resume["surname"]),
            Person.firstname.ilike(resume["firstname"]),
            Person.patronymic.ilike(resume.get("patronymic")),
            Person.birthday == resume["birthday"],
        )
    ).one_or_none()

    for k, v in resume.items():
        if k in ["surname", "firstname", "patronymic"]:
            resume[k] = v.strip().upper()

    if person:
        person_id = person.id
        for k, v in resume.items():
            setattr(person, k, v)
    else:
        if action == "create":
            resume["status_id"] = Status().get_id(Statuses.manual.value)
            resume["user_id"] = current_user.id
        if action == "api":
            resume["status_id"] = Status().get_id(Statuses.new.value)

        person = Person(**resume)
        db.session.add(person)
        db.session.flush()
        person_id = person.id

    person.path = create_folders(
        person_id,
        resume["surname"],
        resume["firstname"],
        resume.get("patronymic", ""),
        "resume",
    )
    person.user_id = current_user.id
    db.session.commit()
    return person_id


def send_resume(person):
    if person.status_id in (
        Status.get_id(Statuses.new.value),
        Status.get_id(Statuses.update.value),
        Status.get_id(Statuses.repeat.value),
        Status.get_id(Statuses.manual.value),
        Status.get_id(Statuses.robot.value),
    ):
        docum = db.session.execute(
            select(Document).filter_by(person_id=person.id).order_by(Document.id.desc())
        ).scalar_one_or_none()
        addr = db.session.execute(
            select(Address)
            .filter(
                Address.person_id == person.id,
                Address.view.ilike("%регистрац%"),
            )
            .order_by(Address.id.desc())
        ).scalar_one_or_none()
        if not docum or not addr:
            return "error"
        serial = ResumeSchemaApi().dump(
            {
                "id": person.id,
                "surname": person.surname,
                "firstname": person.firstname,
                "patronymic": person.patronymic,
                "birthday": person.birthday,
                "birthplace": person.birthplace,
                "snils": person.snils,
                "inn": person.inn,
                "series": docum.series,
                "number": docum.number,
                "agency": docum.agency,
                "issue": docum.issue,
                "address": addr.address,
            }
        )
        try:
            response = httpx.post(url="http://127.0.0.1:5001", json=serial, timeout=5)
            response.raise_for_status()
            person.status_id = Status.get_id(Statuses.robot.value)
            person.user_id = current_user.id
            db.session.add(
                Message(
                    message=f"Aнкета ID #{person.id} успешно отправлена роботу",
                    user_id=current_user.id,
                )
            )
            db.session.commit()
            return "send"
        except httpx.HTTPError as e:
            db.session.add(
                Message(
                    message=f"При отправке анкеты возникла ошибка: {e}",
                    user_id=current_user.id,
                )
            )
            db.session.commit()
            return "error"
    else:
        db.session.add(
            Message(
                message=f"Отправка анкеты ID #{person.id} невозможна",
                user_id=current_user.id,
            )
        )
        db.session.commit()
        return "error"
