"""Items routes."""

from typing import TYPE_CHECKING

from litestar import Controller, delete, get, patch, post
from pydantic import TypeAdapter
from sqlalchemy import label, literal, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.middleware.auth import role_guard
from app.structures.classes import ItemCategory, Roles
from app.structures.models import ItemModelIn, ItemsOutModels, ItemTypeOut
from app.structures.tables import tables

if TYPE_CHECKING:
    from collections.abc import Sequence

ta = TypeAdapter(list[ItemTypeOut])


class ItemsController(Controller):
    """Items controller."""

    path = "/items"

    @staticmethod
    async def select_item(
        item: ItemCategory,
        person_id: int,
        db_session: AsyncSession,
    ) -> Sequence:
        """Select rows from the database based on the provided item and person ID.

        Args:
            item: ItemCategory.
            person_id: Person ID.
            db_session: AsyncSession.

        Returns:
            Sequence of rows from the database.

        """
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
    ) -> ItemsOutModels:
        """Get all items for a person.

        Args:
            person_id: Person ID.
            db_session: AsyncSession.

        Returns:
            Response with status code 200 and serialized ItemsOutModels.

        """
        return ItemsOutModels.model_validate(
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
    ) -> list[ItemTypeOut]:
        """Get an item for a person.

        Args:
            item: ItemCategory.
            person_id: Person ID.
            db_session: AsyncSession.

        Returns:
            Response with status code 200 and serialized list of ItemTypeOut.

        """
        return ta.validate_python(
            await self.select_item(item, person_id, db_session),
            from_attributes=True,
        )

    @post(
        "/{person_id:int}",
        guards=[role_guard],
        opt={"role": Roles.user.value},
    )
    async def post_item(
        self,
        person_id: int,
        data: ItemModelIn,
        db_session: AsyncSession,
    ) -> None:
        """Add a new item to the database.

        Args:
            person_id: Person ID.
            data: ItemModelIn.
            db_session: AsyncSession.

        Returns:
            Response with status code 201.

        """
        item = data.item.item
        json_dict = data.item.model_dump(exclude={"item"}) | {"person_id": person_id}
        stmt = tables[item].insert().values(json_dict)
        await db_session.execute(stmt)

    @patch(
        "/{person_id:int}/{item_id:int}",
        guards=[role_guard],
        opt={"role": Roles.user.value},
    )
    async def patch_item(
        self,
        person_id: int,
        item_id: int,
        data: ItemModelIn,
        db_session: AsyncSession,
    ) -> None:
        """Update an item in the database.

        Args:
            person_id: Person ID.
            item_id: Item ID.
            data: ItemModelIn.
            db_session: AsyncSession.

        Returns:
            Response with status code 201.

        """
        json_dict = data.item.model_dump() | {"person_id": person_id}
        table = tables[json_dict.pop("item")]
        stmt = table.update().where(table.c.id == item_id).values(json_dict)
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
        """Delete an item from the database.

        Args:
            item: ItemCategory.
            item_id: Item ID.
            db_session: AsyncSession.

        Returns:
            Response with status code 204.

        """
        table = tables[item]
        await db_session.execute(
            table.delete().where(table.c.id == item_id),
        )
