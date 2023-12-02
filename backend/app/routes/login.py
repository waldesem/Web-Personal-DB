from datetime import datetime
from functools import wraps

import bcrypt
import redis
from flask import current_app, abort
from flask.views import MethodView
from flask_jwt_extended import current_user, create_access_token, \
    create_refresh_token, get_jwt, jwt_required, get_jwt_identity
from sqlalchemy import select

from . import bp
from .. import jwt
from ..models.model import async_session, User
from ..models.schema import LoginSchema, PasswordSchema, UserSchema
from ..models.classes import Roles

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


async def roles_required(*roles):
    """
    A decorator that checks if the authenticated user has the required roles.
    Parameters:
        *roles: Variable length argument list of strings representing the roles required.
    Returns:
        A decorated function that is executed only if the user has the required roles.
        Otherwise, a 404 error is raised.
    """
    async def decorator(func):
        @wraps(func)
        @jwt_required()
        async def wrapper(*args, **kwargs):
            async with async_session() as session:
                user = await session.execute(select(User)). \
                    filter_by(username=get_jwt_identity()).one_or_none()
                if await user is not None and any(user.has_role(role)
                                            for role in roles):
                    return await func(*args, **kwargs)
                else:
                    abort(404)
        return wrapper
    return decorator


async def group_required(*groups):
    """
    Decorator that checks if the user is a member of any of the specified groups before allowing access to the decorated endpoint.
    Parameters:
        * groups: A variable number of group names to check membership against.
    Returns:
        A decorated wrapper function that checks if the user has the required group membership before allowing access to the decorated endpoint.
    """
    async def decorator(func):
        @wraps(func)
        @jwt_required()
        async def wrapper(*args, **kwargs):
            async with async_session() as session:
                user = await session.execute(select(User)). \
                    filter_by(username=get_jwt_identity()).one_or_none()
                if user is not None and any(user.has_group(group)
                                            for group in groups):
                    return func(*args, **kwargs)
                else:
                    abort(404)
        return wrapper
    return decorator


class LoginView(MethodView):
    """Login view"""

    @bp.doc(hide=True)
    @jwt_required()
    @bp.output(UserSchema)
    async def get(self):
        """
        Retrieves the current authenticated user from the database.
        Returns:
            User: The user object representing the current authenticated user.
        """
        async with async_session() as session:
            user = session.query(User). \
                filter_by(username=current_user.username).one_or_none()
            if user and not user.blocked:
                user.last_login = datetime.now()
                await session.commit()
                return user
            
    @bp.input(LoginSchema)
    async def post(self, json_data):
        """
        Post method for the given API endpoint.

        Args:
            json_data (dict): The JSON data received in the request.

        Returns:
            tuple: A tuple containing the access token and refresh token if the login is successful, 
                   otherwise an empty string and the appropriate status code.
        """
        async with async_session() as session:
            user = await session.query(User). \
                filter_by(username=json_data['username']).one_or_none()
            if user and not user.blocked:
                if bcrypt.checkpw(json_data['password'].encode('utf-8'), user.password):
                    delta_change = datetime.now() - user.pswd_create
                    if user.pswd_change and delta_change.days < 365:
                        user.last_login = datetime.now()
                        user.attempt = 0
                        await session.commit()
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
                    await session.commit()
            return {'message': 'Denied'}
        
    @bp.doc(hide=True)
    @bp.input(PasswordSchema)
    async def patch(self, json_data):
        """
        Patch method for updating user password.
        Args:
            json_data (dict): The JSON data containing the username, password, and new password.
        
        Returns:
            tuple: A tuple containing an empty string and the HTTP status code.
        
        Raises:
            None
        """
        async with async_session() as session:
            user = await session.execute(User). \
                filter_by(username=json_data['username']).one_or_none()
            if user:
                if bcrypt.checkpw(json_data['password'].encode('utf-8'), user.password):
                    user.password = bcrypt.hashpw(json_data['new_pswd'].encode('utf-8'),
                                                bcrypt.gensalt())
                    user.pswd_change = datetime.now()
                    await session.commit()
                    return {'message': 'Authenticated'}
            return {'message': 'Denied'}
        
    @bp.doc(hide=True)
    @jwt_required(verify_type=False)
    async def delete(self):
        """
        A function that deletes the JWT token from the Redis blocklist.
        Returns:
            A tuple containing an empty string and the status code 401.
        """
        access_expires = await current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        await jwt_redis_blocklist.set(get_jwt()["jti"], "", ex=access_expires)
        return {'message': 'Denied'}


bp.add_url_rule('/login', view_func=LoginView.as_view('login'))


class TokenView(MethodView):
    """Token view"""

    @jwt_required(refresh=True)
    @bp.doc(hide=True)
    async def post(self):
        """
        Generate a new access token for the authenticated user.
        Returns:
            dict: A dictionary containing the access token.
        """
        async with async_session() as session:
            user = await session.execute(User). \
                filter_by(username=current_user.username).one_or_none()
            if not user.blocked:
                access_token = create_access_token(identity=get_jwt_identity())
                return {'access_token': access_token}
            return {'access_token': ''}

bp.add_url_rule('/refresh', view_func=TokenView.as_view('refresh'))


@jwt.token_in_blocklist_loader
async def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    """
    Check if a token is revoked.
    Parameters:
        jwt_header (Any): The JWT header.
        jwt_payload (dict): The JWT payload.
    Returns:
        bool: True if the token is revoked, False otherwise.
    """
    token_in_redis = await jwt_redis_blocklist.get(jwt_payload["jti"])
    return await token_in_redis is not None


@jwt.user_identity_loader
async def user_identity_lookup(user):
    """
    A function that acts as a user identity loader for the JWT framework.
    Parameters:
        user (Any): The user object to be used for user identity.
    Returns:
        Any: The user object.
    """
    return await user


@jwt.user_lookup_loader
async def user_lookup_callback(_jwt_header, jwt_data):
    """
    Look up a user based on JWT data.
    Parameters:
        _jwt_header (dict): The JWT header.
        jwt_data (dict): The JWT data.
    Returns:
        User: The user found based on the JWT data, or None if not found.
    """
    async with async_session() as session:
        return await session.execute(User).filter_by(username=jwt_data["sub"]).one_or_none()