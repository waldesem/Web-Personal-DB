from datetime import datetime
from functools import wraps

import bcrypt
import redis
from flask import current_app, abort
from flask.views import MethodView
from flask_jwt_extended import current_user, create_access_token, \
    create_refresh_token, get_jwt, jwt_required, get_jwt_identity
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from . import bp
from .. import jwt
from ..models.model import async_session, User
from ..models.schema import LoginSchema, PasswordSchema, UserSchema
from ..models.classes import Roles

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


def roles_required(*roles):
    """
    This function is a decorator that checks if the user has the required roles 
    to access a given route.
    Parameters:
        *roles (str): Variable number of roles that the user must have. 
        Each role is a string.
    Returns:
        decorator (function): The decorator function that wraps the original 
        function and performs the role check.
    """
    async def decorator(func):
        @wraps(func)
        @jwt_required()
        async def wrapper(*args, **kwargs):
            async with async_session() as session:
                user = await session.execute(
                    select(User)
                    .filter_by(username=get_jwt_identity())
                    .options(selectinload(User.roles))
                ).scalar_one_or_none()
                if user is not None and any(user.has_role(role) for role in roles):
                    return await func(*args, **kwargs)
                else:
                    abort(404)
        return wrapper
    return decorator


def group_required(*groups):
    """
    Decorator that checks if the user is a member of any of the specified groups 
    before allowing access to the decorated endpoint.
    Parameters:
        * groups: A variable number of group names to check membership against.
    Returns:
        A decorated wrapper function that checks if the user has the required 
        group membership before allowing access to the decorated endpoint.
    """
    async def decorator(func):
        @wraps(func)
        @jwt_required()
        async def wrapper(*args, **kwargs):
            async with async_session() as session:
                user = await session.execute(
                    select(User)
                    .filter_by(username=get_jwt_identity())
                    .options(selectinload(User.groups))
                ).scalar_one_or_none()
                if user is not None and any(user.has_group(group)
                                            for group in groups):
                    return await func(*args, **kwargs)
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
                filter(User.username == current_user.username, 
                       User.blocked == False).one_or_none()
            if user:
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
            dict: A dictionary containing the access and refresh tokens.
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
                        
                        return {
                            'message': 'Authenticated',
                            'access_token': create_access_token(identity=user.username),
                            'refresh_token': create_refresh_token(identity=user.username)
                            }
                    return {'message': 'Overdue'}
                else:
                    if user.attempt < 9:
                        user.attempt += 1
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
        """
        async with async_session() as session:
            user = await session.execute(User).\
                filter_by(username=json_data['username']).one_or_none()
            
            if user is None or not bcrypt.checkpw(
                json_data['password'].encode('utf-8'), user.password
            ):
                return {'message': 'Denied'}
            
            user.password = bcrypt.hashpw(
                json_data['new_pswd'].encode('utf-8'), bcrypt.gensalt()
            )
            user.pswd_change = datetime.now()
            await session.commit()
            
            return {'message': 'Authenticated'}

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
                filter(User.username == current_user.username). \
                filter(User.blocked == False). \
                one_or_none()
            access_token = create_access_token(identity=get_jwt_identity()) if user else ''
            return {'access_token': access_token}

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
    token_in_redis = await jwt_redis_blocklist.exists(jwt_payload["jti"])
    return token_in_redis


@jwt.user_identity_loader
async def user_identity_lookup(user):
    return user


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
        query = session.execute(User).filter_by(username=jwt_data["sub"])
        return await query.one_or_none()
