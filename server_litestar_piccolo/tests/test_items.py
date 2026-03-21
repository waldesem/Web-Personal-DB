import pytest
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from litestar.testing import AsyncTestClient

from app.classes.classes import ItemCategory


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("item", "person_id"),
    [(item.value, 5) for item in ItemCategory],
)
async def test_get_item(
    test_auth_client: AsyncTestClient[Litestar],
    item: str,
    person_id: int,
) -> None:
    resp = await test_auth_client.get(
        f"/routes/items/{item}/{person_id}",
    )
    assert resp.status_code == HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "person_id",
    [5],
)
async def test_get_items(
    test_auth_client: AsyncTestClient[Litestar],
    person_id: int,
) -> None:
    resp = await test_auth_client.get(
        f"/routes/items/{person_id}",
    )
    assert resp.status_code == HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("person_id", "data"),
    [
        (
            5,
            {
                "item": {
                    "item": "checks",
                    "conclusion": "СОГЛАСОВАНО",
                },
            },
        ),
    ],
)
async def test_post_item(
    test_auth_client: AsyncTestClient[Litestar],
    person_id: int,
    data: dict,
) -> None:
    resp = await test_auth_client.post(
        f"/routes/items/{person_id}",
        json=data,
    )
    assert resp.status_code == HTTP_201_CREATED


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("person_id", "item_id", "data"),
    [
        (
            5,
            1,
            {
                "item": {
                    "item": "checks",
                    "conclusion": "ОТКАЗАНО В СОГЛАСОВАНИИ",
                },
            },
        ),
    ],
)
async def test_patch_item(
    test_auth_client: AsyncTestClient[Litestar],
    person_id: int,
    item_id: int,
    data: dict,
) -> None:
    resp = await test_auth_client.patch(
        f"/routes/items/{person_id}/{item_id}",
        json=data,
    )
    assert resp.status_code == HTTP_200_OK
