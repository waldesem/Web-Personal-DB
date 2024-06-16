from base64 import b64decode, b64encode
from datetime import datetime
from functools import wraps

from flask import abort, request, g
from werkzeug.local import LocalProxy

from config import Config
from .queries import select_single


current_user = LocalProxy(lambda: get_current_user())


def get_auth(token):
    try:
        decoded = b64decode(token.split(" ", 1)[1]).decode().split(":", 2)
        g.user_id = decoded[1]
        return decoded[0] == Config.SECRET_KEY
    except (IndexError, UnicodeDecodeError):
        return False


def get_current_user():
    user = select_single("SELECT * FROM users WHERE id = ?", (g.user_id,))
    delta_change = datetime.now() - datetime.fromisoformat(user["pswd_create"])
    if (
        user
        and not user["blocked"]
        and not user["deleted"]
        and not user["change_pswd"]
        and delta_change.days < 365
    ):
        return user
    return None


def create_token(user):
    token_parts = [
        Config.SECRET_KEY,
        str(user["id"]),
        user["username"],
        user["region"],
        str(user["has_admin"]),
    ]
    token = ":".join(token_parts)
    return b64encode(token.encode()).decode()


def jwt_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization")
            if header and get_auth(header):
                return func(*args, **kwargs)
            abort(401)
        return wrapper
    return decorator


def user_required(admin=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization")
            if header and get_auth(header):
                if current_user and (
                    not current_user["blocked"]
                    and not current_user["deleted"]
                    and (not admin or current_user["has_admin"])
                ):
                    return func(*args, **kwargs)
                abort(403 if current_user else 401)

        return wrapper

    return decorator
