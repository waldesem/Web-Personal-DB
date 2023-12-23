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
        messages = select(Message).filter_by(user_id=current_user.id)\
            .order_by(Message.create.desc())
        if action == 'new':
            messages = messages.filter(Message.status == Statuses.new.name)
        elif action == 'read':
            self.read_messages(messages)
        result = db.paginate(messages, page=page, per_page=16, error_out=False)
        return [
            MessageSchema().dump(result, many=True), 
            {
                'has_next': result.has_next, 
                "has_prev": result.has_prev
            }
        ]

    def read_messages(self, messages):
        unread = messages.filter(Message.status == Statuses.new.name)
        results = db.session.execute(unread).scalars().all()
        if len(results):
            for message in results:
                message.status = Statuses.reply.name
            db.session.commit()
        self.get('all')

    @bp.output(EmptySchema, status_code=204)
    def delete(self, action):
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
        return self.get('all')

messages_view = MessagesView.as_view('messages')
bp.add_url_rule('/messages/<action>/<int:page>', view_func=messages_view, methods=['GET'])
bp.add_url_rule('/messages/<action>', view_func=messages_view, methods=['DELETE'])
