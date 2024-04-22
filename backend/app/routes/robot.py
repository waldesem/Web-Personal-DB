import os
import shutil

from apiflask import EmptySchema
from flask.views import MethodView

from . import bp
from .login import roles_required
from ..utils.create_folders import create_folders
from ..models.classes import Roles, Statuses
from ..models.schema import  RobotSchema
from ..models.model import db, Person, Status, Message, Robot


class RobotsView(MethodView):

    @roles_required(Roles.api.value)
    @bp.input(RobotSchema)
    @bp.output(EmptySchema)
    def post(self, item_id, json_data):
        json_data = RobotSchema().load(json_data) | {"person_id": item_id}

        robot_path = json_data.pop("path")
        candidate = db.session.get(Person, json_data.pop("id"))

        if not candidate:
            db.session.add(
                Message(
                    report=f"Результат проверки {candidate.surname} не может быть записан."
                    f"Материал проверки находится в {robot_path}",
                    user_id=candidate.user_id,
                )
            )
            db.session.commit()
            return "", 201

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
                db.session.add(Message(report=f"{e}", user_id=candidate.user_id))

        db.session.add(Robot(**json_data | {"person_id": candidate.id}))
        db.session.add(
            Message(
                report=f"Автоматическая проверка {candidate.surname} окончена",
                user_id=candidate.user_id,
            )
        )
        candidate.status_id = Status().get_id(Statuses.reply.value)
        db.session.commit()
        return "", 201


bp.add_url_rule("/robot/<int:item_id>", view_func=RobotsView.as_view("robot"))
