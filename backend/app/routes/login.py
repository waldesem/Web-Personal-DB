from datetime import datetime
from functools import wraps
import bcrypt

import redis
from flask import abort
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    jwt_required,
    current_user,
)

from config import Config
from . import bp
from .. import jwt, cache
from ..models.model import db, User
from ..models.schema import LoginSchema, UserSchema


jwt_redis_blocklist = redis.StrictRedis(
    host=Config.JWT_REDIS_HOST,
    port=Config.JWT_REDIS_PORT,
    db=1, decode_responses=True,
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
        if user and not user.blocked and not user.deleted:
            user.last_login = datetime.now()
            db.session.commit()
            return user
        return abort(401)

    @bp.input(LoginSchema)
    def post(self, json_data):
        """
        Post method for the given API endpoint.
        """
        user = User.get_user(json_data["username"])
        if user and not user.blocked and not user.deleted:
            if bcrypt.checkpw(json_data["password"].encode("utf-8"), user.password):
                delta_change = datetime.now() - user.pswd_create
                if user.pswd_change and delta_change.days < 365:
                    user.last_login = datetime.now()
                    user.attempt = 0
                    db.session.commit()
                    token = UserSchema().dump(user)
                    return {
                        "message": "Authenticated",
                        "access_token": create_access_token(identity=token),
                        "refresh_token": create_refresh_token(identity=token),
                    }, 201
                return {"message": "Overdue"}, 201
            else:
                if user.attempt < 9:
                    user.attempt += 1
                else:
                    user.blocked = True
                db.session.commit()
        return {"message": "Denied"}, 201

    @bp.input(LoginSchema)
    def patch(self, json_data):
        """
        Patch method for updating user password.
        """
        user = User.get_user(json_data["username"])
        if (
            user
            and not user.blocked
            and bcrypt.checkpw(json_data["password"].encode("utf-8"), user.password)
        ):
            user.password = bcrypt.hashpw(
                json_data["new_pswd"].encode("utf-8"), bcrypt.gensalt()
            )
            user.pswd_change = datetime.now()
            db.session.commit()
            return {"message": "Changed"}
        return {"message": "Denied"}

    @bp.doc(hide=True)
    @jwt_required(verify_type=False)
    def delete(self):
        """
        A function that deletes the JWT token from the Redis blocklist.
        """
        jti = get_jwt()["jti"]
        access_expires = Config.JWT_ACCESS_TOKEN_EXPIRES
        jwt_redis_blocklist.set(jti, "", ex=access_expires)
        cache.clear()
        return {"message": "Denied"}


bp.add_url_rule("/login", view_func=LoginView.as_view("login"))


class RefreshView(MethodView):
    """Refresh view"""

    @jwt_required(refresh=True)
    def post(self):
        """
        Generate a new access token for the authenticated user.
        """
        user = db.session.get(User, current_user.id)
        if user and not user.blocked and not user.deleted:
            return {
                "access_token": create_access_token(identity=UserSchema().dump(user))
            }
        return {"access_token": ""}, 401


bp.add_url_rule("/refresh", view_func=RefreshView.as_view("refresh"))


def roles_required(*roles):
    """
    A decorator that checks if the authenticated user has the required roles.
    """

    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            if any(r.role in roles for r in current_user.roles):
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


@cache.memoize()
@jwt.user_identity_loader
def user_identity_lookup(user):
    """
    A function that acts as a user identity loader for the JWT framework.
    """
    return user['id']


@cache.memoize()
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    Look up a user based on JWT data.
    """
    return db.session.get(User, jwt_data["sub"])
