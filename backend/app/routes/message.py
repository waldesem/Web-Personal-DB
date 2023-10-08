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
        self.messages = db.session.query(Report). \
            filter(Report.status == Status.new.value,
                   Report.user_id == current_user.id).all()

    def get(self):
        """
        Get the serialized representation of the messages.

        Returns:
            A serialized representation of the messages.
        """
        return self.schema.dump(self.messages, many=True)

    @bp.output(EmptySchema, status_code=204)
    def delete(self):
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


bp.add_url_rule('/messages', view_func=MessagesView.as_view('messages'))
