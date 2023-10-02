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
    """Require roles or groups"""

    def roles_required(self, *roles):
        """
        A decorator that checks if the authenticated user has the required roles.

        Parameters:
            *roles: Variable length argument list of strings representing the roles required.

        Returns:
            A decorated function that is executed only if the user has the required roles.
            Otherwise, a 404 error is raised.
        """
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
        """
        Decorator that checks if the user is a member of any of the specified groups before allowing access to the decorated endpoint.

        Parameters:
            * groups: A variable number of group names to check membership against.

        Returns:
            A decorated wrapper function that checks if the user has the required group membership before allowing access to the decorated endpoint.
        """
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
    """Login view"""

    decorators = [bp.doc(hide=True)]
        
    @jwt_required()
    @bp.output(UserSchema)
    def get(self): 
        """
        Retrieves the current authenticated user from the database.

        Returns:
            User: The user object representing the current authenticated user.
        """
        user = db.session.query(User).\
            filter_by(username=current_user.username).one_or_none()
        if user and not user.has_blocked():
            user.last_login = datetime.now()
            db.session.commit()
            return user

    @bp.input(LoginSchema)
    def post(self, json_data):
        """
        Post method for the given API endpoint.

        Args:
            json_data (dict): The JSON data received in the request.

        Returns:
            tuple: A tuple containing the access token and refresh token if the login is successful, 
                   otherwise an empty string and the appropriate status code.
        """
        user = db.session.query(User).\
            filter_by(username=json_data['username']).one_or_none()
        if user and not user.blocked and not user.has_role(Roles.api.value):
            if bcrypt.checkpw(json_data['password'].encode('utf-8'), user.password):
                delta_change = datetime.now() - user.pswd_create
                if user.pswd_change and delta_change.days < 365:
                    user.last_login = datetime.now()
                    user.attempt = 0
                    db.session.commit()
                    return {'message': 'Authenticated',
                        'access_token': create_access_token(identity=user.username), 
                            'refresh_token': create_refresh_token(identity=user.username)}
                return {'message': 'Overdue'}
            else:
                if user.attempt < 9:
                    user.attempt = user.attempt+1
                else:
                    user.blocked = True
                db.session.commit()
        return {'message': 'Denied'}
    
    @bp.input(LoginSchema)
    def patch(self, json_data):
        """
        Patch method for updating user password.
        
        Args:
            json_data (dict): The JSON data containing the username, password, and new password.
        
        Returns:
            tuple: A tuple containing an empty string and the HTTP status code.
        
        Raises:
            None
        """
        user = db.session.query(User).\
            filter_by(username=json_data['username']).one_or_none()
        if user:
            if bcrypt.checkpw(json_data['password'].encode('utf-8'), user.password):
                user.password = bcrypt.hashpw(json_data['new_pswd'].encode('utf-8'), 
                                                        bcrypt.gensalt())
                user.pswd_change = datetime.now()
                db.session.commit()
                return {'message': 'Authenticated'}
        return {'message': 'Denied'}


    @jwt_required(verify_type=False)
    def delete(self):
        """
        A function that deletes the JWT token from the Redis blocklist.

        Parameters:
            None

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
    @bp.doc(hide=True)
    def post(self):
        """
        Generate a new access token for the authenticated user.

        Returns:
            dict: A dictionary containing the access token.
                {
                    'access_token': str
                }
        """
        access_token = create_access_token(identity=get_jwt_identity())
        return {'access_token': access_token}

bp.add_url_rule('/refresh', view_func=TokenView.as_view('refresh'))


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    """
    Check if a token is revoked.

    Parameters:
        jwt_header (Any): The JWT header.
        jwt_payload (dict): The JWT payload.

    Returns:
        bool: True if the token is revoked, False otherwise.
    """
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
