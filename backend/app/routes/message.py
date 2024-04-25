from apiflask import EmptySchema
from flask.views import MethodView
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import select

from . import bp
from ..models.model import db, Message
from ..models.schema import MessageSchema


class MessageView(MethodView):

    decorators = [jwt_required(), bp.doc(hide=True)]

    def get(self):
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


    @bp.output(EmptySchema)
    def delete(self, item_id):
        """
        Deletes the current instance of the resource from the database.
        """
        if not item_id:
            messages = db.session.execute(
                select(Message).filter_by(user_id=current_user.id)
            ).scalars().all()
            if len(messages):
                for message in messages:
                    db.session.delete(message)
        else:
            db.session.delete(db.session.get(Message, item_id))
        db.session.commit()
        return "", 204

message_view = MessageView.as_view("messages")
bp.add_url_rule("/messages", view_func=message_view, methods=["GET"])
bp.add_url_rule("/messages/<int:item_id>", view_func=message_view, methods=["DELETE"])