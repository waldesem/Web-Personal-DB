import json
import os
from typing import Annotated

from fastapi import APIRouter, Depends, File, Response
from fastapi.responses import FileResponse
from sqlmodel import Session
from PIL import Image

from ..utils.folders import Folders
from ..utils.parsers import Anketa
from ..dependencies import Permission
from ..models.classes import Roles
from ..models.schema import AnketaSchemaApi
from ..models.model import engine, Person

blob = APIRouter(prefix="/files", tags=["files"])

@blob.post(
    "/file/{action}/{item_id}", status_code=201, dependencies=[Depends(Permission(roles=[Roles.user.value]))]
)
async def post_files(
    action: str, files: Annotated[list[bytes], File()], item_id: int | None = None
):

    if action == "anketa":
        json_data = AnketaSchemaApi(json.load(files[0]))
        anketa = Anketa(json_data)
        person_id = anketa.parse_anketa()
        return {"message": person_id}

    with Session(engine) as session:
        person = session.get(Person, item_id)
        folders = Folders(
            person.id, person.surname, person.firstname, person.patronymic
        )

    if action == "image":
        folder = folders.create_parent_folder("image")
        im = Image.open(file)
        rgb_im = im.convert("RGB")
        image_path = os.path.join(folder, "image.jpg")
        if os.path.isfile(image_path):
            os.remove(image_path)
        rgb_im.save(image_path)
        return Response(status_code=204)

    folder = folders.create_subfolder(action)
    for file in files:
        if file.filename:
            if not os.path.isfile(os.path.join(folder, file.filename)):
                file.save(os.path.join(folder, file.filename))
    return Response(status_code=204)


@blob.get("/image/{item_id}", dependencies=[Depends(Permission(roles=[Roles.user.value]))])
async def get_image(item_id: int):
    """
    Retrieves a file from the server and sends it as a response.
    """
    with Session(engine) as session:
        person = session.get(Person, item_id)
        folders = Folders(
            person.id, person.surname, person.firstname, person.patronymic
        )
        file_path = os.path.join(folders.create_main_folder(), "image", "image.jpg")
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse("static/no-photo.png")