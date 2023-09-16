from werkzeug.exceptions import BadRequest
from . import bp


@bp.errorhandler(BadRequest)
def handle_bad_request(e):
    """
    A decorator function that handles the BadRequest error.
    Parameters:
    - e (BadRequest): The BadRequest error object.
    Returns:
    - str: The error message 'bad request!'.
    - int: The HTTP status code 400.
    """
    return 'bad request!', 400