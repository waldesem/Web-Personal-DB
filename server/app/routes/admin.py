from functools import wraps
import bcrypt

from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user

from . import bp
from app.models.model import db, User, Log, Status
from app.models.schema import LogSchema, UserSchema


def admin_required(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        admin = db.session.query(User).filter_by(username=get_jwt_identity()).one_or_none()
        print(admin.has_role)
        if admin.has_role('admin'):
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


@bp.get('/admin/log/<flag>')
@bp.output(LogSchema)
@bp.doc(hide=True)
@admin_required
def log_actions(flag):
    logs = db.session.query(Log).filter_by(status=Status.new.value).all()
    if flag == 'read':
        for log in logs:
            setattr(log, 'status', Status.reply.value)
        db.session.commit()
        logs = db.session.query(Log).filter_by(status=Status.new.value).all()
    return logs


@bp.post('/user/registration')
@bp.output(UserSchema)
@bp.doc(hide=True)
@admin_required
def registration():
    response = request.get_json()
    user = db.session.query(User).filter_by(username=response['username']).one_or_none()
    if not user:
        new_user = User(fullname=response['fullname'],
                        username=response['username'],
                        password=bcrypt.hashpw(response['username'].encode('utf-8'), bcrypt.gensalt()),
                        role=response['role'])
        db.session.add(new_user)
        db.session.commit()
    return {'user': bool(user)}


@bp.get('/user/<int:user_id>')
@bp.output(UserSchema)
@bp.doc(hide=True)
@admin_required
def get_user(user_id):
    return db.session.query(User).filter_by(id=user_id).one_or_none()


@bp.get('/user/block/<int:user_id>')
@bp.doc(hide=True)
@admin_required
def block_user(user_id):
    user = db.session.query(User).filter_by(id=user_id).one_or_none()
    if user.username != current_user.username:
        setattr(user, 'blocked', False) if user.blocked else setattr(user, 'blocked', True)
        db.session.commit()
        return {'blocked': user.blocked}
    return ''


@bp.get('/status')
@bp.doc(hide=True)
def get_status():
    return {i.name: i.value for i in Status}