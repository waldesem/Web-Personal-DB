from apiflask import EmptySchema
from flask import current_app, request
import bcrypt

from flask_jwt_extended import current_user
from flask.views import MethodView

from . import bp
from .. import db
from .login import r_g
from ..models.classes import Roles, Groups
from ..models.model import User, Person, Staff, Document, Address, Contact, \
    Workplace, Check, Registry, Poligraf, Investigation, Inquiry, Relation, \
    Role, Group
from ..models.schema import RelationSchema, StaffSchema, AddressSchema, \
    PersonSchema, ContactSchema, DocumentSchema, CheckSchema, InquirySchema, \
    InvestigationSchema, PoligrafSchema, RegistrySchema, \
    WorkplaceSchema, UserSchema


class UsersView(MethodView):
    
    decorators = [r_g.roles_required(Roles.admin.value), 
                  bp.input(UserSchema),
                  bp.doc(hide=True)]

    def post(self, json_data):
        """
        Endpoint to handle POST requests for creating new users.

        Parameters:
            json_data (dict): A dictionary containing the data for the new user.

        Returns:
            list: A list of User objects that match the search criteria.
        """
        schema = UserSchema()
        query = db.session.query(User).order_by(User.id.desc()). \
            filter(User.fullname.ilike('%{}%'.format(json_data['fullname']))).all()
        return schema.dump(query, many=True)


bp.add_url_rule('/users', view_func=UsersView.as_view('users'))


class UserView(MethodView):
    decorators = [r_g.roles_required(Roles.admin.value), bp.doc(hide=True)]

    @bp.output(UserSchema)
    def get(self, action, user_id):
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
                setattr(user, 'password',
                        bcrypt.hashpw(current_app.config['DEFAULT_PASSWORD']. \
                                      encode('utf-8'),
                                      bcrypt.gensalt()))
                setattr(user, 'pswd_change', None)
                db.session.commit()
                return db.session.query(User).get(user_id)

    @bp.input(UserSchema)
    def post(self, json_data):
        """
        Creates a new user based on the provided JSON data.

        Parameters:
            json_data (dict): A dictionary containing the user data in JSON format.

        Returns:
            tuple: A tuple containing a message and status code. The message 
            indicates the result of the operation, and the status code represents 
            the HTTP status code.

        Raises:
            None
        """
        if not db.session.query(User). \
                filter_by(username=json_data['username']).one_or_none():
            db.session.add(User(fullname=json_data['fullname'],
                                username=json_data['username'],
                                region_id=json_data['region_id'],
                                email=json_data['email'],
                                password=bcrypt.hashpw(current_app. \
                                                       config['DEFAULT_PASSWORD']. \
                                                       encode('utf-8'),
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
            tuple: A tuple containing a message indicating the success of the 
            patch operation and the HTTP status code.

        Raises:
            None
        """
        user = db.session.query(User). \
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
bp.add_url_rule('/user/<int:user_id>', view_func=user_view, methods=['DELETE'])
bp.add_url_rule('/user/<action>/<int:user_id>', view_func=user_view, methods=['GET'])


class GroupView(MethodView):
    decorators = [r_g.roles_required(Roles.admin.value), bp.doc(hide=True)]

    def get(self, value, user_id):
        """
        Retrieves a user's group from the database and adds it to the user's 
        list of groups if it does not already exist.

        Parameters:
            value (str): The group value to retrieve.
            user_id (int): The ID of the user.

        Returns:
            tuple: A tuple containing an empty string and the HTTP status code 
            201 if the group was added successfully.

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
        if not (user.username == current_user.username and value == Groups.admins.name):
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
            tuple: A tuple containing an empty string and the status code 201 
            if the role was successfully added to the user's roles. Otherwise, returns None.
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
        if not (user.username == current_user.username and value == Roles.admin.name):
            user.roles.remove(item)
            db.session.commit()
            return '', 204


bp.add_url_rule('/role/<value>/<int:user_id>', view_func=RoleView.as_view('role'))


class TableView(MethodView):
    decorators = [r_g.roles_required(Roles.admin.value), bp.doc(hide=True)]
    pagination = 16
    mapped_item = {
        'user': [User, UserSchema()],
        'resume': [Person, PersonSchema()],
        'staff': [Staff, StaffSchema()],
        'document': [Document, DocumentSchema()],
        'address': [Address, AddressSchema()],
        'contact': [Contact, ContactSchema()],
        'workplace': [Workplace, WorkplaceSchema()],
        'relation': [Relation, RelationSchema()],
        'check': [Check, CheckSchema()],
        'registry': [Registry, RegistrySchema()],
        'poligraf': [Poligraf, PoligrafSchema()],
        'investigation': [Investigation, InvestigationSchema()],
        'inquiry': [Inquiry, InquirySchema()]
    }

    def get(self, item, page):
        model = self.mapped_item[item][0]
        schema = self.mapped_item[item][1]
        query = db.session.query(model). \
            order_by(model.id.desc()).paginate(page=page,
                                               per_page=self.pagination,
                                               error_out=False)
        return [schema.dump(query, many=True),
                {'has_next': int(query.has_next)},
                {'has_prev': int(query.has_prev)}]

    def post(self, item, page):
        model = self.mapped_item[item][0]
        schema = self.mapped_item[item][1]
        json_data = request.get_json()
        query = db.session.query(model). \
            filter_by(id=int(json_data['id'])). \
            order_by(model.id.desc()).paginate(page=page,
                                               per_page=self.pagination,
                                               error_out=False)
        return [schema.dump(query, many=True),
                {'has_next': int(query.has_next)},
                {'has_prev': int(query.has_prev)}]

    def patch(self, item, item_id):
        model = self.mapped_item[item][0]
        schema = self.mapped_item[item][1]
        json_data = schema.load(request.get_json())
        data = db.session.query(model). \
            filter_by(id=item_id).one_or_none()
        if data:
            for k, v in json_data.items():
                setattr(data, k, v)
            db.session.commit()
            return {'message': 'Patched'}, 201

    def delete(self, item, item_id):
        model = self.mapped_item[item][0]
        table = db.session.query(model).filter_by(id=item_id).one_or_none()
        if table:
            db.session.delete(table)
            db.session.commit()
        return ''


table_view = TableView.as_view('table')
bp.add_url_rule('/table/<item>/<int:page>',
                view_func=table_view, methods=['GET', 'POST'])
bp.add_url_rule('/table/<item>/<int:item_id>',
                view_func=table_view, methods=['DELETE', 'PATCH'])
