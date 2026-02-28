"""Items routes."""

from advanced_alchemy.base import BigIntAuditBase
from litestar import Controller, delete, get, post
from sqlalchemy import func, label, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.classes.classes import ItemCategory, Roles
from app.depends.auth import role_guard
from app.models.models import ItemModel, ItemsModel


class ItemsController(Controller):
    """Items controller."""

    path = "/items"
    tables = BigIntAuditBase.metadata.tables

    @staticmethod
    async def select_item(
        item: ItemCategory,
        person_id: int,
        db_session: AsyncSession,
    ) -> list[ItemModel]:
        """Retrieve an item from the database based on the provided item."""
        table = ItemsController.tables[item]
        stmt = (
            select(table, label("item", func.str(item)))
            .filter(table.c.person_id == person_id)
            .order_by(table.c.id.desc())
        )
        items = (await db_session.execute(stmt)).all()
        return ItemsModel.model_validate({"item": items}).items

    @get("/{person_id:int}")
    async def get_items(
        self,
        person_id: int,
        db_session: AsyncSession,
    ) -> dict[ItemCategory, list[ItemModel]]:
        """Retrieve an all items from the database."""
        return {
            item.value: await self.select_item(item.value, person_id, db_session)
            for item in ItemCategory
        }

    @get("/{item:str}/{person_id:int}")
    async def get_item(
        self,
        item: ItemCategory,
        person_id: int,
        db_session: AsyncSession,
    ) -> list[ItemModel]:
        """Get result of query based on the provided item."""
        return await self.select_item(item, person_id, db_session)

    @post(
        "/{item:str}/{person_id:int}",
        guards=[role_guard],
        opt={"role": Roles.user.value},
    )
    async def post_item(
        self,
        item: ItemCategory,
        person_id: int,
        data: ItemModel,
        db_session: AsyncSession,
    ) -> None:
        """Insert or replaces a record in the specified table with the given item ID."""
        json_dict = data.item.model_dump(
            exclude_none=True,
            exclude={"created_at", "updated_at", "item"},
        )
        json_dict["person_id"] = person_id
        table = ItemsController.tables[item]
        # Проверяем, есть ли ключ "id" в словаре json_dict
        if item_id := json_dict.pop("id", None):
            # Если есть, создаем запрос на обновление записи с указанным id
            stmt = table.update().where(table.c.id == item_id).values(json_dict)
        else:
            # Если нет, создаем запрос на вставку новой записи
            stmt = table.insert().values(json_dict)
        await db_session.execute(stmt)

    @delete(
        "/{item:str}/{item_id:int}",
        guards=[role_guard],
        opt={"role": Roles.user.value},
    )
    async def delete_item(
        self,
        item: ItemCategory,
        item_id: int,
        db_session: AsyncSession,
    ) -> None:
        """Delete an item from the database with item name and item ID."""
        table = ItemsController.tables[item]
        await db_session.execute(
            table.delete().where(table.c.id == item_id),
        )
