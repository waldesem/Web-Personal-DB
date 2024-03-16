from apiflask import EmptySchema
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import select

from . import bp
from .. import db
from ..models.model import Message
from ..models.schema import MessageSchema


@bp.doc(hide=True)
@jwt_required()
@bp.get("/messages")
def get_messages():
    """
    Get the serialized representation of the messages.
    """
    messages = db.session.execute(
        select(Message)
        .filter_by(user_id=current_user.id)
        .order_by(Message.created.desc())
        .limit(100)
    ).scalars().all()
    return {"messages": MessageSchema().dump(messages, many=True)}


@bp.doc(hide=True)
@bp.output(EmptySchema)
@jwt_required()
def delete_messages():
    """
    Deletes the current instance of the resource from the database.
    """
    messages = db.session.execute(
        select(Message).filter_by(user_id=current_user.id)
    ).scalars().all()
    if len(messages):
        for message in messages:
            db.session.delete(message)
        db.session.commit()
    return "", 204
