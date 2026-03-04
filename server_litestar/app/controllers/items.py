"""Items routes."""

from typing import TYPE_CHECKING

from litestar import Controller, delete, get, patch, post
from pydantic import TypeAdapter
from sqlalchemy import label, literal, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.classes.classes import ItemCategory, Roles
from app.depends.auth import role_guard
from app.models.models import ItemModel, ItemsModels
from app.tables.tables import tables

if TYPE_CHECKING:
    from collections.abc import Sequence

ta = TypeAdapter(list[ItemModel])


class ItemsController(Controller):
    """Items controller."""

    path = "/items"

    @staticmethod
    async def select_item(
        item: ItemCategory,
        person_id: int,
        db_session: AsyncSession,
    ) -> Sequence:
        """Retrieve an item from the database based on the provided item."""
        table = tables[item]
        stmt = (
            select(table, label("item", literal(item)))
            .filter(table.c.person_id == person_id)
            .order_by(table.c.id.desc())
        )
        return (await db_session.execute(stmt)).all()

    @get("/{person_id:int}")
    async def get_items(
        self,
        person_id: int,
        db_session: AsyncSession,
    ) -> ItemsModels:
        """Retrieve an all items from the database."""
        return ItemsModels.model_validate(
            {
                item.value: await self.select_item(item.value, person_id, db_session)
                for item in ItemCategory
            },
            from_attributes=True,
        )

    @get("/{item:str}/{person_id:int}")
    async def get_item(
        self,
        item: ItemCategory,
        person_id: int,
        db_session: AsyncSession,
    ) -> list[ItemModel]:
        """Get result of query based on the provided item."""
        return ta.validate_python(
            await self.select_item(item, person_id, db_session),
            from_attributes=True,
        )

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
        """Insert a record in the specified table."""
        json_dict = data.model_dump(
            exclude={"created_at", "updated_at", "item"},
        ) | {"person_id": person_id}
        table = tables[item]
        stmt = table.insert().values(json_dict)
        await db_session.execute(stmt)

    @patch(
        "/{item:str}/{person_id:int}",
        guards=[role_guard],
        opt={"role": Roles.user.value},
    )
    async def patch_item(
        self,
        item: ItemCategory,
        person_id: int,
        data: ItemModel,
        db_session: AsyncSession,
    ) -> None:
        """Replace a record in the specified table."""
        json_dict = data.model_dump(
            exclude={"created_at", "updated_at", "item"},
        ) | {"person_id": person_id}
        table = tables[item]
        stmt = table.update().where(table.c.id == json_dict["id"]).values(json_dict)
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
        table = tables[item]
        await db_session.execute(
            table.delete().where(table.c.id == item_id),
        )
