from datetime import datetime
from functools import wraps

import bcrypt
import redis
from flask import current_app, abort
from flask.views import MethodView
from flask_jwt_extended import current_user, \
    create_access_token, create_refresh_token, get_jwt, jwt_required, get_jwt_identity

from . import bp
from .. import jwt, db
from ..models.model import  User
from ..models.schema import LoginSchema, UserSchema
from ..models.classes import Roles

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


class RoleGroupRequire:

    def roles_required(self, *roles):
        def decorator(func):
            @wraps(func)
            @jwt_required()
            def wrapper(*args, **kwargs):
                user = db.session.query(User).\
                    filter_by(username=get_jwt_identity()).one_or_none()
                if user is not None and any(user.has_role(role) 
                                                 for role in roles):
                    return func(*args, **kwargs)
                else:
                    abort(404)
            return wrapper
        return decorator

    def group_required(self, *groups):
        def decorator(func):
            @wraps(func)
            @jwt_required()
            def wrapper(*args, **kwargs):
                user = db.session.query(User).\
                    filter_by(username=get_jwt_identity()).one_or_none()
                if user is not None and any(user.has_group(group) 
                                                 for group in groups):
                    return func(*args, **kwargs)
                else:
                    abort(404)
            return wrapper
        return decorator

r_g = RoleGroupRequire()


class LoginView(MethodView):

    decorators = [bp.doc(hide=True)]
        
    @jwt_required()
    @bp.output(UserSchema)
    def get(self): 
        user = db.session.query(User).\
            filter_by(username=current_user.username).one_or_none()
        if user and not user.has_blocked():
            user.last_login = datetime.now()
            db.session.commit()
            return user

    @bp.input(LoginSchema)
    def post(self, json_data):
        user = db.session.query(User).\
            filter_by(username=json_data['username']).one_or_none()
        if user and not user.blocked and not user.has_role(Roles.api.value):
            if bcrypt.checkpw(json_data['password'].encode('utf-8'), user.password):
                delta_change = datetime.now() - user.pswd_create
                if user.pswd_change and delta_change.days < 365:
                    user.last_login = datetime.now()
                    user.attempt = 0
                    db.session.commit()
                    return {'access_token': create_access_token(identity=user.username), 
                            'refresh_token': create_refresh_token(identity=user.username)}
                return '', 401
            else:
                if user.attempt < 4:
                    user.attempt = user.attempt+1
                else:
                    user.blocked = True
                db.session.commit()
        return '', 403

    @bp.input(LoginSchema)
    def patch(self, json_data):
        user = db.session.query(User).\
            filter_by(username=json_data['username']).one_or_none()
        if user:
            if bcrypt.checkpw(json_data['password'].encode('utf-8'), user.password):
                setattr(user, 'password', bcrypt.hashpw(json_data['new_pswd'].encode('utf-8'), 
                                                        bcrypt.gensalt()))
                setattr(user, "pswd_change", datetime.now())
                db.session.commit()
                return '', 201
        return '', 403


    @jwt_required(verify_type=False)
    def delete(self):
        """
        Logout the user and invalidate the access token.
        """
        jti = get_jwt()["jti"]
        access_expires = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        jwt_redis_blocklist.set(jti, "", ex=access_expires)
        return '', 401

bp.add_url_rule('/login', view_func=LoginView.as_view('login'))


class TokenView(MethodView):

    @jwt_required(refresh=True)
    def post(self):
        access_token = create_access_token(identity=get_jwt_identity())
        return {'access_token': access_token}

bp.add_url_rule('/refresh', view_func=TokenView.as_view('refresh'))


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@jwt.user_identity_loader
def user_identity_lookup(user):
    """
    A function that acts as a user identity loader for the JWT framework.
    Parameters:
        user (Any): The user object to be used for user identity.
    Returns:
        Any: The user object.
    """
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    Look up a user based on JWT data.
    Parameters:
        _jwt_header (dict): The JWT header.
        jwt_data (dict): The JWT data.
    Returns:
        User: The user found based on the JWT data, or None if not found.
    """
    identity = jwt_data["sub"]
    return db.session.query(User).filter_by(username=identity).one_or_none()
