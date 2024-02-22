import os
import shutil

from apiflask import EmptySchema
from flask import abort
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy import select

from . import bp
from .. import db
from ..utils.folders import create_folders
from .login import roles_required, group_required
from ..models.classes import Conclusions, Roles, Groups, Statuses
from ..models.model import (
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
    CheckSchema,
    InquirySchema,
    InvestigationSchema,
    PoligrafSchema,
    RobotSchema,
    ActionSchema,
)

class CheckView(MethodView):

    decorators = [bp.doc(hide=True)]

    @group_required(Groups.staffsec.value)
    @bp.input(ActionSchema, location="query")
    def get(self, item_id, query_data):
        action = query_data.get("action")
        if action == "self":
            person = db.session.get(Person, item_id)
            if person.user_id != current_user.id:
                db.session.add(
                    Message(
                        message=f"Aнкета ID #{id} делегирована " 
                        f"{current_user.fullname}",
                        user_id=person.user_id,
                    )
                )
                person.user_id = current_user.id
                db.session.commit()
                return {"message": "self"}, 201
            
        return CheckSchema().dump(
            db.session.execute(
                select(Check)
                .filter_by(person_id=item_id)
                .order_by(Check.id.desc())
            )
            .scalars()
            .all(),
            many=True,
        ), 200


    @group_required(Groups.staffsec.value)
    @roles_required(Roles.user.value)
    @bp.input(ActionSchema, location="query")
    @bp.input(CheckSchema, location="json")
    def post(self, item_id, json_data, query_data):
        action = query_data.get("action")
        json_data["pfo"] = bool(json_data.pop("pfo")) if "pfo" in json_data else False
        if action == "update":
            check = db.session.get(Check, item_id)
            person = db.session.get(Person, check.person_id)
            for k, v in json_data.items():
                setattr(check, k, v)
        else:
            person = db.session.get(Person, item_id)
            db.session.add(
                Check(**json_data | {"person_id": item_id, "officer": current_user.fullname})
                )
            db.session.commit()

        if json_data["conclusion_id"] == Conclusion.get_id(Conclusions.saved.value):
            person.status_id = Status.get_id(Statuses.save.value)
        else:
            person.status_id = (
                Status.get_id(Statuses.poligraf.value)
                if json_data["pfo"]
                else Status.get_id(Statuses.finish.value)
            )
            person.user_id = 0
        return "", 201

    @roles_required(Roles.user.value)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, item_id):
        check = db.session.get(Check, item_id)
        person = db.session.get(Person, check.person_id)
        person.status = Status.get_id(Statuses.update.value)
        person.user_id = 0
        db.session.delete(check)
        db.session.commit()
        return "", 204


bp.add_url_rule("/check//<int:item_id>", view_func=CheckView.as_view("check"))


class RobotView(MethodView):
    """
    The RobotView class is a subclass of the MethodView class from the flask.views module.
    """

    @group_required(Groups.staffsec.value)
    @bp.doc(hide=True)
    def get(self, item_id):
        return RobotSchema().dump(
            db.session.execute(
                select(Robot)
                .filter_by(person_id=item_id)
                .order_by(Robot.id.desc())
            )
            .scalars()
            .all(),
            many=True,
        ), 200

    @group_required(Groups.rest.value)
    @roles_required(Roles.api.value)
    @bp.input(RobotSchema)
    def post(self, json_data):
        user_id = json_data.pop("user_id")
        robot_path = json_data.pop("path")
        candidate = db.session.get(Person, json_data["id"])
        
        del json_data["id"]

        if candidate.has_status(Statuses.robot.value):
            if os.path.isdir(json_data["path"]):
                check_path = create_folders(
                    candidate.id, candidate["fullname"], "robot"
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
                    report=f"Автоматическая проверка {candidate.fullname} окончена",
                    user_id=user_id,
                )
            )
            candidate.status_id = Status().get_id(Statuses.reply.value)

        else:
            db.session.add(
                Message(
                    report=f"Результат проверки {candidate.fullname} не может быть записан."
                    f'Материал проверки находится в {robot_path}',
                    user_id=user_id,
                )
            )
        db.session.commit()
        return "", 201

    @group_required(Groups.staffsec.value)
    @roles_required(Roles.user.value)
    @bp.output(EmptySchema, status_code=204)
    @bp.doc(hide=True)
    def delete(self, item_id):
        robot = db.session.get(Robot, item_id)
        if robot:
            db.session.delete(robot)
            db.session.commit()
            return "", 204
        return abort(403)


bp.add_url_rule("/robot/<int:item_id>", view_func=RobotView.as_view("robot"))


