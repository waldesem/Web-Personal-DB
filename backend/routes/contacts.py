from fastapi import APIRouter, Depends, Response
from sqlmodel import Session, select
from sqlalchemy_searchable import search

from ..config import Settings
from ..dependencies import login_required
from ..models.schema import SchemaConnections
from ..models.model import engine, Connect

connect = APIRouter(prefix="/connect", tags=["connect"])


@connect.get(
    "/{page}",
    status_code=200,
    response_model=SchemaConnections,
    dependencies=[Depends(login_required)],
)
async def get_connection(page: int, searches: str = ""):
    """
    Retrieves a paginated list of Connect objects based on the specified group and item.
    """
    with Session(engine) as session:
        names = session.exec(select(Connect.name)).scalars()
        companies = session.exec(select(Connect.company)).scalars()
        cities = session.exec(select(Connect.city)).scalars()
        query = select(Connect).order_by(Connect.id.desc())
    if searches:
        query = search(query, "%{}%".format(searches))
    pagination = query.offset((page - 1) * Settings.pagination).limit(Settings.pagination + 1)
    result = session.exec(pagination).all()
    has_next = True if len(result) > Settings.pagination else False
    return {
        "connects": pagination,
        "has_next": has_next,
        "names": list({name for name in names}),
        "companies": list({company for company in companies}),
        "cities": list({city for city in cities}),
    }


@connect.post("/", status_code=201, dependencies=[Depends(login_required)])
async def post_connection(json_data: Connect) -> dict:
    """
    Create a new connection.
    """
    with Session(engine) as session:
        session.add(Connect(**json_data))
        session.commit()
        return {"message": "Created"}


@connect.patch("/{item_id}", status_code=201, dependencies=[Depends(login_required)])
async def patch(item_id: int, json_data: Connect) -> dict:
    """
    Patch an item in the Connect table.
    """
    with Session(engine) as session:
        resp = session.get(Connect, item_id)
        for k, v in json_data.items():
            setattr(resp, k, v)
        session.commit()
        return {"message": "Updated"}


@connect.delete("/{item_id}", dependencies=[Depends(login_required)])
async def delete_connection(item_id: int) -> Response:
    """
    Deletes an item from the database.
    """
    with Session(engine) as session:
        resp = session.get(Connect, item_id)
        session.delete(resp)
        session.commit()
        return Response(status_code=204)
