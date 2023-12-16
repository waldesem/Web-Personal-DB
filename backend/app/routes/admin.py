import bcrypt
from apiflask import EmptySchema
from flask import current_app, request
from flask_jwt_extended import current_user
from flask.views import MethodView
from sqlalchemy import select 

from . import bp
from .. import db
from .login import roles_required, group_required
from ..models.classes import Roles, Groups
from ..models.model import User, Role, Group
from ..models.schema import SearchSchema, UserSchema, models_schemas


class UsersView(MethodView):
    
    decorators = [group_required(Groups.admins.name),
                  bp.input(UserSchema),
                  bp.doc(hide=True)]

    def post(self, json_data):
        """
        Endpoint to handle POST requests for creating new users.
        """
        fullname = json_data['fullname']
        query = db.session.execute(
                 select(User)
                 .order_by(User.id.desc())
                 .filter(User.fullname.ilike('%{}%'.format(fullname)))
                 ).scalars().all()
        return UserSchema().dump(query, many=True)
    
bp.add_url_rule('/users', view_func=UsersView.as_view('users'))


class UserView(MethodView):
                  
    decorators = [bp.doc(hide=True)]

    @group_required(Groups.admins.name)
    def get(self, action, user_id):
        """
        Retrieves a user based on the specified action and user ID.
        """
        user = db.session.get(User, user_id)
        match action:
            case 'view':
                return UserSchema().dump(user)
            case 'block':
                if user.username != current_user.username:
                    user.blocked = not user.blocked
                    db.session.commit()
                return self.get('view', user_id)
            case 'drop':
                new_pswd = bcrypt.hashpw(current_app.config['DEFAULT_PASSWORD']. \
                                         encode('utf-8'), bcrypt.gensalt())
                setattr(user, 'password', new_pswd)
                setattr(user, 'pswd_change', None)
                db.session.commit()
                return self.get('view', user_id)
    
    @roles_required(Roles.admin.name)
    @bp.input(UserSchema)
    def post(self, json_data):
        """
        Creates a new user based on the provided JSON data.
        """
        if not User.get_user(json_data['username']):
            new_pswd = bcrypt.hashpw(current_app.config['DEFAULT_PASSWORD']. \
                                     encode('utf-8'), bcrypt.gensalt())
            db.session.add(User(
                fullname=json_data['fullname'],
                username=json_data['username'],
                email=json_data['email'],
                password=new_pswd)
            )
            db.session.commit()
            return UsersView().post({'fullname': ''})
        
    @roles_required(Roles.admin.value)
    @bp.input(UserSchema)
    def patch(self, json_data):
        """
        Patch a user's information.
        """
        user = db.session.get(User, json_data['id'])
        if user:
            for k, v in json_data.items():
                if k in ['fullname', 'username', 'email', 'region']:
                    setattr(user, k, v)
            db.session.commit()
            return self.get('view', json_data['id'])
    
    @roles_required(Roles.admin.value)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, user_id):
        """
        Delete a user by their ID.
        """
        user = db.session.get(User, user_id)
        if user.username != current_user.username and \
                user.username != 'superadmin':
            db.session.delete(user)
            db.session.commit()
            return UsersView().post({'fullname': ''})
        
user_view = UserView.as_view('user')
bp.add_url_rule('/user', view_func=user_view, methods=['PATCH', 'POST'])
bp.add_url_rule('/user/<int:user_id>', view_func=user_view, methods=['DELETE'])
bp.add_url_rule('/user/<action>/<int:user_id>', view_func=user_view, methods=['GET'])


class GroupView(MethodView):

    decorators = [bp.doc(hide=True), roles_required(Roles.admin.value)]

    def get(self, value, user_id):
        """
        Retrieves a user's group from the database and adds it to the user's 
        list of groups if it does not already exist.
        """
        user = db.session.get(User, user_id)
        if value not in user.groups:
            user.groups.append(db.session.get(Group, value))
            db.session.commit()
        return UserView().get('view', user_id)
        
    @bp.output(EmptySchema, status_code=204)
    def delete(self, value, user_id):
        """
        Deletes a group from a user's list of groups.
        """
        user = db.session.get(User, user_id)
        group = db.session.get(Group, value)
        if not (user.username == current_user.username):
            user.groups.remove(group)
            db.session.commit()
        return UserView().get('view', user_id)
        
bp.add_url_rule('/group/<value>/<int:user_id>', view_func=GroupView.as_view('group'))


class RoleView(MethodView):
    """
    Get a user's role based on the value and user ID.
    """
    decorators = [roles_required(Roles.admin.value), 
                  bp.doc(hide=True)]

    def get(self, value, user_id):
        user = db.session.get(User, user_id)
        if value not in user.roles:
            user.roles.append(db.session.get(Role, value))
            db.session.commit()
        return UserView().get('view', user_id)
        
    def delete(self, value, user_id):
        """
        Deletes a role from a user.
        """
        user = db.session.get(User, user_id)
        role = db.session.get(Role, value)
        if not (user.username == current_user.username):
            user.roles.remove(role)
            db.session.commit()
        return UserView().get('view', user_id)
        
bp.add_url_rule('/role/<value>/<int:user_id>', view_func=RoleView.as_view('role'))


class TableView(MethodView):
    
    decorators = [bp.doc(hide=True)]

    @bp.input(SearchSchema)
    @group_required(Groups.admins.name)
    def post(self, item, page, json_data):
        model = models_schemas[item][0]
        schema = models_schemas[item][1]
        query = select(model).order_by(model.id.desc())
        if item in ['user', 'role', 'group', 'report', 'resume', 'connect']:
            query = query.filter_by(id=json_data['search']) if json_data['search'] else query
        else:
            query = query.filter_by(person_id=json_data['search']) if json_data['search'] else query
        result = db.paginate(query, page=page, per_page=16, error_out=False)
        return [
            schema.dump(result, many=True), 
            {
                'has_next': result.has_next,
                'has_prev': result.has_prev
            }
        ]
    
    @roles_required(Roles.admin.name)
    def delete(self, item, item_id, page):
        model = models_schemas[item][0]
        row = db.session.get(model, item_id)
        if not item == 'user' and (row.username == current_user.username 
                                   or row.username == 'admin'):
            db.session.delete(row)
            db.session.commit()
        return self.post(item, page, {'search': ''})
    
table_view = TableView.as_view('table')
bp.add_url_rule('/table/<item>/<int:page>',
                view_func=table_view, methods=['GET', 'POST'])
bp.add_url_rule('/table/<item>/<int:item_id>',
                view_func=table_view, methods=['DELETE', 'PATCH'])