"""Person routes."""

from pathlib import Path

from litestar import Controller, delete, get, post

from app.models.models import PersonIn, PersonOut
from app.tables.tables import Persons, session
from app.utils.utilities import create_destination, upload_resume


class PersonController(Controller):
    @get("/persons/{person_id:int}")
    async def get_person(self, person_id: int, sync_to_thread: bool = False) -> dict:
        """Retrieve an item from the database based on the provided item ID."""
        person = session.get(Persons, person_id)
        if not person.destination or not Path(person.destination).exists():
            person.destination = create_destination(person)
            session.commit()
        return PersonOut.model_validate(person).model_dump()

    @post("/persons")
    async def post_person(
        self,
        data: PersonIn,
        sync_to_thread: bool = False,
    ) -> dict:
        """Replace a record in persons table."""
        # Загружаем резюме, получаем id кандидата, а также был ли он ранее загружен
        cand_id, existed = upload_resume(data)
        return {"person_id": cand_id, "exists": existed}

    @delete("/persons/{person_id:int}")
    async def delete_person(
        self,
        person_id: int,
        sync_to_thread: bool = False,
    ) -> None:
        """Delete an item from the database based on the provided item name and item ID."""
        person = session.get(Persons, person_id)
        session.delete(person)
        session.commit()
