import os
import shutil

from flask.views import MethodView
from flask  import request
from sqlalchemy.orm import Session

from . import bp
from ..utils.folders import Folders
from ..models.model import engine, Person, Message, Robot


class RobotsView(MethodView):

    def post(self):
        """
        Post method for the given API endpoint.
        """
        json_data = request.get_json()
        robot_path = json_data.pop("path")
        with Session(engine) as session:
            candidate = session.get(Person, json_data.pop("id"))

            if not candidate:
                session.add(
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
                        session.add(Message(message=f"{e}", user_id=candidate.user_id))

                session.add(Robot(**json_data | {"person_id": candidate.id}))
                session.add(
                    Message(
                        message=f"Автоматическая проверка {candidate.surname} окончена",
                        user_id=candidate.user_id,
                    )
                )
            session.commit()
            return "", 201


bp.add_url_rule("/robot", view_func=RobotsView.as_view("robot"))
