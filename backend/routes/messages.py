from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlmodel import Session, select

from ..dependencies import login_required   
from ..models.model import engine, User, Message


msg = APIRouter(prefix="/messages", tags=["messages"])


@msg.get("/", status_code=200)
async def get_messages(
    current_user: Annotated[User, Depends(login_required)],
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


@msg.delete("/{item_id}", status_code=204)
async def delete(
    current_user: Annotated[User, Depends(login_required)],
    item_id: int | None = None,
):
    """
    Deletes the current instance of the resource from the database.
    """
    with Session(engine) as session:
        if not item_id:
            messages = (
                session.exec(
                    select(Message).filter_by(user_id=current_user.id)
                )
                .all()
            )
            if len(messages):
                for message in messages:
                    session.delete(message)
        else:
            session.delete(session.get(Message, item_id))
        session.commit()
        return Response(status_code=204)
