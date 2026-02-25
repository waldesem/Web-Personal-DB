import pytest
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from litestar.testing import AsyncTestClient

from app.classes.classes import Tokens


@pytest.mark.asyncio
async def test_candidates(
    test_client: AsyncTestClient[Litestar], test_token: dict,
) -> None:
    resp = await test_client.get(
        "/routes/candidates",
        headers={"Authorization": test_token["access_token"]},
        params={
            "page": 1,
            "per_page": 10,
            "search": "",
        },
    )
    assert resp.status_code == HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.parametrize("person_id", [(1), (2)])
async def test_switch_user(
    test_client: AsyncTestClient[Litestar],
    test_token: Tokens,
    person_id: int,
) -> None:
    resp = await test_client.patch(
        f"/routes/status/{person_id}",
        json={},
        headers={"Authorization": test_token.access_token},
    )
    assert resp.status_code == HTTP_201_CREATED
