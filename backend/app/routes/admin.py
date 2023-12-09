from flask import current_app, request
import bcrypt

from apiflask import EmptySchema
from flask_jwt_extended import get_jwt_identity
from flask.views import MethodView
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import bp
from .login import roles_required, group_required
from ..models.classes import Roles, Groups
from ..models.model import  User, Role, Group, engine
from ..models.schema import UserSchema, models_schemas
from ..models.paginate import Pagination


class UsersView(MethodView):
    
    @bp.input(UserSchema)
    @group_required(Groups.admins.name)
    async def post(self, json_data):
        """
        Endpoint to handle POST requests for searching users.
        """
        async with AsyncSession(engine) as session:
            async with session.begin():
                users = await session.execute(
                    select(User)
                    .order_by(User.id.desc())
                    .filter(User.fullname.ilike('%{}%'.format(json_data['fullname'])))
                    )
                await engine.dispose()
                return UserSchema().dump(users.scalars(), many=True)

bp.add_url_rule('/users', view_func=UsersView.as_view('users'))


class UserView(MethodView):

    @bp.output(UserSchema)
    @group_required(Groups.admins.name)
    async def get(self, action, user_id):
        """
        Retrieves a user based on the specified action and user ID.
        """
        async with AsyncSession(engine) as session:
            async with session.begin():
                user = await session.get(User, user_id)
                if action != 'view':
                    if action == 'block':
                        if user.username != get_jwt_identity():
                            user.blocked = not user.blocked
                    elif action == 'drop':
                        user.password = bcrypt.hashpw(
                            current_app.config['DEFAULT_PASSWORD'].encode('utf-8'),
                            bcrypt.gensalt()
                        )
                    user = await session.get(User, user_id)
                await engine.dispose()
                return user

    @bp.input(UserSchema)
    @bp.output(EmptySchema)             
    @roles_required(Roles.admin.name)
    async def post(self, json_data):
        """
        Creates a new user based on the provided JSON data.
        """
        async with AsyncSession(engine) as session:
            async with session.begin():
                user = await session.execute(
                    select(User)
                    .filter_by(username=json_data['username'])
                    )
                if not user.scalar_one_or_none():
                    new_user = User(
                        fullname=json_data['fullname'],
                        username=json_data['username'],
                        email=json_data['email'],
                        password=bcrypt.hashpw(current_app.config['DEFAULT_PASSWORD'].encode('utf-8'),
                                               bcrypt.gensalt())
                    )
                    session.add(new_user)
                await engine.dispose()
                return "", 204

    @bp.input(UserSchema)
    @bp.output(EmptySchema)
    @roles_required(Roles.admin.name)
    async def patch(self, json_data):
        """
        Patch a user's information.
        """
        async with AsyncSession(engine) as session:
            async with session.begin():
                user = await session.get(User, json_data['id'])
                for k, v in json_data.items():
                    setattr(user, k, v)
                await  engine.dispose()
                return "", 204

    @bp.output(EmptySchema)
    @roles_required(Roles.admin.name)
    async def delete(self, user_id):
        """
        Delete a user by their ID.
        """
        async with AsyncSession(engine) as session:
            async with session.begin():
                user = await session.get(User, user_id)
                if user.username not in [get_jwt_identity(), 'admin']:
                    await session.delete(user)
                await engine.dispose()
                return "", 204

user_view = UserView.as_view('user')
bp.add_url_rule('/user', view_func=user_view, methods=['PATCH', 'POST'])
bp.add_url_rule('/user/<int:user_id>', view_func=user_view, methods=['DELETE'])
bp.add_url_rule('/user/<action>/<int:user_id>', view_func=user_view, methods=['GET'])


