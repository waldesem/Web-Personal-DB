from functools import wraps
import bcrypt

from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user

from . import bp
from ..models.model import Person, db, User, Log, Status, Region
from ..models.schema import LogSchema, UserSchema
from ..models.classify import Role


def admin_required(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        admin = db.session.query(User).filter_by(username=get_jwt_identity()).one_or_none()
        if admin.has_role(Role.admin.value):
            return func(*args, **kwargs)
        else:
            abort(404)
    return wrapper


@bp.get('/admin')
@bp.doc(hide=True)
@jwt_required()
def get_admin():
    user = db.session.query(User).filter_by(username=current_user.username).one_or_none()
    return {"admin": user.has_role(Role.admin.value)}


@bp.get('/users')
@bp.doc(hide=True)
@admin_required
def get_users():
    query = db.session.query(User).order_by(User.id.desc()).all()
    user_schema = UserSchema()
    datas = user_schema.dump(query, many=True)
    return datas


@bp.get('/users/<int:user_id>')
@bp.output(UserSchema)
@bp.doc(hide=True)
@admin_required
def get_user(user_id):
    return db.session.query(User).get(user_id)


@bp.post('/users/<int:user_id>/post/<flag>/')
@bp.doc(hide=True)
@admin_required
def add_user_info(flag, user_id):
    response = request.get_json()
    user = db.session.query(User).filter_by(username=response['username']).one_or_none()

    if not user and flag == "create":
        new_user = User(fullname=response['fullname'],
                        username=response['username'],
                        region_id = response['region_id'],
                        email = response['email'],
                        password=bcrypt.hashpw(response['username'].encode('utf-8'), bcrypt.gensalt()),
                        role=response['role'])
        db.session.add(new_user)
        db.session.commit()
        return {'user': flag}

    elif flag == "edit":
        user = db.session.query(User).get(user_id)
        for k, v in response.items():
            setattr(user, k, v)
        db.session.commit()
        return {'user': flag}

    else:
        return {'user': 'none'}


@bp.get('/users/<int:user_id>/get/<flag>')
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


@bp.get('/logs')
@bp.output(LogSchema)
@bp.doc(hide=True)
@admin_required
def logs_list():
    return db.session.query(Log).filter_by(status=Status.new.value).limit(100).all()
    

@bp.get('/logs/<flag>')
@bp.output(LogSchema)
@bp.doc(hide=True)
@admin_required
def log_actions(flag):
    logs = db.session.query(Log).filter_by(status=Status.new.value).all()
    if flag == 'reply':
        for log in logs:
            setattr(log, 'status', Status.reply.value)
        db.session.commit()
    elif flag == 'delete':
        db.session.delete(logs)
        db.session.commit()
    logs = db.session.query(Log).filter_by(status=Status.new.value).limit(100).all()
    return logs
    
    
@bp.post('/region')
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


@bp.get('/region/<int:loc_id>/delete')
@bp.doc(hide=True)
@admin_required
def del_location(loc_id):
    location = db.session.query(Region).filter_by(id=loc_id).one_or_none()
    db.session.delete(location)
    db.session.commit()
    return {'location': location.region}
        
        
@bp.get('/person/<int:person_id>/delete')
@bp.doc(hide=True)
@admin_required
def del_person(person_id):
    person = db.session.query(Person).filter_by(id=person_id).one_or_none()
    db.session.delete(person)
    db.session.commit()
    return {'person': person.fullname}
    