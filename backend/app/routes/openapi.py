import os
import shutil

from apiflask import EmptySchema
from flask.views import MethodView

from . import bp
from ..utils.folders import Folders
from ..models.schema import  RobotSchema, AnketaSchemaApi
from ..models.model import db, Person, Message, Robot
from ..utils.parsers import Anketa


class RobotsView(MethodView):

    @bp.input(RobotSchema)
    @bp.output(EmptySchema, status_code=201)
    def post(self, json_data):
        """
        Post method for the given API endpoint.
        """
        robot_path = json_data.pop("path")
        candidate = db.session.get(Person, json_data.pop("id"))

        if not candidate:
            db.session.add(
                Message(
                    message=f"Результат {candidate.surname} не может быть записан."
                    f"Файлы находятся в {robot_path}",
                    user_id=candidate.user_id,
                )
            )
        else:
            if os.path.isdir(robot_path):
                folders = Folders(
                    candidate.id,
                    candidate.surname,
                    candidate.firstname,
                    candidate.patronymic,
                )
                check_path = folders.create_subfolder("robot")
                try:
                    for item in os.listdir(robot_path):
                        item_path = os.path.join(robot_path, item)
                        if os.path.isfile(item_path):
                            shutil.copyfile(item_path, os.path.join(check_path, item))
                        elif os.path.isdir(item_path):
                            shutil.copytree(item_path, os.path.join(check_path, item))
                except FileNotFoundError as e:
                    db.session.add(Message(message=f"{e}", user_id=candidate.user_id))

            db.session.add(Robot(**json_data | {"person_id": candidate.id}))
            db.session.add(
                Message(
                    message=f"Автоматическая проверка {candidate.surname} окончена",
                    user_id=candidate.user_id,
                )
            )
        db.session.commit()
        return ""


bp.add_url_rule("/robot", view_func=RobotsView.as_view("robot"))


class PulseView(MethodView):

    @bp.input(AnketaSchemaApi, location="json")
    @bp.output(EmptySchema, status_code=201)
    def post(self, json_data):
        """
        Post method for the given API endpoint.
        """
        anketa = Anketa(json_data)
        anketa.parse_anketa()

        return ""
    
bp.add_url_rule("/pulse", view_func=PulseView.as_view("pulse"))
