"""Items routes."""

from litestar import Controller, delete, get, post

from app.models.models import Items, models
from app.tables.tables import Base, session
from app.utils.utilities import select_item


class ItemsController(Controller):
    path = "/items"

    @get("/{person_id:int}")
    async def get_items(self, person_id: int, sync_to_thread: bool = False) -> dict:
        """Retrieve an all items from the database."""
        return {item: select_item(item, person_id) for item in models}

    @get("/{item:str}/{person_id:int}")
    async def get_item(item: Items, person_id: int) -> list[dict]:
        """Get an item based on the provided item."""
        return select_item(item, person_id)

    @post("{item:str}/{person_id:int}")
    async def post_item(
        self,
        item: Items,
        person_id: int,
        json_data: dict,
        sync_to_thread: bool = False,
    ) -> dict:
        """Insert or replaces a record in the specified table with the given item ID."""
        data = models[item].model_validate(json_data)
        json_dict = data.model_dump(exclude_none=True, exclude={"created"})
        json_dict["person_id"] = person_id
        table = Base.metadata.tables[item]
        # Проверяем, есть ли ключ "id" в словаре json_dict
        if item_id := json_dict.pop("id", None):
            # Если есть, создаем запрос на обновление записи с указанным id
            stmt = table.update().where(table.c.id == item_id).values(json_dict)
        else:
            # Если нет, создаем запрос на вставку новой записи
            stmt = table.insert().values(json_dict)
        session.execute(stmt)
        session.commit()
        return {"message": "success"}

    @delete("/{item:str}/{item_id:int}")
    async def delete_item(
        self,
        item: Items,
        item_id: int,
        sync_to_thread: bool = False,
    ) -> None:
        """Delete an item from the database based on the provided item name and item ID."""
        table = Base.metadata.tables[item]
        session.execute(
            table.delete().where(table.c.id == item_id),
        )
        session.commit()
