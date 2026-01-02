"""Items routes."""

from litestar import Controller, delete, get, post
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: TC002

from app.classes.classes import Roles
from app.depends.auth import role_guard
from app.models.models import Items, models
from app.tables.tables import Base
from app.utils.utilities import select_item


class ItemsController(Controller):
    """Items controller."""

    path = "/items"

    @get("/{person_id:int}")
    async def get_items(self, person_id: int, db_session: AsyncSession) -> dict:
        """Retrieve an all items from the database."""
        async with db_session.begin():
            return {item: select_item(item, person_id, db_session) for item in models}

    @get("/{item:str}/{person_id:int}")
    async def get_item(
        self,
        item: Items,
        person_id: int,
        db_session: AsyncSession,
    ) -> list[dict]:
        """Get an item based on the provided item."""
        async with db_session.begin():
            return select_item(item, person_id, db_session)

    @post(
        "{item:str}/{person_id:int}",
        guards=[role_guard],
        opt={"roles": Roles.user.value},
    )
    async def post_item(
        self,
        item: Items,
        person_id: int,
        data: dict,
        db_session: AsyncSession,
    ) -> dict:
        """Insert or replaces a record in the specified table with the given item ID."""
        async with db_session.begin():
            json_data = models[item].model_validate(data)
            json_dict = json_data.model_dump(exclude_none=True, exclude={"created"})
            json_dict["person_id"] = person_id
            table = Base.metadata.tables[item]
            # Проверяем, есть ли ключ "id" в словаре json_dict
            if item_id := json_dict.pop("id", None):
                # Если есть, создаем запрос на обновление записи с указанным id
                stmt = table.update().where(table.c.id == item_id).values(json_dict)
            else:
                # Если нет, создаем запрос на вставку новой записи
                stmt = table.insert().values(json_dict)
            await db_session.execute(stmt)
            return {"message": "success"}

    @delete(
        "/{item:str}/{item_id:int}",
        guards=[role_guard],
        opt={"roles": Roles.user.value},
    )
    async def delete_item(
        self,
        item: Items,
        item_id: int,
        db_session: AsyncSession,
    ) -> None:
        """Delete an item from the database with item name and item ID."""
        async with db_session.begin():
            table = Base.metadata.tables[item]
            await db_session.execute(
                table.delete().where(table.c.id == item_id),
            )
