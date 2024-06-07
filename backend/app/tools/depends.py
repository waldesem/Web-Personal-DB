from base64 import b64decode, b64encode
from datetime import datetime
from functools import wraps

from flask import abort, request, g
from werkzeug.local import LocalProxy

from config import Config
from .queries import select_single


current_user = LocalProxy(lambda: get_current_user())


def get_auth(token):
    cuted = token.replace("Basic ", "")
    decoded = b64decode(cuted).decode()
    secret, g.user_id, *_ = decoded.split(":")
    return secret == Config.SECRET_KEY


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
    return (
        b64encode(
            f"{Config.SECRET_KEY}:{user['id']}:{user['fullname']};{user['username']}:{user['region']}:{user['has_admin']}"
        )
        .encode()
        .decode()
    )


def jwt_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization")
            if get_auth(header):
                return func(*args, **kwargs)
            else:
                abort(401)

        return wrapper

    return decorator


def user_required(admin=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization")
            if get_auth(header):
                if current_user:
                    if admin:
                        if current_user["has_admin"]:
                            return func(*args, **kwargs)
                        else:
                            abort(403)
                    else:
                        return func(*args, **kwargs)
                else:
                    abort(403)
            else:
                abort(401)

        return wrapper

    return decorator
