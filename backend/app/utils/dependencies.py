from functools import wraps
from base64 import b64decode, b64encode

from flask import abort, request
from sqlalchemy.orm import Session

from config import Config
from ..models.model import engine, User


class Token:
    current_user = None

    @classmethod
    def get_auth(cls, token):
        Token.current_user = None
        token = token.replace("Basic ", "")
        decoded = b64decode(token).decode()
        user_id, secret = decoded.split(":")
        if user_id and secret == Config.SECRET_KEY:
            with Session(engine) as session:
                if user_id:
                    user = session.get(User, user_id)
                    if user and not user.deleted and not user.blocked:
                        Token.current_user = user
                        return True
        return False


def create_token(cridentials):
    return b64encode(f"{cridentials}:{Config.SECRET_KEY}".encode()).decode()


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
                if any(r.role in roles for r in Token.current_user.roles):
                    return func(*args, **kwargs)
                else:
                    abort(404)
            else:
                abort(404)

        return wrapper

    return decorator
