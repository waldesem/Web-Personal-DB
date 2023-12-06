# from flask import current_app, request
# import bcrypt

# from flask_jwt_extended import current_user
# from flask.views import MethodView
# from sqlalchemy import select

# from . import bp
# from .login import roles_required
# from ..models.classes import Roles, Groups
# from ..models.model import  User, Role, Group, async_session
# from ..models.schema import UserSchema, Pagination, models_schemas


# class UsersView(MethodView):
    
#     decorators = [roles_required(Roles.admin.value), 
#                   bp.input(UserSchema),
#                   bp.doc(hide=True)]

#     async def post(self, json_data):
#         """
#         Endpoint to handle POST requests for creating new users.
#         """
#         async with async_session() as session:
#             users = await session.execute(
#                 select(User)
#                 .order_by(User.id.desc())
#                 .filter(User.fullname.ilike('%{}%'.format(json_data['fullname'])))
#                 )
#             return await UserSchema().dump(users.all(), many=True)


# class UserView(MethodView):

#     decorators = [roles_required(Roles.admin.value), bp.doc(hide=True)]

#     async def get(self, action, user_id):
#         """
#         Retrieves a user based on the specified action and user ID.
#         """
#         async with async_session() as session:
#             user = await session.get(User, user_id)
#             if action == 'view':
#                 return await UserSchema().dump(user)
#             else:
#                 if action == 'block':
#                     if user.username != current_user.username:
#                         user.blocked = not user.blocked
#                 elif action == 'drop':
#                     user.password = bcrypt.hashpw(
#                         current_app.config['DEFAULT_PASSWORD'].encode('utf-8'),
#                         bcrypt.gensalt()
#                     )
#                 await session.commit()
#                 return self.get('view', user_id)
        
#     @bp.input(UserSchema)
#     async def post(self, json_data):
#         """
#         Creates a new user based on the provided JSON data.
#         """
#         async with async_session() as session:
#             user = await session.select(
#                 select(User)
#                 .filter_by(username=json_data['username']))
#             if not user.exists():
#                 new_user = User(fullname=json_data['fullname'],
#                             username=json_data['username'],
#                             region_id=json_data['region_id'],
#                             email=json_data['email'],
#                             password=bcrypt.hashpw(current_app.config['DEFAULT_PASSWORD'].encode('utf-8'),
#                                                 bcrypt.gensalt()))
#                 session.add(new_user)
#                 await session.commit()
#                 return UsersView().post({'fullname': ''})

#     @bp.input(UserSchema)
#     async def patch(self, json_data):
#         """
#         Patch a user's information.
#         """
#         async with async_session() as session:
#             user = await session.get(User, json_data['id'])
#             await user.update(**json_data)
#             await session.commit()
#             return self.get('view', json_data['id'])
        

#     async def delete(self, user_id):
#         """
#         Delete a user by their ID.
#         """
#         async with async_session() as session:
#             if user.username != current_user.username and user.username != 'admin':
#                 user = await session.get(User, user_id)
#                 await session.delete(user)
#                 await session.commit()
#                 return UsersView().post({'fullname': ''})

# user_view = UserView.as_view('user')
# bp.add_url_rule('/user', view_func=user_view, methods=['PATCH', 'POST'])
# bp.add_url_rule('/user/<int:user_id>', view_func=user_view, methods=['DELETE'])
# bp.add_url_rule('/user/<action>/<int:user_id>', view_func=user_view, methods=['GET'])


# class GroupView(MethodView):

#     decorators = [roles_required(Roles.admin.value), bp.doc(hide=True)]

#     async def get(self, value, user_id):
#         """
#         Retrieves a user's group from the database and adds it to the user's 
#         list of groups if it does not already exist.
#         """
#         async with async_session() as session:
#             user = await session.get(User, user_id)
#             item = await session.scalar(
#                 select(Group)
#                 .filter_by(group=value))
#             group = user.has_group(value)
#             if not group:
#                 user.groups.append
#                 await session.commit()
#                 return UsersView().get('view', user_id)

#     async def delete(self, value, user_id):
#         """
#         Deletes a group from a user's list of groups.
#         """
#         async with async_session() as session:
#             user = await session.get(User, user_id)
#             item = await session.scalar(select(Group).filter_by(group=value)).first()
#             if not (user.username == current_user.username and value == Groups.admins.name):
#                 user.groups.remove(item)
#                 await session.commit()
#                 return UsersView().get('view', user_id)

# bp.add_url_rule('/group/<value>/<int:user_id>', view_func=GroupView.as_view('group'))


# class RoleView(MethodView):

#     decorators = [roles_required(Roles.admin.value), bp.doc(hide=True)]

#     async def get(self, value, user_id):
#         """
#         Get a user's role based on the value and user ID.
#         """
#         async with async_session() as session:
#             user = await session.get(User, user_id)
#             item = await session.scalar(
#                 select(Role)
#                 .filter_by(role=value))
#             role = user.has_role(value)
#             if not role:
#                 user.roles.append(item)
#                 await session.commit()
#                 return UsersView().get('view', user_id)
    
#     async def delete(self, value, user_id):
#         """
#         Deletes a role from a user.
#         """
#         async with async_session() as session:
#             user = await session.get(User, user_id)
#             item = await session.scalar(select(Role).filter_by(role=value)).first()
#             if not (user.username == current_user.username and value == Roles.admin.name):
#                 user.roles.remove(item)
#                 await session.commit()
#                 return UsersView().get('view', user_id)
            
# bp.add_url_rule('/role/<value>/<int:user_id>', view_func=RoleView.as_view('role'))


# class TableView(MethodView):
    
#     decorators = [roles_required(Roles.admin.value), bp.doc(hide=True)]

#     async def post(self, item, page):
#         model = models_schemas[item][0]
#         schema = models_schemas[item][1]
#         json_data = request.get_json()
#         async with async_session() as session:
#             query = session.execute(select(model))
#             if item in ['user', 'role', 'group', 'report', 'resume', 'connect']:
#                 query = query.filter_by(id=json_data['id'])
#             else:
#                 query = query.filter_by(person_id=json_data['id'])
#             pagination = Pagination(query, 16, page)
#             result = pagination.paginate()
#             return [schema.dump(result, many=True),
#                     {'has_next': bool(pagination.has_next()),
#                      'has_prev': bool(pagination.has_prev())}]

#     async def delete(self, item, item_id):
#         model = models_schemas[item][0]
#         async with async_session() as session:
#             row_query = await session.execute(
#                 select(model)
#                 .filter_by(id=item_id))
#             row = row_query.one_or_none()
#             if not item == 'user' and (row.username == current_user.username 
#                                     or row.username == 'admin'):
#                 session.delete(row)
#                 await session.commit()
#             return ''

# table_view = TableView.as_view('table')
# bp.add_url_rule('/table/<item>/<int:page>',
#                 view_func=table_view, methods=['GET', 'POST'])
# bp.add_url_rule('/table/<item>/<int:item_id>',
#                 view_func=table_view, methods=['DELETE', 'PATCH'])