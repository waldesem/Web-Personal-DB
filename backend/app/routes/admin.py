from apiflask import EmptySchema
import bcrypt

from flask_jwt_extended import current_user
from flask.views import MethodView

from . import bp
from .. import db
from .login import r_g
from ..models.model import  User, Role, Group
from ..models.schema import  UserSchema
from ..models.classes import Roles


class UsersView(MethodView):

    decorators = [r_g.roles_required(Roles.admin.value), bp.doc(hide=True)]

    schema = UserSchema()

    def get(self):
        """
        Retrieves all users from the database and returns them in descending order by ID.

        :return: A list of User objects.
        """
        query = db.session.query(User).order_by(User.id.desc())
        return self.schema.dump(query, many=True)
    
    @bp.input(UserSchema)
    def post(self, json_data):
        """
        Endpoint to handle POST requests for creating new users.

        Parameters:
            json_data (dict): A dictionary containing the data for the new user.

        Returns:
            list: A list of User objects that match the search criteria.
        """
        query = db.session.query(User).order_by(User.id.desc()).\
            filter(User.fullname.ilike('%{}%'.format(json_data['fullname']))).all()
        return self.schema.dump(query, many=True)

bp.add_url_rule('/users', view_func=UsersView.as_view('users'))


class UserView(MethodView):

    decorators = [r_g.roles_required(Roles.admin.value), bp.doc(hide=True)]

    @bp.output(UserSchema)
    def get(self, action, user_id):
        """
        Retrieves a user based on the specified action and user ID.

        Parameters:
            action (str): The action to perform. Possible values are 'view', 'block', or 'drop'.
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The retrieved user object if the action is 'view'.
            User: The updated user object if the action is 'block' or 'drop'.
        """
        user = db.session.query(User).get(user_id)
        match action:
            case 'view':
                return user
            case 'block':
                if user.username != current_user.username:
                    user.blocked = not user.blocked
                    db.session.commit()
                return db.session.query(User).get(user_id)
            case 'drop':
                setattr(user, 'password', bcrypt.hashpw(user.username.encode('utf-8'), 
                                                        bcrypt.gensalt()))
                setattr(user, 'pswd_change', None)
                db.session.commit()
                return db.session.query(User).get(user_id)                

    @bp.input(UserSchema)
    def post(json_data):
        """
        Creates a new user based on the provided JSON data.

        Parameters:
            json_data (dict): A dictionary containing the user data in JSON format.

        Returns:
            tuple: A tuple containing a message and status code. The message indicates the result of the operation, and the status code represents the HTTP status code.

        Raises:
            None
        """
        if not db.session.query(User).\
            filter_by(username=json_data['username']).one_or_none():
            db.session.add(User(fullname=json_data['fullname'],
                                username=json_data['username'],
                                region_id = json_data['region_id'],
                                email = json_data['email'],
                                password=bcrypt.hashpw(json_data['username'].encode('utf-8'), 
                                                       bcrypt.gensalt())))
            db.session.commit()
            return {'message': 'Created'}, 201
    
    @bp.input(UserSchema)
    def patch(self, json_data):
        """
        Patch a user's information.

        Args:
            json_data (dict): A dictionary containing the updated information for the user.

        Returns:
            tuple: A tuple containing a message indicating the success of the patch operation and the HTTP status code.

        Raises:
            None
        """
        user = db.session.query(User).\
            filter_by(username=json_data['username']).one_or_none()
        if user:
            for k, v in json_data.items():
                setattr(user, k, v)
            db.session.commit()
            return {'message': 'Patched'}, 201
        
    @bp.output(EmptySchema, status_code=204)
    def delete(self, user_id):
        """
        Delete a user by their ID.

        Parameters:
            user_id (int): The ID of the user to delete.

        Returns:
            dict: A dictionary with a message indicating the user has been deleted.
                  The dictionary also includes the HTTP status code 204 indicating
                  a successful deletion.
        """
        user = db.session.query(User).get(user_id)
        if user.username != current_user.username:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'Deleted'}, 204
        
user_view = UserView.as_view('user')
bp.add_url_rule('/user', view_func=user_view, methods=['PATCH', 'POST'])
bp.add_url_rule('/user/<action>/<int:user_id>', view_func=user_view, methods=['GET', 'DELETE'])


class GroupView(MethodView):

    decorators = [r_g.roles_required(Roles.admin.value), bp.doc(hide=True)]
    
    def get(self, value, user_id):
        """
        Retrieves a user's group from the database and adds it to the user's list of groups if it does not already exist.

        Parameters:
            value (str): The group value to retrieve.
            user_id (int): The ID of the user.

        Returns:
            tuple: A tuple containing an empty string and the HTTP status code 201 if the group was added successfully.

        """
        user = db.session.query(User).get(user_id)
        item = db.session.query(Group).filter_by(group=value).first() 
        group = user.has_group(value)
        if not group:
            user.groups.append(item)
            db.session.commit()
            return '', 201
        
    @bp.output(EmptySchema, status_code=204)
    def delete(self, value, user_id):
        """
        Deletes a group from a user's list of groups.

        Parameters:
            value (str): The name of the group to be deleted.
            user_id (int): The id of the user.

        Returns:
            str: An empty string indicating success.
        """
        user = db.session.query(User).get(user_id)
        item = db.session.query(Group).filter_by(group=value).first() 
        if user.username != current_user.username and value != 'admin':
            user.groups.remove(item)
            db.session.commit()
            return '', 204
        
bp.add_url_rule('/group/<value>/<int:user_id>', view_func=GroupView.as_view('group'))


class RoleView(MethodView):

    decorators = [r_g.roles_required(Roles.admin.value), bp.doc(hide=True)]
    
    def get(self, value, user_id):
        """
        Get a user's role based on the value and user ID.
        
        Args:
            value (str): The role value to search for.
            user_id (int): The ID of the user.
            
        Returns:
            tuple: A tuple containing an empty string and the status code 201 if the role was successfully added to the user's roles. Otherwise, returns None.
        """
        user = db.session.query(User).get(user_id)
        item = db.session.query(Role).filter_by(role=value).first() 
        response = user.has_role(value)
        if not response:
            user.roles.append(item)
            db.session.commit()
            return '', 201
        
    @bp.output(EmptySchema, status_code=204)
    def delete(self, value, user_id):
        """
        Deletes a role from a user.

        Args:
            value (str): The role value to be deleted.
            user_id (int): The ID of the user.

        Returns:
            str: An empty string indicating success.
        """
        user = db.session.query(User).get(user_id)
        item = db.session.query(Role).filter_by(role=value).first()
        if user.username != current_user.username and value != 'admin':
            user.roles.remove(item)
            db.session.commit()
            return '', 204
        
bp.add_url_rule('/role/<value>/<int:user_id>', view_func=RoleView.as_view('role'))
