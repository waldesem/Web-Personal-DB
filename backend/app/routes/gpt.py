from . import bp
from .login import roles_required
from ..models.classes import Roles
from ..models.schema import GptInputSchema, GptOutputSchema


@roles_required(Roles.user.value)
@bp.post("/gpt")
@bp.input(GptInputSchema)
@bp.output(GptOutputSchema)
@bp.doc(hide=True)
def post_gpt(json_data):
    print(json_data)
    return {
        "answer": "К сожалению, ничего не удалось сгенерировать или сервис отключен"
    }, 201