class InvestigationView(MethodView):

    decorators = [bp.doc(hide=True)]

    @group_required(Groups.staffsec.value)
    def get(self, item_id):
        return InvestigationSchema().dump(
            db.session.execute(
                select(Investigation)
                .filter_by(person_id=item_id)
                .order_by(Investigation.id.desc())
            )
            .scalars()
            .all(),
            many=True,
        )

    @group_required(Groups.staffsec.value)
    @roles_required(Roles.user.value)
    @bp.input(InvestigationSchema)
    def post(self, item_id, json_data):
        db.session.add(
            Investigation(
                **json_data | {"person_id": item_id, "officer": current_user.fullname}
            )
        )
        db.session.commit()
        return "", 201
    
    @group_required(Groups.staffsec.value)
    @roles_required(Roles.user.value)
    @bp.input(InvestigationSchema)
    def patch(self, item_id, json_data):
        invs = db.session.get(Investigation, item_id)
        if invs:
            for k, v in json_data.items():
                setattr(invs, k, v)
            db.session.commit()
            return "", 201
        return abort(403)

    @group_required(Groups.staffsec.value)
    @roles_required(Roles.user.value)
    @bp.output(EmptySchema)
    def delete(self, item_id):
        invs = db.session.get(Investigation, item_id)
        if invs:
            db.session.delete(invs)
            db.session.commit()
            return "", 204
        return abort(403)


bp.add_url_rule(
    "/investigation/<int:item_id>",
    view_func=InvestigationView.as_view("investigation"),
)


class PoligrafView(MethodView):

    decorators = [bp.doc(hide=True)]

    @group_required(Groups.staffsec.value)
    def get(self, item_id):
        return PoligrafSchema().dump(
            db.session.execute(
                select(Poligraf)
                .filter_by(person_id=item_id)
                .order_by(Poligraf.id.desc())
            )
            .scalars()
            .all(),
            many=True,
        )

    @group_required(Groups.staffsec.value)
    @roles_required(Roles.user.value)
    @bp.input(PoligrafSchema)
    def post(self, item_id, json_data):
        person = db.session.get(Person, item_id)
        if person:
            if person.has_status(Statuses.poligraf.value):
                person.status_id = Status.get_id(Statuses.finish.value)
            db.session.add(
                Poligraf(
                    **json_data | {"person_id": item_id, "officer": current_user.fullname}
                )
            )
            db.session.commit()
            return "", 201
        return abort(403)

    @group_required(Groups.staffsec.value)
    @roles_required(Roles.user.value)
    @bp.input(PoligrafSchema)
    def patch(self, item_id, json_data):
        pfo = db.session.get(Poligraf, item_id)
        if pfo:
            for k, v in json_data.items():
                setattr(pfo, k, v)
            db.session.commit()
            return "", 201
        return abort(403)

    @group_required(Groups.staffsec.value)
    @roles_required(Roles.user.value)
    @bp.output(EmptySchema)
    def delete(self, item_id):
        pfo = db.session.get(Poligraf, item_id)
        if pfo:
            db.session.delete(pfo)
            db.session.commit()
            return "", 204
        return abort(403)


bp.add_url_rule(
    "/poligraf/<int:item_id>", view_func=PoligrafView.as_view("poligraf")
)


class InquiryView(MethodView):

    decorators = [bp.doc(hide=True)]

    @group_required(Groups.staffsec.value)
    def get(self, item_id):
        return InquirySchema().dump(
            db.session.execute(
                select(Inquiry).filter_by(person_id=item_id).order_by(Inquiry.id.desc())
            )
            .scalars()
            .all(),
            many=True,
        ), 200

    @group_required(Groups.staffsec.value)
    @bp.input(InquirySchema)
    @roles_required(Roles.user.value)
    def post(self, item_id, json_data):
        db.session.add(
            Inquiry(
                **json_data | {"person_id": item_id, "officer": current_user.fullname}
            )
        )
        db.session.commit()
        return "", 201

    @group_required(Groups.staffsec.value)
    @roles_required(Roles.user.value)
    @bp.input(InquirySchema)
    def patch(self, item_id, json_data):
        inq = db.session.get(Inquiry, item_id)
        if inq:
            for k, v in json_data.items():
                setattr(inq, k, v)
            db.session.commit()
            return "", 201

    @group_required(Groups.staffsec.value)
    @roles_required(Roles.user.value)
    @bp.output(EmptySchema)
    def delete(self, item_id):
        inq = db.session.get(Inquiry, item_id)
        if inq:
            db.session.delete(db.session.get(Inquiry, item_id))
            db.session.commit()
            return "", 204
        return abort(403)

bp.add_url_rule(
    "/inquiry/<int:item_id>", view_func=InquiryView.as_view("inquiry")
)
