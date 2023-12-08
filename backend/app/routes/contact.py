from apiflask import EmptySchema
from flask import request
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import bp
from ..models.model import Group, Connect, engine
from ..models.schema import ConnectSchema, Pagination


class ContactsView(MethodView):
    """
    The ContactsView class is a subclass of the MethodView class from the flask.views module.
    It provides methods for retrieving paginated list of Connect objects based on the specified group and item.
    """
    decorators = [jwt_required(), bp.doc(hide=True)]

    def __init__(self):
        self.pagination = 16
        self.schema = ConnectSchema()

    async def post(self, group, item):
        """
        Retrieves a paginated list of Connect objects based on the specified group and item.
        """
        async with AsyncSession(engine) as session:
            async with session.begin():
                response = request.get_json()
                datalist = await session.execute(
                    select(Connect.company, Connect.city)
                    )
                group_id = await session.execute(
                    select(Group.id)
                    .filter_by(group=group)
                    )  
                query = await session.execute(
                    select(Connect)
                    .filter(Connect.company.like('%{}%'.format(response['search'])))
                    .filter(Connect.group_id == group_id)
                    .order_by(Connect.id.desc())
                )

                pagination = Pagination(query.scalars(), self.pagination, item)
                return [self.schema.dump(pagination, many=True),
                        {'has_next': pagination.has_next()},
                        {'has_prev': pagination.has_prev()},
                        {'companies': list({company[0] for company in datalist})},
                        {'cities': list({city[1] for city in datalist})}]

bp.add_url_rule('/connects/<group>/<int:item>', view_func=ContactsView.as_view('connects'))


class ConnnectView(MethodView):
    decorators = [jwt_required(), bp.doc(hide=True)]

    @bp.input(ConnectSchema)
    async def post(self, group, json_data):
        """
        Create a new connection.
        """
        async with AsyncSession(engine) as session:
            async with session.begin():
                group_id = await session.execute(
                    select(Group.id)
                    .filter_by(group=group)
                    )
                connect = Connect(**json_data | {
                    "group_id": group_id.scalar_one_or_none()
                    })
                session.add(connect)
                await session.flush()
                item = connect.id
                await engine.dispose()
                return {'item_id': item}

    @bp.input(ConnectSchema)
    async def patch(self, item, json_data):
        """
        Patch an item in the Connect table.
        """
        async with AsyncSession(engine) as session:
            async with session.begin():
                resp = await session.execute(
                    select(Connect)
                    .filter_by(id=item)
                )
                for k, v in json_data.items():
                    setattr(resp.scalar_one_or_none(), k, v)
                await engine.dispose()
                return {'item_id': item}

    @bp.output(EmptySchema)
    async def delete(self, item):
        """
        Deletes an item from the database.
        """
        async with AsyncSession(engine) as session:
            async with session.begin():
                resp = await session.execute(
                    select(Connect)
                    .filter_by(id=item)
                )
                session.delete(resp.scalar_one_or_none())
                await engine.dispose()
                return '', 204

contacts_view = ConnnectView.as_view('connect')
bp.add_url_rule('/connect/<group>', view_func=contacts_view, methods=['POST'])
bp.add_url_rule('/connect/<int:item>', view_func=contacts_view, methods=['PATCH', 'DELETE'])
