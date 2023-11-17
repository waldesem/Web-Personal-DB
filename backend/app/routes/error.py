from werkzeug.exceptions import BadRequest
from . import bp


@bp.errorhandler(BadRequest)
def handle_bad_request(e):
    
    return 'bad request!', 400