class GroupView(MethodView):

    @bp.output(EmptySchema)
    @roles_required(Roles.admin.name)
    async def get(self, group, user_id):
        """
        Retrieves a user's group from the database and adds it to the user's 
        list of groups if it does not already exist.
        """
        async with AsyncSession(engine) as session:
            async with session.begin():
                user = await session.get(User, user_id)
                item = await session.scalar(
                    select(Group)
                    .filter_by(group=group))
                if not group not in [user.group for user in user.groups]:
                    user.groups.append(item)
                await engine.dispose()
                return "", 204

    @bp.output(EmptySchema)
    @roles_required(Roles.admin.name)
    async def delete(self, group, user_id):
        """
        Deletes a group from a user's list of groups.
        """
        async with AsyncSession(engine) as session:
            async with session.begin():
                user = await session.get(User, user_id)
                item = await session.scalar(
                    select(Group)
                    .filter_by(group=group)
                    )
                if not (user.username == get_jwt_identity() and group == Groups.admins.name):
                    user.groups.remove(item)
                await engine.dispose()
                return "", 204

bp.add_url_rule('/group/<group>/<int:user_id>', view_func=GroupView.as_view('group'))


class RoleView(MethodView):

    @bp.output(EmptySchema)
    @roles_required(Roles.admin.name)
    async def get(self, role, user_id):
        """
        Get a user's role based on the role and user ID.
        """
        async with AsyncSession(engine) as session:
            async with session.begin():
                user = await session.get(User, user_id)
                item = await session.scalar(
                    select(Role)
                    .filter_by(role=role))
                if role not in [user.role for user in user.roles]:
                    user.roles.append(item)
                await engine.dispose()
                return "", 204
    
    @bp.output(EmptySchema)
    @roles_required(Roles.admin.name)
    async def delete(self, role, user_id):
        """
        Deletes a role from a user.
        """
        async with AsyncSession(engine) as session:
            async with session.begin():
                user = await session.get(User, user_id)
                item = await session.scalar(
                    select(Role)
                    .filter_by(role=role)
                    )
                if not (user.username == get_jwt_identity() and role == Roles.admin.name):
                    user.roles.remove(item)
                await engine.dispose()
                return "", 204
            
bp.add_url_rule('/role/<role>/<int:user_id>', view_func=RoleView.as_view('role'))


class TableView(MethodView):
    
    @group_required(Groups.admins.name)
    async def get(self, item, page):
        model = models_schemas[item][0]
        schema = models_schemas[item][1]
        async with AsyncSession(engine) as session:
            async with session.begin():
                if item in ['user', 'role', 'group', 'report', 'resume', 'connect']:
                    query = await session.execute(
                        select(model)
                    )
                else:
                    query = await session.execute(
                        select(model)
                    )
                pagination = Pagination(query.scalars(), 16, page)
                result = pagination.paginate()
                await engine.dispose()
                return [
                    schema.dump(result, many=True),
                        {'has_next': pagination.has_next(),
                        'has_prev': pagination.has_prev()}
                    ]
            
    @group_required(Groups.admins.name)
    async def post(self, item, page):
        model = models_schemas[item][0]
        schema = models_schemas[item][1]
        json_data = request.get_json()
        async with AsyncSession(engine) as session:
            async with session.begin():
                if item in ['user', 'role', 'group', 'report', 'resume', 'connect']:
                    query = await session.execute(
                        select(model)
                        .filter_by(id=int(json_data['id']))
                    )
                else:
                    query = await session.execute(
                        select(model)
                        .filter_by(person_id=json_data['id'])
                    )
                pagination = Pagination(query, 16, page)
                result = pagination.paginate()
                await engine.dispose()
                return [
                    schema.dump(result, many=True),
                        {'has_next': pagination.has_next(),
                        'has_prev': pagination.has_prev()}
                    ]
            
    @bp.output(EmptySchema)
    @group_required(Groups.admins.name)
    async def delete(self, item, item_id, page):
        model = models_schemas[item][0]
        async with AsyncSession(engine) as session:
            async with session.begin():
                row = await session.get(model, item_id)
                if not item == 'user' \
                    and (row.username == get_jwt_identity() 
                         or row.username == 'admin'):
                    session.delete(row)
                await engine.dispose()
                return "", 204

table_view = TableView.as_view('table')
bp.add_url_rule('/table/<item>/<int:page>',
                view_func=table_view, methods=['GET', 'POST'])
bp.add_url_rule('/table/<item>/<int:item_id>',
                view_func=table_view, methods=['DELETE', 'PATCH'])