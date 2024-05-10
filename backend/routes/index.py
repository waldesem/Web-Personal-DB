from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func

from ..utils.token import login_required
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


@index.get("/index/{flag}/{page}", status_code=200, response_model=SchemaPersons)
async def get_persons(
    flag: str,
    page: int,
    current_user: Annotated[User, Depends(login_required)],
    order: str = "asc",
    sort: str = "id",
    search: str = "",
):
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
            if search:
                query = search(query, "%{}%".format(search))

        result = session.paginate(query, page=page, per_page=16, error_out=False)
        return {
            "persons": result,
            "has_next": bool(result.has_next),
            "has_prev": bool(result.has_prev),
        }


@index.get("/information", status_code=200, dependencies=[Depends(login_required)])
async def get_information(start: str, end: str, region_id: int = 1) -> dict:
    with Session(engine) as session:
        query = (
            select(Check.conclusion_id, func.count(Check.id))
            .join(Person)
            .group_by(Check.conclusion_id)
            .filter(Person.region_id == region_id)
            .filter(Check.deadline.between(start, end))
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
