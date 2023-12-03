from flask import current_app, request
import bcrypt

from flask_jwt_extended import current_user
from flask.views import MethodView
from sqlalchemy import select

from . import bp
from .login import roles_required
from ..models.classes import Roles, Groups
from ..models.model import  User, Role, Group, async_session
from ..models.schema import UserSchema, models_schemas


class UsersView(MethodView):
    
    decorators = [roles_required(Roles.admin.value), 
                  bp.input(UserSchema),
                  bp.doc(hide=True)]

    async def post(self, json_data):
        """
        Endpoint to handle POST requests for creating new users.
        Parameters:
            json_data (dict): A dictionary containing the data for the new user.
        Returns:
            list: A list of User objects that match the search criteria.
        """
        async with async_session() as session:
            query = await session.execute(select(User)).order_by(User.id.desc()). \
                filter(User.fullname.ilike('%{}%'.format(json_data['fullname']))).all()
            return await UserSchema().dump(query, many=True)


class UserView(MethodView):

    decorators = [roles_required(Roles.admin.value), bp.doc(hide=True)]

    async def get(self, action, user_id):
        """
        Retrieves a user based on the specified action and user ID.

        Parameters:
            action (str): The action to perform. Possible values are 'view', 
            'block', or 'drop'.
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The retrieved user object if the action is 'view'.
            User: The updated user object if the action is 'block' or 'drop'.
        """
        async with async_session() as session:
            user = await session.get(User, user_id)
            match action:
                case 'view':
                    return await UserSchema().dump(user)
                case 'block':
                    if user.username != current_user.username:
                        user.blocked = not user.blocked
                        await session.commit()
                    return self.get('view', user_id)
                case 'drop':
                    user.password = bcrypt.hashpw(
                        current_app.config['DEFAULT_PASSWORD'].encode('utf-8'),
                        bcrypt.gensalt()
                    )
                    await session.commit()
                    return self.get('view', user_id)
        
    @bp.input(UserSchema)
    async def post(self, json_data):
        """
        Creates a new user based on the provided JSON data.
        Parameters:
            json_data (dict): A dictionary containing the user data in JSON format.
        """
        async with async_session() as session:
            user_exists = await session.scalar(select(User)
                                               .filter_by(username=json_data['username'])
                                               .exists())
            if not user_exists:
                user = User(fullname=json_data['fullname'],
                            username=json_data['username'],
                            region_id=json_data['region_id'],
                            email=json_data['email'],
                            password=bcrypt.hashpw(current_app.config['DEFAULT_PASSWORD'].encode('utf-8'),
                                                bcrypt.gensalt()))
                session.add(user)
                await session.commit()
                return UsersView().post({'fullname': ''})

    @bp.input(UserSchema)
    async def patch(self, json_data):
        """
        Patch a user's information.
        """
        async with async_session() as session:
            user = await session.get(User, json_data['id'])
            for k, v in json_data.items():
                if k in ['fullname', 'username', 'email', 'region']:
                    setattr(user, k, v)
            await session.commit()
            return self.get('view', json_data['id'])
        

    async def delete(self, user_id):
        """
        Delete a user by their ID.
        Parameters:
            user_id (int): The ID of the user to delete.
        """
        async with async_session() as session:
            if user.username != current_user.username and user.username != 'admin':
                user = await session.get(User, user_id)
                session.delete(user)
                await session.commit()
                return UsersView().post({'fullname': ''})

user_view = UserView.as_view('user')
bp.add_url_rule('/user', view_func=user_view, methods=['PATCH', 'POST'])
bp.add_url_rule('/user/<int:user_id>', view_func=user_view, methods=['DELETE'])
bp.add_url_rule('/user/<action>/<int:user_id>', view_func=user_view, methods=['GET'])


class GroupView(MethodView):

    decorators = [roles_required(Roles.admin.value), bp.doc(hide=True)]

    async def get(self, value, user_id):
        """
        Retrieves a user's group from the database and adds it to the user's 
        list of groups if it does not already exist.
        """
        async with async_session() as session:
            user = await session.get(User, user_id)
            item = await session.scalar(select(Group).filter_by(group=value))
            group = user.has_group(value)
            if not group:
                user.groups.append(item)
                await session.commit()
                return UsersView().get('view', user_id)

    async def delete(self, value, user_id):
        """
        Deletes a group from a user's list of groups.
        """
        async with async_session() as session:
            user = await session.get(User, user_id)
            item = await session.scalar(select(Group).filter_by(group=value)).first()
            if not (user.username == current_user.username and value == Groups.admins.name):
                user.groups.remove(item)
                await session.commit()
                return UsersView().get('view', user_id)

bp.add_url_rule('/group/<value>/<int:user_id>', view_func=GroupView.as_view('group'))


class RoleView(MethodView):

    decorators = [roles_required(Roles.admin.value), bp.doc(hide=True)]

    async def get(self, value, user_id):
        """
        Get a user's role based on the value and user ID.
        """
        async with async_session() as session:
            user = await session.get(User, user_id)
            item = await session.scalar(select(Role).filter_by(role=value))
            role = user.has_role(value)
            if not role:
                user.roles.append(item)
                await session.commit()
                return UsersView().get('view', user_id)
    
    async def delete(self, value, user_id):
        """
        Deletes a role from a user.
        """
        async with async_session() as session:
            user = await session.get(User, user_id)
            item = await session.scalar(select(Role).filter_by(role=value)).first()
            if not (user.username == current_user.username and value == Roles.admin.name):
                user.roles.remove(item)
                await session.commit()
                return UsersView().get('view', user_id)
            
bp.add_url_rule('/role/<value>/<int:user_id>', view_func=RoleView.as_view('role'))


class TableView(MethodView):
    
    decorators = [roles_required(Roles.admin.value), bp.doc(hide=True)]

    async def post(self, item, page):
        pagination = 16
        model = models_schemas[item][0]
        schema = models_schemas[item][1]
        json_data = request.get_json()
        async with async_session() as session:
            query = session.execute(select(model))
            if item in ['user', 'role', 'group', 'report', 'resume', 'connect']:
                query = query.filter_by(id=json_data['id'])
            else:
                query = query.filter_by(person_id=json_data['id'])
            result = query.paginate(page=page,per_page=pagination, error_out=False)
            return [schema.dump(result, many=True),
                    {'has_next': bool(result.has_next),
                     'has_prev': bool(result.has_prev)}]

    async def delete(self, item, item_id):
        model = models_schemas[item][0]
        async with async_session() as session:
            row = await session.execute(select(model)).filter_by(id=item_id).one_or_none()
            if not item == 'user' and (row.username == current_user.username 
                                    or row.username == 'admin'):
                session.delete(row)
                await session.commit()
            return ''

table_view = TableView.as_view('table')
bp.add_url_rule('/table/<item>/<int:page>',
                view_func=table_view, methods=['GET', 'POST'])
bp.add_url_rule('/table/<item>/<int:item_id>',
                view_func=table_view, methods=['DELETE', 'PATCH'])
