from datetime import datetime
from functools import wraps

import bcrypt
from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

from . import bp
from app.models.model import db, User, Log, LogSchema, UserSchema, Status


def admin_required(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if 'admin' in db.session.query(User.role).filter_by(username=current_user).first():
            return func(*args, **kwargs)
        else:
            abort(403)  # Return a 403 Forbidden error if the user does not have the admin role
    return wrapper


@bp.get('/admin/index')
@bp.doc(hide=True)
@admin_required
def get_Users():
    query = db.session.query(User).order_by(User.id.desc()).all()
    user_schema = UserSchema()
    datas = user_schema.dump(query, many=True)
    return datas


@bp.post('/user/registration')
@bp.doc(hide=True)
@admin_required
def registration():
    # Get user data from the form
    user_form = request.get_json()
    fullname = user_form.get('fullname')
    username = user_form.get('username')
    role = user_form.get('role')
    # Query the database for a user with the provided credentials
    user = db.session.query(User).filter_by(username=username).first()
    if user:
        return {'attr': 'alert-danger', 'text': 'Пользователь уже существует'}
    else:
        new_user = User(
            fullname=fullname,
            username=username,
            pswd_create=datetime.now(),
            password=bcrypt.hashpw(f'{username}'.encode('utf-8'), bcrypt.gensalt()),
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        return {'attr': 'alert-success', 'text': f'Пользователь {username} успешно создан'}


@bp.get('/user/<int:user_id>')
@bp.doc(hide=True)
@bp.output(UserSchema)
@admin_required
def get_user(user_id):
    user = db.session.query(User).filter_by(id=user_id).one_or_none()
    return user


@bp.get('/user/block/<int:user_id>')
@bp.doc(hide=True)
@admin_required
def block_user(user_id):
    """
    Returns the full profile of a candidate/employee based on the candidate ID
    """
    user = db.session.query(User).filter_by(id=user_id).one_or_none()
    setattr(user, 'blocked', False) if user.blocked else setattr(user, 'blocked', True)
    db.session.commit()
    result = 'разблокирован' if user.blocked else 'заблокирован'
    
    return {'attr': 'alert-success', 
            'text': f'Пользователь {user.username} {result}', 
            'blocked': not user.blocked}


@bp.get('/admin/log/<flag>')
@bp.doc(hide=True)
@admin_required
def log_actions(flag):
    logs = db.session.query(Log).filter_by(status=Status.NEWFAG.value).all()
    if flag == 'unread':
        log_schema = LogSchema()
        log = log_schema(logs, many=True) if logs else []
        return {'counts': len(logs) if logs is not None else 0,
                'messages': log}
    else:
        for resp in logs:
            setattr(resp, 'status', Status.REPLY.value)
            db.session.commit()
        # Return the response with counts and an empty list of messages
        return {'counts': 0, 'messages': []}