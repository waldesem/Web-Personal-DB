from datetime import datetime
from functools import wraps

import redis
from flask import abort
from flask.views import MethodView
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    jwt_required,
    current_user,
)
from ldap3 import ALL, Server, Connection, Tls, NTLM

from config import Config
from . import bp
from .. import jwt
from ..models.model import Role, db, User
from ..models.schema import LoginSchema, UserSchema
from ..models.classes import Roles


jwt_redis_blocklist = redis.StrictRedis(
    host=Config.JWT_REDIS_HOST,
    port=Config.JWT_REDIS_PORT,
    db=1,
    decode_responses=True,
)


class AuthView(MethodView):
    """Login view"""

    decorators = [bp.doc(hide=True)]

    @jwt_required()
    @bp.output(UserSchema)
    def get(self):
        """
        Retrieves the current authenticated user from the database.
        """
        user = User.get_user(current_user.username)
        if user and not user.blocked and not user.deleted:
            user.last_login = datetime.now()
            db.session.commit()
            return user
        return abort(404)


bp.add_url_rule("/auth", view_func=AuthView.as_view("auth"))


class LoginView(MethodView):
    """Login view"""

    decorators = [bp.doc(hide=True)]

    @bp.input(LoginSchema)
    def post(self, json_data):
        """
        Post method for the given API endpoint.
        """
        # ldap = ldap_auth(json_data["username"], json_data["password"])
        # if ldap:
        #     user = User.get_user(json_data["username"])
        #     if not user:
        #         user = User(
        #         fullname=ldap["fullname"],
        #         email=ldap["email"],
        #         username=json_data["username"],
        #         )
        #     )
        #         db.session.add(user)
        #         db.session.flush()
        #         user.roles.append(
        #             db.session.execute(
        #                 select(Role).filter_by(role=(Roles.user.value))
        #                 ).scalar_one_or_none()
        #         )
        #     if not user.deleted and not user.blocked:
        #         user.last_login = datetime.now()
        #         token = UserSchema().dump(user)
        #         db.session.commit()
        #         return {
        #             "message": "Authenticated",
        #             "access_token": create_access_token(identity=token),
        #             "refresh_token": create_refresh_token(identity=token),
        #         }, 201
            
        user = User.get_user(json_data["username"])
        if user and not user.blocked and not user.deleted:
            if check_password_hash(user.password, json_data["password"]):
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
            and check_password_hash(user.password, json_data["password"])
        ):
            user.password = generate_password_hash(
                json_data["new_pswd"],
                method="scrypt",
                salt_length=16,
            )
            user.pswd_change = datetime.now()
            db.session.commit()
            return {"message": "Changed"}
        return {"message": "Denied"}

    @jwt_required(verify_type=False)
    def delete(self):
        """
        A function that deletes the JWT token from the Redis blocklist.
        """
        jti = get_jwt()["jti"]
        access_expires = Config.JWT_ACCESS_TOKEN_EXPIRES
        jwt_redis_blocklist.set(jti, "", ex=access_expires)
        return {"message": "Denied"}


bp.add_url_rule("/login", view_func=LoginView.as_view("login"))


class RefreshView(MethodView):
    """Refresh view"""

    decorators = [jwt_required(refresh=True), bp.doc(hide=True)]

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


def ldap_auth(user_name, password):
    ldap_user_name = user_name.strip()
    server = Server("ldap://ldap.forumsys.com:389", get_info=ALL)
    connection = Connection(
        server,
        user='uid={},dc=example,dc=com'.format(ldap_user_name),
        password=password,
    )
    if connection.bind():
        connection.search(
            "dc=example,dc=com",
            f"(uid={ldap_user_name})",
        )
        if connection.entries:
            return {
                'fullname': connection.entries[0].cn.value,
                'email': connection.entries[0].mail.value
            }
    else:
        return None


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
    return user["id"]


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    Look up a user based on JWT data.
    """
    return db.session.get(User, jwt_data["sub"])
