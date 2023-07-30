from functools import wraps
import bcrypt

from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user

from . import bp
from ..models.model import db, User, Log, Status, Region
from ..models.schema import LogSchema, UserSchema, LocationSchema
from ..models.classify import Category, Conclusions, Decisions, Role


def admin_required(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        """
        A decorator function that wraps another function and requires JWT authentication.
        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            The result of the wrapped function if the authenticated user has the 'admin' role.
            Otherwise, raises a 404 error.
        Raises:
            None.
        """
        admin = db.session.query(User).filter_by(username=get_jwt_identity()).one_or_none()
        if admin.has_role(Role.admin.value):
            return func(*args, **kwargs)
        else:
            abort(404)
    return wrapper


@bp.get('/admin/admin')
@bp.doc(hide=True)
@jwt_required()
def get_admin():
    user = db.session.query(User).filter_by(username=current_user.username).one_or_none()
    return {"admin": user.has_role(Role.admin.value)}


@bp.get('/admin/index')
@bp.doc(hide=True)
@admin_required
def get_users():
    query = db.session.query(User).order_by(User.id.desc()).all()
    user_schema = UserSchema()
    datas = user_schema.dump(query, many=True)
    return datas


@bp.get('/user/profile/<int:user_id>')
@bp.output(UserSchema)
@bp.doc(hide=True)
@admin_required
def get_user(user_id):
    return db.session.query(User).get(user_id)


@bp.get('/logs/<flag>')
@bp.output(LogSchema)
@bp.doc(hide=True)
@admin_required
def log_actions(flag):
    logs = db.session.query(Log).filter_by(status=Status.new.value).limit(100).all()
    if flag == 'reply':
        for log in logs:
            setattr(log, 'status', Status.reply.value)
        db.session.commit()
        logs = db.session.query(Log).filter_by(status=Status.new.value).limit(100).all()
    elif flag == 'delete':
        db.session.delete(logs)
        db.session.commit()
        logs = db.session.query(Log).filter_by(status=Status.new.value).limit(100).all()
    return logs


@bp.get('/region/list')
@bp.doc(hide=True)
def get_locations():
    query = db.session.query(Region.id, Region.region).all()
    region_schema = LocationSchema()
    datas = region_schema.dump(query, many=True)
    return datas
    
    
@bp.post('/region/add')
@bp.doc(hide=True)
@admin_required
def add_location():
    response = request.get_json()
    location = db.session.query(Region).filter_by(region=response['region']).one_or_none()
    if not location:
        new_location = Region(region=response['region'])
        db.session.add(new_location)
        db.session.commit()
    return {'location': bool(location)}


@bp.get('/region/delete/<int:loc_id>')
@bp.doc(hide=True)
@admin_required
def del_location(loc_id):
    location = db.session.query(Region).filter_by(id=loc_id).one_or_none()
    db.session.delete(location)
    db.session.commit()
    return {'location': location.region}
        
        
@bp.post('/user/update/<action>/<int:user_id>')
@bp.doc(hide=True)
@admin_required
def add_user_info(action, user_id):
    response = request.get_json()
    user = db.session.query(User).filter_by(username=response['username']).one_or_none()

    if not user and action == "create":
        new_user = User(fullname=response['fullname'],
                        username=response['username'],
                        region_id = response['region_id'],
                        password=bcrypt.hashpw(response['username'].encode('utf-8'), bcrypt.gensalt()),
                        role=response['role'])
        db.session.add(new_user)
        db.session.commit()
        return {'user': action}

    elif action == "edit":
        user = db.session.query(User).get(user_id)
        for k, v in response.items():
            setattr(user, k, v)
        db.session.commit()
        return {'user': action}

    else:
        return {'user': 'none'}


@bp.get('/user/action/<flag>/<int:user_id>')
@bp.doc(hide=True)
@admin_required
def edit_user_info(flag, user_id):
    user = db.session.query(User).get(user_id)
    if user.username != current_user.username:
        if flag == 'block':
            setattr(user, 'blocked', False) if user.blocked else setattr(user, 'blocked', True)
            db.session.commit()
            return {'user': str(user.blocked)}
        if flag == 'drop':
            setattr(user, 'password', bcrypt.hashpw(user.username.encode('utf-8'), bcrypt.gensalt()))
            setattr(user, 'pswd_change', None)
            db.session.commit()
            return {'user': flag}
        else:
            db.session.delete(user)
            db.session.commit()
            return {'user': flag}
    return {'user': 'None'}
    
    
@bp.get('/classify')
@bp.doc(hide=True)
def get_classify():
    return [{i.name: i.value for i in Status}, 
            {i.name: i.value for i in Role}, 
            {i.name: i.value for i in Conclusions}, 
            {i.name: i.value for i in Decisions}, 
            {i.name: i.value for i in Category}]
