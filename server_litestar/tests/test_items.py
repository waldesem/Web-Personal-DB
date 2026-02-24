import pytest
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient
from polyfactory.factories import DataclassFactory

from app.classes.classes import ItemCategory
from app.models.models import ItemModel


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("item", "person_id"),
    [(item.value, 1) for item in ItemCategory],
)
async def test_get_items(
    test_client: AsyncTestClient[Litestar],
    test_token: dict,
    item: str,
    person_id: int,
) -> None:
    resp = await test_client.get(
        f"/routes/items/{item}/{person_id}",
        headers={"Authorization": test_token["access_token"]},
    )
    assert resp.status_code == HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "person_id",
    [(1), (2)],
)
async def test_get_item(
    test_client: AsyncTestClient[Litestar],
    test_token: dict,
    person_id: int,
) -> None:
    resp = await test_client.get(
        f"/routes/items/{person_id}",
        headers={"Authorization": test_token["access_token"]},
    )
    assert resp.status_code == HTTP_200_OK


def data_factory(item: str) -> dict:

    class ItemFactory(DataclassFactory[ItemModel]):
        __model__ = ItemModel

    data = ItemFactory.build()

    return data.model_dump(exclude={"item"})


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("item", "person_id", "data"),
    [(item.value, 1, data_factory(item.value)) for item in ItemCategory],
)
async def test_post_item(
    test_client: AsyncTestClient[Litestar],
    test_token: dict,
    item: str,
    person_id: int,
    data: dict,
) -> None:
    resp = await test_client.post(
        f"/routes/items/{item}/{person_id}",
        headers={"Authorization": test_token["access_token"]},
        json=data,
    )
    assert resp.status_code == HTTP_200_OK
