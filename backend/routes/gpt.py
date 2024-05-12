from fastapi import APIRouter, Depends
from ..dependencies import Permission
from ..models.classes import Roles
from ..models.schema import SchemaGptInput, SchemaGptOutput

gpt = APIRouter(prefix="/gpt", tags=["gpt"])

@gpt.post(
    "/gpt",
    status_code=201,
    response_model=SchemaGptOutput,
    dependencies=[Depends(Permission(roles=[Roles.user.value]))],
)
async def post_gpt(query: SchemaGptInput):
    print(query)
    return {
        "answer": "К сожалению, ничего не удалось сгенерировать или сервис отключен"
    }
