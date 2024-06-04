import sqlite3
from base64 import b64decode, b64encode
from functools import wraps

from config import Config
from flask import abort, request


def select_roles(user_id):
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        cursor = conn.cursor()
        query = cursor.execute(
            "SELECT roles.role FROM user_roles LEFT JOIN roles ON user_roles.role_id = roles.id WHERE user_id = ?",
            (user_id),
        )
        return [role[0] for role in query.fetchall()]

class Token:
    current_user = None

    @classmethod
    def get_auth(cls, token):
        Token.current_user = None
        token = token.replace("Basic ", "")
        decoded = b64decode(token).decode()
        secret, user_id, _ = decoded.split(":")
        if  secret and user_id == Config.SECRET_KEY:
            with sqlite3.connect(Config.DATABASE_URI) as conn:
                cursor = conn.cursor()
                query = cursor.execute(
                    "SELECT * FROM users WHERE id = ?", (user_id,)
                )
                col_names = [i[0] for i in query.description]
                user = dict(zip(col_names, query.fetchone()))
                user["roles"] = select_roles(user_id)
                if user and not user["deleted"] and not user["blocked"]:
                    Token.current_user = user
                    return True
        return False


def create_token(user_id, roles):
    return b64encode(f"{Config.SECRET_KEY}:{user_id}:{roles}".encode()).decode()


def jwt_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization")
            if Token.get_auth(header):
                return func(*args, **kwargs)
            else:
                abort(404)

        return wrapper

    return decorator


def roles_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization")
            if Token.get_auth(header):
                if any(r in roles for r in Token.current_user["roles"]):
                    return func(*args, **kwargs)
                else:
                    abort(404)
            else:
                abort(404)

        return wrapper

    return decorator
