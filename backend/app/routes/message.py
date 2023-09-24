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
        self.schema = MessageSchema()
        self.messages = db.session.query(Report).\
            filter(Report.status == Status.new.value, 
                   Report.user_id == current_user.id).all()

    def get(self):
        return self.schema.dump(self.messages, many=True)
    
    @bp.output(EmptySchema, status_code=204)
    def delete(self):
        db.session.delete(self.messages)
        db.session.commit()
        return ''

bp.add_url_rule('/messages', view_func=MessagesView.as_view('messages'))

