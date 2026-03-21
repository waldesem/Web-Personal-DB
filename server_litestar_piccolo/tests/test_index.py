import pytest
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient


@pytest.mark.asyncio
async def test_candidates(test_auth_client: AsyncTestClient[Litestar]) -> None:
    resp = await test_auth_client.get(
        "/routes/candidates",
        params={
            "last_seen_id": 3,
            "per_page": 2,
            "search": "",
        },
    )
    assert resp.status_code == HTTP_200_OK
