import pytest
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from litestar.testing import AsyncTestClient


@pytest.mark.asyncio
async def test_candidates(test_auth_client: AsyncTestClient[Litestar]) -> None:
    resp = await test_auth_client.get(
        "/routes/candidates",
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
    test_auth_client: AsyncTestClient[Litestar],
    person_id: int,
) -> None:
    resp = await test_auth_client.patch(
        f"/routes/status/{person_id}",
        json={},
    )
    assert resp.status_code == HTTP_201_CREATED
