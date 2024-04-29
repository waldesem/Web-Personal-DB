from apiflask import EmptySchema
from flask import request
from flask.views import MethodView
from flask_jwt_extended import current_user

from . import bp
from .login import roles_required
from ..utils.parsers import Resume, Personal
from ..models.classes import Roles, Statuses
from ..models.schema import  PersonSchema
from ..models.model import  db, Person, Message


class ResumeView(MethodView):

    decorators = [roles_required(Roles.user.value), bp.doc(hide=True)]

    def get(self, person_id):
        action = request.args.get("action")
        person = Personal(person_id)
        if action == "status":
            person.change_status(Statuses.update.value)
            return {"message": action}, 201

        if action == "self" and not person.user_id:
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
            status = person.send_anketa()
            if status == "send":
                person.change_status(Statuses.robot.value, current_user.id)
            return {"message": status}, 201

        return {"message": PersonSchema().dump(person)}, 200

    @bp.output(EmptySchema)
    def delete(self, person_id):
        person = db.session.get(Person, person_id)
        db.session.delete(person)
        db.session.commit()
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


resume_view = ResumeView.as_view("resume")
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

