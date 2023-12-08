from datetime import datetime
from functools import wraps

import bcrypt
import redis
from flask import current_app, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, \
    get_jwt, jwt_required, get_jwt_identity
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from . import bp
from .. import jwt
from ..models.model import  engine, User
from ..models.schema import LoginSchema, PasswordSchema, UserSchema


jwt_redis_blocklist = redis.StrictRedis(
    host="localhost",
    port=6379, 
    db=0, 
    decode_responses=True
    )


class LoginView(MethodView):
    """Login view"""

    @bp.doc(hide=True)
    @jwt_required()
    @bp.output(UserSchema)
    async def get(self):
        """
        Retrieves the current authenticated user from the database.
         """
        async with AsyncSession(engine) as session:
            async with session.begin():
                user_query = await session.execute(
                    select(User)
                    .filter_by(username=get_jwt_identity()) 
                    .filter(User.blocked == False)
                    .options(selectinload(User.groups))
                    .options(selectinload(User.roles))
                )
                user = user_query.scalar_one_or_none()
                if user:
                    user.last_login = datetime.now()
                await session.close()
                await engine.dispose()
                return user
            
    @bp.input(LoginSchema)
    async def post(self, json_data):
        async with AsyncSession(engine) as session:
                user_query = await session.execute(
                    select(User)
                    .filter_by(username=json_data['username'])
                )
                user = user_query.scalar_one_or_none()
                if user and not user.blocked:
                    if bcrypt.checkpw(json_data['password'].encode('utf-8'), user.password):
                        delta_change = datetime.now() - user.pswd_create
                        
                        if user.pswd_change and delta_change.days < 365:
                            user.last_login = datetime.now()
                            user.attempt = 0
                            await engine.dispose()
                            return {
                                'message': 'Authenticated',
                                'access_token': create_access_token(identity=user.username),
                                'refresh_token': create_refresh_token(identity=user.username)
                                }
                        else:
                            await engine.dispose()
                            return {'message': 'Overdue'}
                    else:
                        if user.attempt < 9:
                            user.attempt += 1
                        else:
                            user.blocked = True
                await engine.dispose()
                return {'message': 'Denied'}

    @bp.input(PasswordSchema)
    async def patch(self, json_data):
        """
        Patch method for updating user password.
        """
        async with AsyncSession(engine) as session:
            async with session.begin():
                user_query = await session.execute(
                    select(User)
                    .filter_by(username=json_data['username'])
                )
                user = user_query.scalar_one_or_none()
                
                if user is None or not bcrypt.checkpw(
                    json_data['password'].encode('utf-8'), 
                    user.password
                    ):
                    await engine.dispose()
                    return {'message': 'Denied'}
                
                user.password = bcrypt.hashpw(
                    json_data['new_pswd'].encode('utf-8'), 
                    bcrypt.gensalt()
                    )
                user.pswd_change = datetime.now()
                await engine.dispose()
                return {'message': 'Authenticated'}

    @jwt_required(verify_type=False)
    def delete(self):
        """
        A function that deletes the JWT token from the Redis blocklist.
        """
        access_expires = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        jwt_redis_blocklist.set(get_jwt()["jti"], "", ex=access_expires)
        return {'message': 'Denied'}

bp.add_url_rule('/login', view_func=LoginView.as_view('login'))


class TokenView(MethodView):
    """Token view"""

    @jwt_required(refresh=True)
    def post(self):
        """
        Generate a new access token for the authenticated user.
        """
        access_token = create_access_token(identity=get_jwt_identity())
        return {'access_token': access_token}

bp.add_url_rule('/refresh', view_func=TokenView.as_view('refresh'))


def roles_required(*roles):
    """
    This function is a decorator that checks if the user has the required roles 
    to access a given route.
     """
    def decorator(func):
        @wraps(func)
        @jwt_required()
        async def wrapper(*args, **kwargs):
            user = await get_user(User.roles)
            user_roles = [user.role for user in user.roles]
            if user and any(r == item for item in user_roles for r in roles):
                return await func(*args, **kwargs)
            else:
                return await abort(404)
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
        async def wrapper(*args, **kwargs):
            user = await get_user(User.groups)      
            user_groups = [user.group for user in user.groups]
            if user and any(g == item for item in user_groups for g in groups):
                return await func(*args, **kwargs)
            else:
                return await abort(404)
        return wrapper
    return decorator


async def get_user(model_attr):
    async with AsyncSession(engine) as session:
        async with session.begin():
            user = await session.execute(
                select(User)
                .filter_by(username=get_jwt_identity())
                .options(selectinload(model_attr))
            )
            await session.close()
            await engine.dispose()
            return user.scalar_one_or_none()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    """
    Check if a token is revoked.
    """
    token_in_redis = jwt_redis_blocklist.exists(jwt_payload["jti"])
    return token_in_redis


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    Look up a user based on JWT data.
    """
    async def load_collback():
        return await user_lookup(jwt_data)
    return load_collback


async def user_lookup(jwt_data):
    async with AsyncSession(engine) as session:
        async with session.begin():
            user = await session.execute(
                select(User)
                .filter_by(username=jwt_data["sub"])
                )
            await engine.dispose()
            return user.scalar_one_or_none()
