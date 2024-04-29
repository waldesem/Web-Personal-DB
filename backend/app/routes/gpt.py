from flask import request
from . import bp
from .login import roles_required
from ..models.classes import Roles


@roles_required(Roles.user.value)
@bp.post("/gpt")
@bp.doc(hide=True)
def post_gpt():
    response = request.args.get("query")
    print(response)
    return {
        "answer": "К сожалению, ничего не удалось сгенерировать или сервис отключен"
    }, 201
