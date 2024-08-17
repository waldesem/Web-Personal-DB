from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select

from ..dependencies import Permission
from ..models.classes import Conclusions, Roles, Statuses
from ..models.model import (
    Address,
    Affilation,
    Check,
    Conclusion,
    Contact,
    Document,
    Education,
    Inquiry,
    Investigation,
    Person,
    Poligraf,
    Previous,
    Relation,
    Robot,
    Staff,
    Status,
    User,
    Workplace,
    engine,
)
from ..models.schema import Models
from ..routes.api import send_anketa
from ..utils.parsers import Anketa, Resume

person = APIRouter(prefix="/person", tags=["person"])


@person.get("/resume/{person_id}", status_code=200)
async def get_resume(
    person_id,
    action: str,
    current_user: Annotated[User, Depends(Permission(roles=[Roles.user.value]))],
):
    if action == "status":
        change_status(Statuses.update.value, person_id)
        return Response(status_code=201)

    elif action == "self":
        change_status(Statuses.manual.value, person_id, current_user.id)
        return Response(status_code=202)

    elif action == "send":
        status = await send_anketa()
        if status == 200:
            change_status(Statuses.robot.value, person_id, current_user.id)
            return Response(status_code=203)
        raise HTTPException(status_code=400, detail="Невозможно отправить анкету")
    with Session(engine) as session:
        anketa = session.get(Person, person_id)
        return Person.model_dump(anketa)


@person.delete(
    "/resume/{person_id}",
    dependencies=[Depends(Permission(roles=[Roles.user.value]))],
)
async def delete_resume(person_id):
    with Session(engine) as session:
        anketa = session.get(Person, person_id)
        session.delete(anketa)
        session.commit()
        return Response(status_code=204)


@person.patch(
    "/resume/{person_id}",
    dependencies=[Depends(Permission(roles=[Roles.user.value]))],
)
async def patch_resume(person_id, json_data: Person):
    resume = Resume(json_data)
    with Session(engine) as session:
        resume.update_resume(session.get(Person, person_id))
        return Response(status_code=201)


@person.post(
    "/resume",
    status_code=201,
    dependencies=[Depends(Permission(roles=[Roles.user.value]))],
)
async def post_resume(json_data: Person):
    resume = Resume(json_data)
    person_id = resume.check_resume()
    return {"message": person_id}


def change_status(status, person_id, user_id=None):
    with Session(engine) as session:
        anketa = session.get(Person, person_id)
        anketa.status_id = Status.get_id(status)
        anketa.user_id = user_id
        session.commit()


@person.get(
    "/{item}/{item_id}",
    status_code=200,
    dependencies=[Depends(Permission(roles=[Roles.user.value]))],
)
async def get_item(item, item_id):
    with Session(engine) as session:
        query = (
            select(Models[item].value)
            .filter_by(person_id=item_id)
            .order_by(Models[item].value.id.desc())
        )
        result = session.exec(query).all()
        return [res.model_dump() for res in result]


@person.post("/{action}/{item}/{item_id}", status_code=201)
async def post_item(
    action: str,
    item: str,
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
    with Session(engine) as session:
        if action == "create":
            setattr(json_data, "person_id", item_id)

            if item == "previous":
                person = session.get(Person, item_id)
                prev = session.exec(
                    select(Person).filter(
                        Person.surname.ilike(json_data.surname),
                        Person.firstname.ilike(json_data.firstname),
                        Person.patronymic.ilike(json_data.patronymic),
                        Person.birthday == person.birthday,
                    )
                ).one_or_none()
                if prev:
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
        else:
            result = session.get(Models[item].value, item_id)
            if result:
                for k, v in json_data.__dict__.items():
                    if hasattr(result, k):
                        setattr(result, k, v)
                session.commit()
                return Response(status_code=201)
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
