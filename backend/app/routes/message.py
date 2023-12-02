from apiflask import EmptySchema
from flask_jwt_extended import jwt_required, current_user
from flask.views import MethodView
from sqlalchemy import select

from . import bp
from ..models.model import Report, async_session
from ..models.schema import MessageSchema
from ..models.classes import Statuses


class MessagesView(MethodView):
    decorators = [jwt_required(), bp.doc(hide=True)]

    async def __init__(self) -> None:
        self.pagination = 16
        self.schema = MessageSchema()
        async with async_session() as session:
            self.messages = await session.execute(select(Report)).\
                filter(Report.user_id == current_user.id)

    async def get(self, action, page=1):
        """
        Get the serialized representation of the messages.

        Returns:
            A serialized representation of the messages.
        """            
        if action == 'new':
            async with async_session() as session:
                self.messages = self.messages.\
                    filter(Report.status == Statuses.new.value).all()
                return self.schema.dump(self.messages, many=True)

        elif action == 'all':
            self.messages = self.messages.group_by(Report.status).\
                order_by(Report.status, Report.create.desc())
        elif action == 'read':
            self.messages = self.messages.filter(Report.status == Statuses.new.value)
            for message in self.messages:
                message.status = Statuses.finish.value
            await session.commit()
        
        result = self.messages.paginate(page=page,
                    per_page=self.pagination,
                    error_out=False)
        
        has_next, has_prev = int(result.has_next), int(result.has_prev)
        
        return [self.schema.dump(result, many=True),
                {'has_next': has_next, "has_prev": has_prev}]


    @bp.output(EmptySchema, status_code=204)
    async def delete(self, action):
        """
        Deletes the current instance of the resource from the database.
        Returns:
            str: An empty string indicating a successful deletion.
        Raises:
            None
        """
        async with async_session() as session:
            for message in self.messages:
                await session.delete(message)
            await session.commit()
            return self.get(action)


bp.add_url_rule('/messages/action', view_func=MessagesView.as_view('messages'))
