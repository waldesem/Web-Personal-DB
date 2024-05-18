from enum import Enum
from typing import Annotated, Union

import aiohttp
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select

from ..dependencies import Permission
from ..utils.parsers import Resume, Anketa
from ..models.schema import ResumeSchemaApi
from ..models.classes import Roles, Statuses, Conclusions
from ..models.model import (
    User,
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


person = APIRouter(prefix="/person", tags=["person"])


@person.get("/resume/{person_id}", status_code=201)
async def get_resume(
    person_id,
    action: str,
    current_user: Annotated[User, Depends(Permission(roles=[Roles.user.value]))],
):
    person = ResumeAction(person_id)
    if action == "status":
        person.change_status(Statuses.update.value)
        return {"message": action}, 201

    if action == "self" and not person.anketa.user_id:
        with Session(engine) as session:
            session.add(
                Message(
                    message=f"Aнкета ID #{person_id} принята в работу",
                    user_id=current_user.id,
                )
            )
            session.commit()
            person.change_status(Statuses.manual.value, current_user.id)
            return {"message": action}

    elif action == "send":
        if person.anketa.status_id in (
            Status.get_id(Statuses.new.value),
            Status.get_id(Statuses.update.value),
            Status.get_id(Statuses.repeat.value),
            Status.get_id(Statuses.manual.value),
            Status.get_id(Statuses.robot.value),
        ):
            status = await person.send_anketa()
            if status == "send":
                person.change_status(Statuses.robot.value, current_user.id)
            return {"message": status}
        else:
            raise HTTPException(status_code=400, detail="Невозможно отправить анкету")
    return Person.model_dump(person.anketa)


@person.delete(
    "/resume/{person_id}",
    status_code=204,
    dependencies=[Depends(Permission(roles=[Roles.user.value]))],
)
async def delete_resume(person_id):
    person = ResumeAction(person_id)
    person.del_person()
    return Response(status_code=204)


@person.patch(
    "/resume/{person_id}",
    status_code=201,
    dependencies=[Depends(Permission(roles=[Roles.user.value]))],
)
async def patch_resume(person_id, json_data: Person):
    resume = Resume(json_data)
    with Session(engine) as session:
        resume.update_resume(session.get(Person, person_id))
    return {"message": person_id}


@person.post(
    "/resume",
    status_code=201,
    dependencies=[Depends(Permission(roles=[Roles.user.value]))],
)
async def post_resume(json_data: Person):
    resume = Resume(json_data)
    person_id = resume.check_resume()
    return {"message": person_id}


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

    async def send_anketa(self):
        with Session(engine) as session:
            docum = session.exec(
                select(Document)
                .filter_by(person_id=self.anketa.id)
                .order_by(Document.id.desc())
            ).scalar_one_or_none()
            addr = session.exec(
                select(Address)
                .filter(
                    Address.person_id == self.anketa.id,
                    Address.view.ilike("%регистрац%"),
                )
                .order_by(Address.id.desc())
            ).scalar_one_or_none()
            if not docum or not addr:
                return "error"
            serial = ResumeSchemaApi.model_dump(
                {
                    "id": self.anketa.id,
                    "surname": self.anketa.surname,
                    "firstname": self.anketa.firstname,
                    "patronymic": self.anketa.patronymic,
                    "birthday": self.anketa.birthday,
                    "birthplace": self.anketa.birthplace,
                    "snils": self.anketa.snils,
                    "inn": self.anketa.inn,
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
                        print(response.status)
                        print(await response.text())
                return "send"
            except aiohttp.ClientConnectorError as e:
                print(e)
                return "error"


class Models(Enum):
    previous = Previous
    staff = Staff
    document = Document
    address = Address
    contact = Contact
    education = Education
    workplace = Workplace
    relation = Relation
    affilation = Affilation
    check = Check
    robot = Robot
    poligraf = Poligraf
    investigation = Investigation
    inquiry = Inquiry


@person.get(
    "/{item}/{item_id}",
    status_code=200,
    response_model=Models,
    dependencies=[Depends(Permission(roles=[Roles.user.value]))],
)
async def get_item(item: Models, item_id):
    query = (
        select(Models[item].value)
        .filter_by(person_id=item_id)
        .order_by(Models[item].value.id.desc())
    )
    with Session(engine) as session:
        result = session.exec(query).all()
    return result


@person.post("/{item}/{item_id}", status_code=201)
async def post_item(
    item: Models,
    json_data: Union[
        Previous,
        Staff,
        Document,
        Address,
        Contact,
        Education,
        Workplace,
        Relation,
        Affilation,
        Check,
        Robot,
        Inquiry,
        Investigation,
        Poligraf,
    ],
    item_id: int,
    current_user: Annotated[User, Depends(Permission(roles=[Roles.user.value]))],
):
    setattr(json_data, "person_id", item_id)

    with Session(engine) as session:
        if item == "previous":
            person = session.get(Person, item_id)
            prev = session.exec(
                select(Person).filter(
                    Person.surname.ilike(json_data.surname),
                    Person.firstname.ilike(json_data.firstname),
                    Person.patronymic.ilike(json_data.patronymic),
                    Person.birthday == person.birthday,
                )
            ).scalar_one_or_none()
            if prev:
                session.add(
                    Message(
                        message=f"Кандидат ранее проверялся ID: {prev.id}",
                        user_id=current_user.id,
                    )
                )
                Anketa.add_relation("Одно лицо", prev.id, item_id)
        if item == "workplace":
            setattr(
                json_data,
                "now_work",
                True if json_data.now_work else False,
            )
        if item == "relation":
            Anketa.add_relation(
                json_data["relation"], item_id, json_data["relation_id"]
            )

        if item in ["check", "poligraf", "inquiry", "investigation"]:
            setattr(json_data, "user_id", current_user.id)

            if item == "check":
                person = session.get(Person, item_id)
                if json_data.conclusion_id == Conclusion.get_id(
                    Conclusions.saved.value
                ):
                    person.status_id = Status.get_id(Statuses.save.value)
                else:
                    person.status_id = (
                        Status.get_id(Statuses.poligraf.value)
                        if json_data.pfo
                        else Status.get_id(Statuses.finish.value)
                    )
                    person.user_id = None

            if item == "poligraf":
                person = session.get(Person, item_id)
                if person.status_id == Status.get_id(Statuses.poligraf.value):
                    person.status_id = Status.get_id(Statuses.finish.value)

        session.add(json_data)
        session.commit()
        return "", 201


@person.patch(
    "/{item}/{item_id}",
    status_code=201,
    dependencies=[Depends(Permission(roles=[Roles.user.value]))],
)
async def patch_item(
    item: Models,
    item_id: int,
    json_data: Union[
        Previous,
        Staff,
        Document,
        Address,
        Contact,
        Education,
        Workplace,
        Relation,
        Affilation,
        Check,
        Robot,
        Inquiry,
        Investigation,
        Poligraf,
    ],
):
    with Session(engine) as session:
        result = session.get(Models[item], item_id)
        if result:
            for k, v in json_data.__dict__.items():
                if hasattr(result, k):
                    setattr(result, k, v)
            session.commit()
            return Response(status_code=204)
        raise HTTPException(status_code=404)


@person.delete(
    "/{item}/{item_id}",
    status_code=204,
    dependencies=[Depends(Permission(roles=[Roles.user.value]))],
)
async def delete(item: Models, item_id: int):
    with Session(engine) as session:
        result = session.get(Models[item], item_id)
        if result:
            session.delete(result)
            session.commit()
            return Response(status_code=204)
        raise HTTPException(status_code=404)
