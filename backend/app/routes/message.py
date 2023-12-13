from apiflask import EmptySchema
from flask_jwt_extended import jwt_required, current_user
from flask.views import MethodView
from sqlalchemy import select

from . import bp
from .. import db
from ..models.classes import Statuses
from ..models.model import Message
from ..models.schema import MessageSchema


class MessagesView(MethodView):

    decorators = [jwt_required(), bp.doc(hide=True)]

    def get(self, action, page=1):
        """
        Get the serialized representation of the messages.
        """
        messages = select(Message).filter_by(user_id=current_user.id)
        if action == 'new':
            messages = messages.filter_by(status=Statuses.new.name)
        elif action == 'all':
            messages = messages.order_by(Message.status, Message.create.desc())
        elif action == 'read' and len(messages):
            for message in messages:
                message.status = Statuses.reply.name
            db.session.commit()
            messages = select(Message).filter_by(user_id=current_user.id)
        result = db.paginate(messages, page=page, per_page=16, error_out=False)
        return [
            MessageSchema().dump(messages, many=True), 
            {
                'has_next': result.has_next, 
                "has_prev": result.has_prev
            }
        ]


    @bp.output(EmptySchema, status_code=204)
    def delete(self, action):
        """
        Deletes the current instance of the resource from the database.
         """
        messages = db.session.execute(
             select(Message)
             .filter_by(user_id=current_user.id)
        ).scalars()
        for message in messages:
            db.session.delete(message)
        db.session.commit()
        return self.get(action)

messages_view = MessagesView.as_view('messages')
bp.add_url_rule('/messages/<action>', view_func=messages_view, methods=['GET'])
bp.add_url_rule('/messages', view_func=messages_view, methods=['DELETE'])
