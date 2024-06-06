from base64 import b64decode, b64encode
from functools import wraps

from flask import abort, request

from .queries import select_single
from config import Config


class Token:
    current_user = None

    @classmethod
    def get_auth(cls, token):
        Token.current_user = None
        token = token.replace("Basic ", "")
        decoded = b64decode(token).decode()
        secret, user_id, _ = decoded.split(":")
        if secret and user_id == Config.SECRET_KEY:
            user = select_single("SELECT * FROM users WHERE id = ?", (user_id,))
            if user and not user["blocked"]:
                Token.current_user = user
                return True
        return False


def create_token(user_id, has_admin):
    return b64encode(f"{Config.SECRET_KEY}:{user_id}:{has_admin}".encode()).decode()


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
