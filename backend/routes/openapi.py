import os
import shutil

from fastapi import APIRouter, Response
from sqlmodel import Session

from ..utils.folders import Folders
from ..models.schema import  RobotSchema, AnketaSchemaApi
from ..models.model import engine, Person, Message, Robot
from ..utils.parsers import Anketa


api = APIRouter(prefix="/api", tags=["api"])


@api.post("/robot")
async def post_robot(json_data: RobotSchema):
    """
    Post method for the given API endpoint.
    """

    with Session(engine) as session:
        candidate = session.get(Person, json_data.pop("id"))
        robot_path = json_data.path
        delattr(json_data, "path")
        delattr(json_data, "id")
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

            setattr(json_data, "person_id", candidate.id)
            session.add_all([
                Robot(json_data),
                Message(
                    message=f"Автоматическая проверка {candidate.surname} окончена",
                    user_id=candidate.user_id,
                )
            ])
        session.commit()
        return Response(status_code=204)


@api.post("/pulse")
async def post(json_data: AnketaSchemaApi):
    """
    Post method for the given API endpoint.
    """
    anketa = Anketa(json_data)
    anketa.parse_anketa()

    return Response(status_code=204)
