import os
import shutil

import aiohttp
from fastapi import APIRouter, Response
from sqlmodel import Session, select

from ..models.classes import Statuses
from ..models.model import Address, Document, Message, Person, Robot, Status, engine
from ..models.schema import AnketaSchemaApi, ResumeSchemaApi, RobotSchema
from ..utils.folders import Folders
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
            session.add_all(
                [
                    Robot(json_data),
                    Message(
                        message=f"Автоматическая проверка {candidate.surname} окончена",
                        user_id=candidate.user_id,
                    ),
                ]
            )
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


async def send_anketa(person_id):
    with Session(engine) as session:
        anketa = session.get(Person, person_id)
        if anketa.status_id in (
            Status.get_id(Statuses.new.value),
            Status.get_id(Statuses.update.value),
            Status.get_id(Statuses.repeat.value),
            Status.get_id(Statuses.manual.value),
            Status.get_id(Statuses.robot.value),
        ):
            docum = session.exec(
                select(Document)
                .filter_by(person_id=anketa.id)
                .order_by(Document.id.desc())
            ).one_or_none()
            addr = session.exec(
                select(Address)
                .filter(
                    Address.person_id == anketa.id,
                    Address.view.ilike("%регистрац%"),
                )
                .order_by(Address.id.desc())
            ).one_or_none()
            if not docum or not addr:
                return "error"
            serial = ResumeSchemaApi.model_dump(
                {
                    "id": anketa.id,
                    "surname": anketa.surname,
                    "firstname": anketa.firstname,
                    "patronymic": anketa.patronymic,
                    "birthday": anketa.birthday,
                    "birthplace": anketa.birthplace,
                    "snils": anketa.snils,
                    "inn": anketa.inn,
                    "series": docum.series,
                    "number": docum.number,
                    "agency": docum.agency,
                    "issue": docum.issue,
                    "address": addr.address,
                }
            )
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url="http://127.0.0.1:5001", json=serial, timeout=5
                    ) as response:
                        print(await response.text())
                        return response.status
            except aiohttp.ClientConnectorError as e:
                return Response(status_code=500, content=e)
