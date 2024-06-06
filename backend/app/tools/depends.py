from base64 import b64decode, b64encode
from functools import wraps

from flask import abort, request

from config import Config
from .queries import select_single


class Token:
    current_user = None

    @classmethod
    def get_auth(cls, token):
        Token.current_user = None
        cuted = token.replace("Basic ", "")
        decoded = b64decode(cuted).decode()
        secret, user_id, *_ = decoded.split(":")
        if secret == Config.SECRET_KEY:
            user = select_single("SELECT * FROM users WHERE id = ?", (user_id,))
            if user and not user["blocked"] and not user["deleted"]:
                Token.current_user = user
                return True
        return False


def create_token(user_id, fullname, username, has_admin):
    return b64encode(
        f"{Config.SECRET_KEY}:{user_id}:{fullname};{username}:{has_admin}".encode()
    ).decode()


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


def admin_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization")
            if Token.get_auth(header):
                if Token.current_user["has_admin"]:
                    return func(*args, **kwargs)
                else:
                    abort(404)
            else:
                abort(404)

        return wrapper

    return decorator
