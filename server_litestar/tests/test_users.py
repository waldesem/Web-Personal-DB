import pytest
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient


@pytest.mark.asyncio
async def test_get_users(
    test_client: AsyncTestClient[Litestar], test_token: dict,
) -> None:
    resp = await test_client.get(
        "/routes/users",
        headers={"Authorization": test_token["access_token"]},
    )
    assert resp.status_code == HTTP_200_OK
