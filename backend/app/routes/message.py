from apiflask import EmptySchema
from flask import request
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
    def delete(self):
        """
        Deletes the current instance of the resource from the database.
        """
        json_data = request.get_json()
        if not json_data['id']:
            messages = db.session.execute(
                select(Message).filter_by(user_id=current_user.id)
            ).scalars().all()
            if len(messages):
                for message in messages:
                    db.session.delete(message)
        else:
            db.session.delete(db.session.get(Message, json_data["id"]))
        db.session.commit()
        return "", 204


bp.add_url_rule("/messages", view_func=MessageView.as_view("messages"))