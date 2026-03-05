import pytest
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from litestar.testing import AsyncTestClient

from app.structures.classes import ItemCategory


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("item", "person_id"),
    [(item.value, 1) for item in ItemCategory],
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
    [1],
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
    ("item", "person_id", "data"),
    [
        (
            "staffs",
            1,
            {
                "item": {
                    "position": "Officer",
                    "department": "Investing",
                    "item": "staffs",
                },
            },
        ),
    ],
)
async def test_post_item(
    test_auth_client: AsyncTestClient[Litestar],
    item: str,
    person_id: int,
    data: dict,
) -> None:
    resp = await test_auth_client.patch(
        f"/routes/items/{item}/{person_id}",
        json=data,
    )
    assert resp.status_code == HTTP_201_CREATED
