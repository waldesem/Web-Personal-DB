"""Items routes."""

from litestar import Controller, delete, get, patch, post
from piccolo.conf.apps import table_finder
from piccolo.query.functions import Lower
from piccolo.table import Table
from pydantic import TypeAdapter

from app.classes.classes import ItemCategory, Roles
from app.middleware.auth import person_guard, role_guard
from app.models.items import ItemModelIn, ItemsOutModels, ItemTypeOut

ta = TypeAdapter(list[ItemTypeOut])


class ItemsController(Controller):
    """Items controller."""

    path = "/items"

    @classmethod
    async def _get_table(cls, item: str) -> type[Table]:
        return table_finder(modules=["app.tables.tables"], include_tags=[item])[0]

    @classmethod
    async def select_item(
        cls,
        item: str,
        person_id: int,
    ) -> list[dict]:
        """Select rows from the database based on the provided item and person ID.

        Args:
            item: ItemCategory.
            person_id: Person ID.

        Returns:
            Sequence of rows from the database.

        """
        table = await cls._get_table(item)
        return (
            await table.select(table.all_columns(), Lower(item, alias="item"))  # ty:ignore[invalid-argument-type]
            .where(getattr(table, "person_id") == person_id)
            .order_by(getattr(table, "id"), ascending=False)
        )

    @get("/{person_id:int}")
    async def get_items(
        self,
        person_id: int,
    ) -> ItemsOutModels:
        """Get all items for a person.

        Args:
            person_id: Person ID.

        Returns:
            Response with status code 200 and serialized ItemsOutModels.

        """
        selection = {
            item.value: await self.select_item(item.value, person_id)
            for item in ItemCategory
        }
        return ItemsOutModels.model_validate(selection, from_attributes=True)

    @get("/{item:str}/{person_id:int}")
    async def get_item(
        self,
        item: ItemCategory,
        person_id: int,
    ) -> list[ItemTypeOut]:
        """Get an item for a person.

        Args:
            item: ItemCategory.
            person_id: Person ID.

        Returns:
            Response with status code 200 and serialized list of ItemTypeOut.

        """
        selection = await self.select_item(item, person_id)
        return ta.validate_python(selection, from_attributes=True)

    @post(
        "/{person_id:int}",
        guards=[role_guard, person_guard],
        opt={"role": Roles.user.value},
    )
    async def post_item(
        self,
        person_id: int,
        data: ItemModelIn,
    ) -> None:
        """Add a new item to the database.

        Args:
            person_id: Person ID.
            data: ItemModelIn.
            request: Request.

        Returns:
            Response with status code 201.

        """
        json_dict = data.item.model_dump(exclude={"item"}) | {
            "person_id": person_id,
        }
        table = await self._get_table(data.item.item)
        await table.insert(table(json_dict))

    @patch(
        "/{person_id:int}/{item_id:int}",
        guards=[role_guard, person_guard],
        opt={"role": Roles.user.value},
    )
    async def patch_item(
        self,
        person_id: int,
        item_id: int,
        data: ItemModelIn,
    ) -> None:
        """Update an item in the database.

        Args:
            person_id: Person ID.
            item_id: Item ID.
            data: ItemModelIn.
            request: Request.

        Returns:
            Response with status code 201.

        """
        json_dict = data.item.model_dump(exclude={"item"}) | {"person_id": person_id}
        table = await self._get_table(data.item.item)
        await table.update(json_dict).where(getattr(table, "id") == item_id)

    @delete(
        "/{item:str}/{person_id:int}/{item_id:int}",
        guards=[role_guard, person_guard],
        opt={"role": Roles.user.value},
    )
    async def delete_item(
        self,
        item: ItemCategory,
        item_id: int,
    ) -> None:
        """Delete an item from the database.

        Args:
            item: ItemCategory.
            person_id: Person ID.
            item_id: Item ID.
            request: Request.

        Returns:
            Response with status code 204.

        """
        table = await self._get_table(item)
        await table.delete().where(getattr(table, "id") == item_id)
