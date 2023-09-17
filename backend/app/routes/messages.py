from flask_jwt_extended import jwt_required, current_user

from . import bp
from ..models.classes import Status
from ..models.model import db, Report
from ..models.schema import MessageSchema


@bp.get('/messages/<string:flag>')
@bp.doc(hide=True)
@jwt_required()
def get_messages(flag):
    """
    Retrieves messages based on a flag.
    Args:
        flag (str): The flag to determine the type of messages to retrieve.
    Returns:
        list: A list of messages retrieved based on the flag.
    """
    def update_messages():
        updates = db.session.query(Report).filter(Report.status == Status.new.value, 
                                                  Report.user_id == current_user.id).limit(16).all()
        return updates

    messages = update_messages()

    if flag == 'reply':
        for message in messages:
             db.session.delete(message)
        db.session.commit()
        messages = update_messages()
    schema = MessageSchema()
    messages = schema.dump(messages, many=True)
    return messages
