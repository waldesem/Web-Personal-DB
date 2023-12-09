from apiflask import EmptySchema
from flask_jwt_extended import get_current_user, jwt_required
from flask.views import MethodView
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import bp
from ..models.model import Message, engine
from ..models.schema import MessageSchema
from ..models.classes import Statuses
from ..models.paginate import Pagination


class MessagesView(MethodView):
    """
    The MessagesView class is a subclass of the MethodView class from the flask.views module.
    It provides methods for retrieving paginated list of Connect objects based on the specified group and item.
    """
    decorators = [jwt_required(), bp.doc(hide=True)]

    async def __init__(self) -> None:
        self.pagination = 16
        self.schema = MessageSchema()
    
    async def get(self, action, page=1):
        """
        Get the serialized representation of the messages.
         """
        async with AsyncSession(engine) as session:
            async with session.begin():
                query = await session.execute(
                    select(Message)
                    .filter(Message.user_id == get_current_user().id)
                )
                if action == 'new':
                    messages = query.filter(Message.status == Statuses.new.value).all()
                    return self.schema.dump(messages, many=True)
            
                elif action == 'all':
                    messages = query.group_by(Message.status).\
                        order_by(Message.status, Message.create.desc()).all()
                    
                elif action == 'read':
                    messages = query.filter(Message.status == Statuses.new.value).all()
                    for message in messages:
                        message.status = Statuses.finish.value

                await engine.dispose()

                pagination = Pagination(messages, self.pagination, page)
                return [
                    self.schema.dump(pagination.paginate(), many=True),
                    {
                        'has_next': pagination.has_next(), 
                        "has_prev": pagination.has_prev()
                    }
                ]
    
    @bp.output(EmptySchema)
    async def delete(self, action):
        """
        Deletes the current instance of the resource from the database.
        """
        async with AsyncSession(engine) as session: 
            async with session.begin():
                messages = await session.execute(
                    select(Message)
                    .filter(Message.user_id == get_current_user().id)
                )
                for message in messages.scalars():
                    session.delete(message)
                await engine.dispose()
                return "", 204
        
bp.add_url_rule('/messages/action', view_func=MessagesView.as_view('messages'))
