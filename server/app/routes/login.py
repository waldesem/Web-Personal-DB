from datetime import datetime

import bcrypt
from flask import jsonify
from flask_jwt_extended import JWTManager, current_user, \
    create_access_token, jwt_required, unset_jwt_cookies

from . import bp
from ..models.model import User, db
from ..models.schema import LoginSchema

jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()


@bp.get('/auth')
@bp.doc(hide=True)
@jwt_required()
def auth():
    user = db.session.query(User).filter_by(username=current_user.username).one_or_none()
    if user and not user.blocked:
        user.last_login = datetime.now()
        db.session.commit()
        return {"user": user.username}
    return {"user": user}


@bp.post('/login')
@bp.input(LoginSchema)
@bp.doc(hide=True)
def login(response):
    user = db.session.query(User).filter_by(username=response['username']).one_or_none()
    if user and not user.blocked:
        if bcrypt.checkpw(response['password'].encode('utf-8'), user.password):
            delta_change = datetime.now() - user.pswd_create
            if user.pswd_change and delta_change.days < 365:
                access_token = create_access_token(identity=response['username'])
                user.last_login = datetime.now()
                db.session.commit()
                return {'access': 'Authorized', 'access_token': access_token}
            return {"access": "Overdue", 'access_token': None}
    return {"access": "None", 'access_token': None}


@bp.get('/logout')
@bp.doc(hide=True)
def logout():
    unset_jwt_cookies(jsonify({"user": "None"}))
    return {'access': 'Default'}


@bp.post('/password')
@bp.input(LoginSchema)
@bp.doc(hide=True)
def change_password(response):
    user = db.session.query(User).filter_by(username=response['username']).one_or_none()
    if user:
        if bcrypt.checkpw(response['password'].encode('utf-8'), user.password):
            setattr(user, 'password', bcrypt.hashpw(response['new_pswd'].encode('utf-8'), bcrypt.gensalt()))
            setattr(user, "pswd_change", datetime.now())
            db.session.commit()
            return {"access": "Success", 'access_token': None}
    return {"access": "None", 'access_token': None}
