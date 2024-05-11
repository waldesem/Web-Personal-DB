from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlmodel import Session, select

from ..utils.token import Permission
from ..models.classes import Roles
from ..models.model import engine, User, Message


msg = APIRouter(prefix="/users", tags=["users"])


@msg.get("/messages")
async def get_messages(
    current_user: Annotated[User, Depends(Permission(roles=[Roles.user.value]))]
) -> list[Message]:
    """
    Get the serialized representation of the messages.
    """
    with Session(engine) as session:
        return session.exec(
            select(Message)
            .filter_by(user_id=current_user.id)
            .order_by(Message.created.desc())
            .limit(100)
        ).all()


@msg.delete("/messages/{item_id}")
async def delete(
    current_user: Annotated[User, Depends(Permission(roles=[Roles.user.value]))],
    item_id: int | None = None,
):
    """
    Deletes the current instance of the resource from the database.
    """
    with Session(engine) as session:
        if not item_id:
            messages = (
                session.exec(select(Message).filter_by(user_id=current_user.id))
                .scalars()
                .all()
            )
            if len(messages):
                for message in messages:
                    session.delete(message)
        else:
            session.delete(session.get(Message, item_id))
        session.commit()
        return Response(status_code=204)
