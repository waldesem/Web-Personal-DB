from base64 import b64decode, b64encode
from datetime import datetime
from functools import lru_cache, wraps

from flask import abort, current_app, g, request
from werkzeug.local import LocalProxy

from ..model.tables import Users, db_session

current_user = LocalProxy(lambda: get_current_user(g.user_id))


def get_auth(token):
    """
    Decode the given token and check if it matches the secret key.

    Args:
        token (str): The token to be decoded.

    Returns:
        bool: True if the decoded token matches the secret key, False otherwise.
    """
    try:
        decoded = b64decode(token.split(" ", 1)[1]).decode().split(":", 1)
        secret_key, g.user_id = decoded
        return secret_key == current_app.config["SECRET_KEY"]
    except (IndexError, UnicodeDecodeError):
        return False


@lru_cache(maxsize=4)
def get_current_user(user_id):
    """
    Retrieve the current user based on the user ID stored in the global variable 'g.user_id'.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict or None: A instance containing the user's information if the user exists,
            is not blocked, not deleted, and has not changed password in the last year.
            Otherwise, returns None.
    """
    user = db_session.get(Users, user_id)
    delta_change = datetime.now() - user.pswd_create
    if (
        user
        and not user.blocked
        and not user.deleted
        and not user.change_pswd
        and delta_change.days < 365
    ):
        return user.to_dict()
    return None


def create_token(user):
    """
    Generate a token for the given user.

    Args:
        user (dict): A dictionary containing the user's information.

    Returns:
        str: The generated token, encoded in base64.

    This function takes a dictionary containing the user's information
    and generates a token using the secret key and the user's id.
    The token is then encoded in base64 and returned as a string.
    """
    token_parts = [
        current_app.config["SECRET_KEY"],
        str(user.id),
    ]
    token = ":".join(token_parts)
    return b64encode(token.encode()).decode()


def jwt_required():
    """
    Decorator function that checks if the request contains a valid JWT token.

    The decorated function checks if the request contains a valid JWT token in the
    'Authorization' header. If the token is valid, the decorated function is executed.
    Otherwise, a 401 HTTP status code is returned.

    Parameters:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization")
            if header and get_auth(header):
                return func(*args, **kwargs)
            abort(401)

        return wrapper

    return decorator


def roles_required(*roles):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization")
            if header and get_auth(header):
                cur_user = current_user
                if cur_user and cur_user['role'] in roles:
                    return func(*args, **kwargs)
                abort(403)
            abort(401)

        return wrapper

    return decorator
