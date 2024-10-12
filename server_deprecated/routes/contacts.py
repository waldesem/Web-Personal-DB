from fastapi import APIRouter, Depends, Response
from sqlmodel import Session, select, text

from ..config import settings
from ..dependencies import login_required
from ..models.schema import SchemaConnections
from ..models.model import engine, Connect

connect = APIRouter(prefix="/connect", tags=["connect"])


@connect.get(
    "/{page}",
    status_code=200,
    dependencies=[Depends(login_required)],
)
async def get_connection(
    page: int, item: str = None, searches: str = None
) -> SchemaConnections:
    """
    Retrieves a paginated list of Connect objects based on the specified group and item.
    """
    with Session(engine) as session:
        query = select(Connect).order_by(Connect.id.desc())
        if searches:
            query = select(Connect).filter(text(f"{item} ilike '%{searches}%'"))
        pagination = query.offset((page - 1) * settings.pagination).limit(
            settings.pagination + 1
        )
        result = session.exec(pagination).all()
        has_next = True if len(result) > settings.pagination else False
        return {
            "contacts": result if not has_next else result[:-1],
            "has_next": has_next,
            "names": [name for name in session.exec(select(Connect.name)).all()],
            "companies": [
                company for company in session.exec(select(Connect.company)).all()
            ],
            "cities": [city for city in session.exec(select(Connect.city)).all()],
        }


@connect.post("/", status_code=201, dependencies=[Depends(login_required)])
async def post_connection(json_data: Connect):
    """
    Create a new connection.
    """
    with Session(engine) as session:
        session.add(json_data)
        session.commit()
        return Response(status_code=201)


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
        return Response(status_code=201)


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
