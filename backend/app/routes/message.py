from apiflask import EmptySchema
from flask_jwt_extended import jwt_required, current_user
from flask.views import MethodView

from . import bp
from .. import db
from ..models.classes import Statuses
from ..models.model import Message
from ..models.schema import MessageSchema


class MessagesView(MethodView):

    decorators = [jwt_required(), bp.doc(hide=True)]

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        Returns:
            None
        """
        self.pagination = 16
        self.schema = MessageSchema()
        self.messages = db.session.query(Message).\
            filter(Message.user_id == current_user.id).all()

    def get(self, action, page=1):
        """
        Get the serialized representation of the messages.
        Returns:
            A serialized representation of the messages.
        """
        if action == 'new':
            self.messages = self.messages.\
                filter(Message.status == Statuses.new.value).all()
            return self.schema.dump(self.messages, many=True)

        elif action == 'all':
            self.messages = self.messages
            self.messages = self.messages.group_by(Message.status).\
                order_by(Message.status, Message.create.desc())
        elif action == 'read':
            for message in self.messages:
                message.status = Statuses.finish.value
            db.session.commit()

        result = self.messages.paginate(page=page,
                    per_page=self.pagination,
                    error_out=False)

        has_next, has_prev = int(result.has_next), int(result.has_prev)

        return [self.schema.dump(result, many=True),
                {'has_next': has_next, "has_prev": has_prev}]


    @bp.output(EmptySchema, status_code=204)
    def delete(self, action):
        """
        Deletes the current instance of the resource from the database.
        Returns:
            str: An empty string indicating a successful deletion.
        Raises:
            None
        """
        for message in self.messages:
            db.session.delete(message)
        db.session.commit()
        return self.get(action)

bp.add_url_rule('/messages/action', view_func=MessagesView.as_view('messages'))