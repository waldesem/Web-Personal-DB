from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from sqlalchemy_searchable import search

from ..config import Config
from ..dependencies import login_required
from ..models.classes import Statuses
from ..models.schema import SchemaPersons
from ..models.model import (
    engine,
    Person,
    Check,
    Conclusion,
    Role,
    Status,
    Region,
    User,
)

index = APIRouter()


@index.get("/index/{flag}/{page}", status_code=200)
async def get_persons(
    flag: str,
    page: int,
    order: str,
    sort: str,
    searches: str,
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
        else:
            if searches:
                query = search(query, "%{}%".format(searches))
        pagination = query.offset((page - 1) * Config.PAGINATION).limit(Config.PAGINATION + 1)
        result = session.exec(pagination).all()
        has_next = True if len(result) > Config.PAGINATION else False
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
        result = session.exec(query).scalars()
        return dict(map(lambda x: (x[1], x[0]), result))


@index.get("/classes", status_code=200)
async def get_classes():
    models = [Conclusion, Role, Status, Region, User]
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
                    ),
                )
                for sub in sublist
            )
            for sublist in queries
        ]
