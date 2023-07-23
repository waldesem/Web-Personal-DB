from functools import wraps
import bcrypt

from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user

from . import bp
from ..models.model import db, User, Log, Status
from ..models.schema import LogSchema, UserSchema
from ..models.classify import Roles


def admin_required(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        admin = db.session.query(User).filter_by(username=get_jwt_identity()).one_or_none()
        if admin.has_role(Roles.admin.value):
            return func(*args, **kwargs)
        else:
            abort(403)
    return wrapper


@bp.get('/admin/index')
@bp.doc(hide=True)
@admin_required
def get_Users():
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


@bp.get('/admin/log/<flag>')
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


@bp.post('/user/actions/<action>/<int:user_id>')
@bp.doc(hide=True)
@admin_required
def add_user_info(action, user_id):
    response = request.get_json()
    user = db.session.query(User).filter_by(username=response['username']).one_or_none()
    if not user and action == "create":
        new_user = User(fullname=response['fullname'],
                        username=response['username'],
                        location = response['location'],
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


@bp.get('/user/actions/<action>/<int:user_id>')
@bp.doc(hide=True)
@admin_required
def edit_user_info(action, user_id):
    user = db.session.query(User).get(user_id)
    if user.username != current_user.username:
        if action == 'block':
            setattr(user, 'blocked', False) if user.blocked else setattr(user, 'blocked', True)
            db.session.commit()
            return {'user': str(user.blocked)}
        else:
            db.session.delete(user)
            db.session.commit()
            return {'user': action}
    return {'user': 'None'}
    
