from datetime import datetime
from functools import lru_cache, wraps

from flask import abort, current_app, g, request
import jwt
from werkzeug.local import LocalProxy

from ..model.tables import Users, db_session

current_user = LocalProxy(lambda: get_current_user(g.user_id))


def get_auth(token):
    """
    Validates a JWT token and stores the user ID in the g object.

    Parameters:
        token (str): The JWT token to validate.

    Returns:
        bool: True if the token is valid, False if not.
    """
    try:
        decoded = jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
        )
        g.user_id = decoded["id"]
        return True
    except jwt.exceptions.InvalidTokenError:
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
    Creates a JWT token containing the user's information.

    Args:
        user (dict): A dictionary containing the user's information.

    Returns:
        str: The JWT token.
    """

    return jwt.encode(user, current_app.config["SECRET_KEY"], algorithm="HS256")


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
                if cur_user and cur_user["role"] in roles:
                    return func(*args, **kwargs)
                abort(403)
            abort(401)

        return wrapper

    return decorator
