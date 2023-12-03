from flask import request
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from sqlalchemy import select

from . import bp
from ..models.model import Group, Connect, async_session
from ..models.schema import ConnectSchema


class ContactsView(MethodView):
    """
    The ContactsView class is a subclass of the MethodView class from the flask.views module.
    It provides methods for retrieving paginated list of Connect objects based on the specified group and item.
    """
    decorators = [jwt_required(), bp.doc(hide=True)]

    async def post(self, group, item):
        """
        Retrieves a paginated list of Connect objects based on the specified group and item.

        Args:
            group (str): The name of the group.
            item (int): The page number of the pagination.

        Returns:
            list: A list containing the following:
                - A serialized version of the Connect objects matching the search criteria.
                - A dictionary indicating whether there is a next page.
                - A dictionary indicating whether there is a previous page.
                - A list of companies.
                - A list of cities.
        """
        async with async_session() as session:
            pagination = 16
            schema = ConnectSchema()
            response = request.get_json()
            datalist = await session.execute(select(Connect.company, Connect.city)).all()
            group_id = await session.execute(select(Group.id)).filter_by(group=group).scalar()            
            if response['search']:
                query = await Connect.query.search('%{}%'.format(response['search']))    
            else:
                query = await session.execute(select(Connect))

            result = query.order_by(Connect.id.desc()). \
                filter(Connect.group_id == group_id). \
                    paginate(page=item, per_page=pagination, error_out=False)

            return [schema.dump(result, many=True),
                    {'has_next': int(result.has_next)},
                    {'has_prev': int(result.has_prev)},
                    {'companies': list({company[0] for company in datalist})},
                    {'cities': list({city[1] for city in datalist})}]

bp.add_url_rule('/connects/<group>/<int:item>', view_func=ContactsView.as_view('connects'))


class ConnnectView(MethodView):
    decorators = [jwt_required(), bp.doc(hide=True)]

    @bp.input(ConnectSchema)
    async def post(self, group, json_data):
        """
        Create a new connection.

        Parameters:
            group (str): The name of the group.
            json_data (dict): The JSON data containing the connection information.

        Returns:
            dict: A dictionary containing the ID of the created connection.
        """
        async with async_session() as session:
            group_id = await session.execute(select(Group.id)).filter_by(group=group).scalar()
            connect = Connect(**json_data | {"group_id": group_id})
            await session.add(connect)
            await session.flush()
            item = connect.id
            await session.commit()
            return {'item_id': item}

    @bp.input(ConnectSchema)
    async def patch(self, item, json_data):
        """
        Patch an item in the Connect table.

        Args:
            item: The id of the item to be patched.
            json_data: The data to be updated.
        
        Returns:
            A dictionary containing the updated item id.
        """
        async with async_session() as session:
            resp = session.query(Connect).filter_by(id=item).first()
            for k, v in json_data.items():
                setattr(resp, k, v)
            await session.commit()
            return {'item_id': item}

    async def delete(self, item):
        """
        Deletes an item from the database.

        Parameters:
            item (int): The ID of the item to be deleted.

        Returns:
            str: An empty string indicating the deletion was successful.
        """
        async with async_session() as session:
            resp = session.query(Connect).filter_by(id=item).first()
            await session.delete(resp)
            await session.commit()
            return ''

contacts_view = ConnnectView.as_view('connect')
bp.add_url_rule('/connect/<group>', view_func=contacts_view, methods=['POST'])
bp.add_url_rule('/connect/<int:item>', view_func=contacts_view, methods=['PATCH', 'DELETE'])
