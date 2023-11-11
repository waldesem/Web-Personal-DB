from apiflask import EmptySchema
from flask_jwt_extended import jwt_required, current_user
from flask.views import MethodView

from . import bp
from .. import db
from ..models.classes import Status
from ..models.model import Report
from ..models.schema import MessageSchema


class MessagesView(MethodView):
    decorators = [jwt_required(), bp.doc(hide=True)]

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.

        Returns:
            None
        """
        self.schema = MessageSchema()
        self.messages = db.session.query(Report).\
            filter(Report.user_id == current_user.id).all()

    def get(self, action):
        """
        Get the serialized representation of the messages.

        Returns:
            A serialized representation of the messages.
        """
        if action == 'new':
            self.messages = self.messages.filter(Report.status == Status.new.value)
        elif action == 'all':
            self.messages = self.messages
        elif action == 'read':
            self.messages = self.messages.filter(Report.status == Status.new.value)
            for message in self.messages:
                message.status = Status.finish.value
            db.session.commit()
        return self.schema.dump(self.messages, many=True)


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
        return ''


bp.add_url_rule('/messages/action', view_func=MessagesView.as_view('messages'))
