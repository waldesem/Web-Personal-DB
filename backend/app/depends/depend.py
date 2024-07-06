from functools import lru_cache
from base64 import b64decode, b64encode
from datetime import datetime
from functools import wraps

from flask import abort, current_app,  request, g
from werkzeug.local import LocalProxy

from ..databases.database import select


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
        decoded = b64decode(token.split(" ", 1)[1]).decode().split(":", 2)
        secret_key, g.user_id, _ = decoded
        return secret_key == current_app.config["SECRET_KEY"]
    except (IndexError, UnicodeDecodeError):
        return False


@lru_cache(maxsize=8)
def get_current_user(user_id):
    """
    Retrieves the current user based on the user ID stored in the global variable 'g.user_id'.
    """
    user = select("SELECT * FROM users WHERE id = ?", args=(user_id,))
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
        str(user["id"]),
        user["username"],
        str(user["has_admin"]),
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


def user_required(admin=False):
    """
    A decorator function that checks if the user is authorized to access a specific resource.
    
    Parameters:
        admin (bool): A boolean indicating whether the user is an admin or not. Default is False.
        func (function): The function to be decorated.
    
    Returns:
        function: The decorated function that checks user authorization before executing the original function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization")
            if header and get_auth(header):
                cu = current_user
                if cu and (
                    not admin or cu["has_admin"]
                ):
                    return func(*args, **kwargs)
                abort(403)
            abort(401)

        return wrapper

    return decorator
