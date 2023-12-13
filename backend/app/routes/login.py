from datetime import datetime
from functools import wraps
import bcrypt

import redis
from flask import current_app, abort
from flask.views import MethodView
from flask_jwt_extended import current_user, \
    create_access_token, create_refresh_token, get_jwt, \
        jwt_required, get_jwt_identity

from . import bp
from .. import jwt, db
from ..models.model import User
from ..models.schema import LoginSchema, PasswordSchema, UserSchema
from ..models.classes import Roles


jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)

class LoginView(MethodView):
    """Login view"""

    @bp.doc(hide=True)
    @bp.output(UserSchema)
    @jwt_required()
    def get(self):
        """
        Retrieves the current authenticated user from the database.
        """
        user = User.get_user(current_user.username)
        if user and not user.blocked:
            user.last_login = datetime.now()
            db.session.commit()
            return user
        return abort
            
    @bp.input(LoginSchema)
    def post(self, json_data):
        """
        Post method for the given API endpoint.
        """
        user = User.get_user(json_data['username'])
        if user and not user.blocked:
            if bcrypt.checkpw(json_data['password'].encode('utf-8'), user.password):
                delta_change = datetime.now() - user.pswd_create
                if user.pswd_change and delta_change.days < 365:
                    user.last_login = datetime.now()
                    user.attempt = 0
                    db.session.commit()
                    if user.has_role(Roles.api.value):
                        return {'message': 'Overdue'}
                    
                    return {'message': 'Authenticated',
                            'access_token': create_access_token(identity=user.username),
                            'refresh_token': create_refresh_token(identity=user.username)}
                return {'message': 'Overdue'}
            else:
                if user.attempt < 9:
                    user.attempt = user.attempt + 1
                else:
                    user.blocked = True
                db.session.commit()
        return {'message': 'Denied'}

    @bp.input(PasswordSchema)
    def patch(self, json_data):
        """
        Patch method for updating user password.
        """
        user = User.get_user(json_data['username'])
        if user:
            if bcrypt.checkpw(json_data['password'].encode('utf-8'), user.password):
                user.password = bcrypt.hashpw(json_data['new_pswd'].encode('utf-8'),
                                              bcrypt.gensalt())
                user.pswd_change = datetime.now()
                db.session.commit()
                return {'message': 'Authenticated'}
        return {'message': 'Denied'}


    @bp.doc(hide=True)
    @jwt_required(verify_type=False)
    def delete(self):
        """
        A function that deletes the JWT token from the Redis blocklist.
        Returns:
            A tuple containing an empty string and the status code 401.
        """
        jti = get_jwt()["jti"]
        access_expires = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        jwt_redis_blocklist.set(jti, "", ex=access_expires)
        return {'message': 'Denied'}
    
bp.add_url_rule('/login', view_func=LoginView.as_view('login'))


class TokenView(MethodView):
    
    """Token view"""
    
    @jwt_required(refresh=True)
    def post(self):
        """
        Generate a new access token for the authenticated user.
        """
        if not User.get_user(current_user.username).blocked:
            access_token = create_access_token(identity=get_jwt_identity())
            return {'access_token': access_token}
        return {'access_token': ''}
    
bp.add_url_rule('/refresh', view_func=TokenView.as_view('refresh'))


def roles_required(*roles):
    """
    A decorator that checks if the authenticated user has the required roles.
    """
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = User.get_user(get_jwt_identity())
            if user is not None and user.has_role(*roles):
                return func(*args, **kwargs)
            else:
                abort(404)
        return wrapper
    return decorator
    

def group_required(*groups):
    """
    Decorator that checks if the user is a member of any of the specified groups 
    before allowing access to the decorated endpoint.
    """
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = User.get_user(get_jwt_identity())
            if user is not None and user.has_group(*groups):
                return func(*args, **kwargs)
            else:
                abort(404)
        return wrapper
    return decorator


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    """
    Check if a token is revoked.
    """
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@jwt.user_identity_loader
def user_identity_lookup(user):
    """
    A function that acts as a user identity loader for the JWT framework.
    """
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    Look up a user based on JWT data.
    """
    return User.get_user(jwt_data["sub"])
