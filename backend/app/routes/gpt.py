from . import bp
from .login import roles_required
from ..models.classes import Roles
from ..models.schema import GptInputSchema, GptOutputSchema


@roles_required(Roles.user.value)
@bp.doc(hide=True)
@bp.input(GptInputSchema)
@bp.output(GptOutputSchema)
@bp.post("/gpt")
def postGPT(json_data):
    print(json_data)
    return {
        "answer": "К сожалению, ничего не удалось сгенерировать или сервис отключен"
    }, 201
