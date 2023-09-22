from apiflask import EmptySchema
import bcrypt

from flask_jwt_extended import current_user
from flask.views import MethodView

from . import bp
from .. import db
from .login import r_g
from ..models.model import  User, Role, Group
from ..models.schema import  UserSchema, UsersSchema
from ..models.classes import Roles


class UsersView(MethodView):

    decorators = [r_g.roles_required(Roles.admin.value), bp.doc(hide=True)]

    @bp.output(UsersSchema)
    def get(self):
        return db.session.query(User).order_by(User.id.desc()).all()
    
    @bp.input(UserSchema)
    @bp.output(UsersSchema)
    def post(self, json_data):
        return db.session.query(User).order_by(User.id.desc()).\
            filter(User.fullname.ilike('%{}%'.format(json_data['fullname']))).all()

bp.add_url_rule('/users', view_func=UsersView.as_view('users'))


class UserView(MethodView):

    decorators = [r_g.roles_required(Roles.admin.value), bp.doc(hide=True)]

    @bp.output(UserSchema)
    def get(self, action, user_id):
        user = db.session.query(User).get(user_id)
        match action:
            case 'view':
                return user
            case 'block':
                if user.username != current_user.username:
                    user.blocked = not user.blocked
                    db.session.commit()
                return user
            case 'drop':
                setattr(user, 'password', bcrypt.hashpw(user.username.encode('utf-8'), 
                                                        bcrypt.gensalt()))
                setattr(user, 'pswd_change', None)
                db.session.commit()
                return user                

    @bp.input(UserSchema)
    def post(json_data):
        if not db.session.query(User).\
            filter_by(username=json_data['username']).one_or_none():
            db.session.add(User(fullname=json_data['fullname'],
                                username=json_data['username'],
                                region_id = json_data['region_id'],
                                email = json_data['email'],
                                password=bcrypt.hashpw(json_data['username'].encode('utf-8'), 
                                                       bcrypt.gensalt())))
            db.session.commit()
            return ''
    
    @bp.input(UserSchema)
    def patch(self, json_data):
        user = db.session.query(User).\
            filter_by(username=json_data['username']).one_or_none()
        if user:
            for k, v in json_data.items():
                setattr(user, k, v)
            db.session.commit()
            return '', 201
        
    @bp.output(EmptySchema, status_code=204)
    def delete(self, user_id):
        user = db.session.query(User).get(user_id)
        if user.username != current_user.username:
            db.session.delete(user)
            db.session.commit()
            return ''
        
user_view = UserView.as_view('user')
bp.add_url_rule('/user', view_func=user_view, methods=['PATCH', 'POST'])
bp.add_url_rule('/user/<int:user_id>', view_func=user_view, methods=['DELETE'])
bp.add_url_rule('/user/<flag>/<int:user_id>', view_func=user_view, methods=['GET'])


class GroupView(MethodView):

    decorators = [r_g.roles_required(Roles.admin.value), bp.doc(hide=True)]
    
    def post(self, value, user_id):
        user = db.session.query(User).get(user_id)
        item = db.session.query(Group).filter_by(group=value).first() 
        group = user.has_group(value)
        if not group:
            user.groups.append(item)
            db.session.commit()
            return '', 201
        
    @bp.output(EmptySchema, status_code=204)
    def delete(self, value, user_id):
        user = db.session.query(User).get(user_id)
        item = db.session.query(Group).filter_by(group=value).first() 
        if user.username != current_user.username and value != 'admin':
            user.groups.remove(item)
            db.session.commit()
            return ''
        
bp.add_url_rule('/group/<value>/<int:user_id>', view_func=GroupView.as_view('group'))


class RoleView(MethodView):

    decorators = [r_g.roles_required(Roles.admin.value), bp.doc(hide=True)]
    
    def get(self, value, user_id):
        user = db.session.query(User).get(user_id)
        item = db.session.query(Role).filter_by(role=value).first() 
        response = user.has_role(value)
        if not response:
            user.roles.append(item)
            db.session.commit()
            return '', 201
        
    @bp.output(EmptySchema, status_code=204)
    def delete(self, value, user_id):
        user = db.session.query(User).get(user_id)
        item = db.session.query(Role).filter_by(role=value).first()
        if user.username != current_user.username and value != 'admin':
            user.roles.remove(item)
            db.session.commit()
            return ''
        
bp.add_url_rule('/role/<value>/<int:user_id>', view_func=RoleView.as_view('role'))
