from apiflask import EmptySchema
from flask.views import MethodView
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import select

from config import Config
from . import bp_message
from ... import db
from ...models.classes import Statuses
from ...models.model import Message
from ...models.schema import MessageSchema, ActionSchema


class MessagesView(MethodView):

    decorators = [jwt_required(), bp_message.doc(hide=True)]

    @bp_message.input(ActionSchema, location="query")
    def get(self, page, query_data):
        """
        Get the serialized representation of the messages.
        """
        action = query_data.get("action")
        messages = (
            select(Message)
            .filter_by(user_id=current_user.id)
            .order_by(Message.created.desc())
        )
        if action == "new":
            messages = messages.filter(Message.status == Statuses.new.name)
        elif action == "read":
            unreaded = messages.filter(Message.status == Statuses.new.name)
            results = db.session.execute(unreaded).scalars().all()
            if len(results):
                for result in results:
                    result.status = Statuses.reply.name
            db.session.commit()  
        result = db.paginate(
            messages,
            page=page if page else 1,
            per_page=Config.PAGINATION,
            error_out=False,
        )
        return [
            MessageSchema().dump(result, many=True),
            {"has_next": result.has_next, "has_prev": result.has_prev},
        ]

    @bp_message.output(EmptySchema)
    def delete(self):
        """
        Deletes the current instance of the resource from the database.
        """
        messages = db.session.execute(
            select(Message)
            .filter_by(user_id=current_user.id)
        ).all()
        if len(messages):
            for message in messages:
                db.session.delete(message)
            db.session.commit()
            return {"message": "Deleted"}, 204
        else:
            return {"message": "Empty"}, 201


messages_view = MessagesView.as_view("messages")
bp_message.add_url_rule("/messages/<int:page>", view_func=messages_view, methods=["GET"])
bp_message.add_url_rule("/messages", view_func=messages_view, methods=["DELETE"])