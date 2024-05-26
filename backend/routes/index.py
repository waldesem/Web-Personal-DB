from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, func, select

from ..config import settings
from ..dependencies import login_required
from ..models.classes import Statuses
from ..models.model import (
    Check,
    Conclusion,
    Motivation,
    Person,
    Region,
    Role,
    Status,
    User,
    engine,
)
from ..models.schema import SchemaPersons, SchemaPersonsInput

index = APIRouter()


@index.post("/index/{flag}/{page}", status_code=200)
async def post_persons(
    flag: str,
    page: int,
    order: str,
    sort: str,
    searches: SchemaPersonsInput,
    current_user: Annotated[User, Depends(login_required)],
) -> SchemaPersons:
    with Session(engine) as session:
        query = (
            select(Person)
            if current_user.region_id == 1
            else select(Person).filter_by(region_id=current_user.region_id)
        )
        sort_attribute = getattr(Person, sort)
        query = (
            query.order_by(sort_attribute.asc())
            if order == "asc"
            else query.order_by(sort_attribute.desc())
        )

        if flag == "officer":
            query = query.filter(
                Person.status_id.notin_(
                    [
                        Status().get_id(Statuses.finish.value),
                        Status().get_id(Statuses.cancel.value),
                    ]
                ),
                Person.user_id == current_user.id,
            )
        elif flag == "search":
            if searches:
                query = select(Person).filter(
                    Person.surname.contains(searches.surname),
                    Person.region_id == current_user.region_id,
                )
        elif flag == "extended":
            print(datetime.strptime(searches.birthday, "%Y-%m-%d").date())
            query = select(Person).filter(
                Person.surname.ilike(f"%{searches.surname}%" if searches.surname else "%"),
                Person.firstname.ilike(f"%{searches.firstname}%" if searches.firstname else "%"),
                Person.patronymic.ilike(f"%{searches.patronymic}%" if searches.patronymic else "%"),
                Person.birthday == datetime.strptime(searches.birthday, "%Y-%m-%d").date() if searches.birthday else None,
            )

        pagination = query.offset((page - 1) * settings.pagination).limit(
            settings.pagination + 1
        )
        result = session.exec(pagination).all()
        has_next = True if len(result) > settings.pagination else False
        return {
            "persons": result if not has_next else result[:-1],
            "has_next": has_next,
        }
    

@index.get("/information", status_code=200, dependencies=[Depends(login_required)])
async def get_information(start: str, end: str, region_id: int = 1) -> dict:
    with Session(engine) as session:
        query = (
            select(Check.conclusion_id, func.count(Check.id))
            .join(Person)
            .group_by(Check.conclusion_id)
            .filter(Person.region_id == region_id)
            .filter(Check.created.between(start, end))
        )
        result = session.exec(query).all()
        return dict(map(lambda x: (x[1], x[0]), result))


@index.get("/classes", status_code=200)
async def get_classes():
    models = [Conclusion, Motivation, Role, Status, Region, User]
    with Session(engine) as session:
        queries = [session.exec(select(model)).all() for model in models]
        return [
            dict(
                (
                    sub.id,
                    (
                        sub.conclusion
                        if hasattr(sub, "conclusion")
                        else (
                            sub.motivation
                            if hasattr(sub, "motivation")
                            else (
                                sub.role
                                if hasattr(sub, "role")
                                else (
                                    sub.status
                                    if hasattr(sub, "status")
                                    else (
                                        sub.region
                                        if hasattr(sub, "region")
                                        else (
                                            sub.fullname
                                            if hasattr(sub, "fullname")
                                            else None
                                        )
                                    )
                                )
                            )
                        )
                    ),
                )
                for sub in sublist
            )
            for sublist in queries
        ]
