from flask_jwt_extended import jwt_required, current_user
from flask.views import MethodView

from . import bp
from .. import db
from ..models.classes import Status
from ..models.model import Report
from ..models.schema import MessagesSchema


class MessagesView(MethodView):

    decorators = [jwt_required(), bp.doc(hide=True), bp.output(MessagesSchema)]

    def __init__(self) -> None:
        super().__init__()
        self.messages = db.session.query(Report).filter(Report.status == Status.new.value, 
                                                        Report.user_id == current_user.id).all()

    def get(self):
        return self.messages
    
    def delete(self):
        for message in self.messages:
            db.session.delete(message)
        db.session.commit()
        return []

bp.add_url_rule('/messages', view_func=MessagesView.as_view('messages'))

