from apiflask import EmptySchema
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy import select

from . import bp
from .. import db
from .login import roles_required
from ..models.classes import Roles
from ..models.model import Message
from ..models.schema import MessageSchema


class MessagesView(MethodView):


    decorators = [roles_required(Roles.user.value), bp.doc(hide=True)]

    def get(self):
        """
        Get the serialized representation of the messages.
        """
        messages = db.session.execute(
            select(Message)
            .filter_by(user_id=current_user.id)
            .order_by(Message.created.desc())
            .limit(100)
        ).all()
        return {"messages": MessageSchema().dump(messages, many=True)}

    @bp.output(EmptySchema)
    def delete(self):
        """
        Deletes the current instance of the resource from the database.
        """
        messages = db.session.execute(
            select(Message).filter_by(user_id=current_user.id)
        ).all()
        if len(messages):
            for message in messages:
                db.session.delete(message)
            db.session.commit()
            return {"message": "Deleted"}, 204
        else:
            return {"message": "Empty"}, 201


bp.add_url_rule("/messages", view_func=MessagesView.as_view("messages"))
