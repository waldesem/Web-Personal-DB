import pytest
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "person_id", [(1), (2)],
    )
async def test_get_person(
    test_client: AsyncTestClient[Litestar], test_token: dict, person_id: int,
) -> None:
    resp = await test_client.get(
        f"/routes/persons/{person_id}",
        headers={"Authorization": test_token["access_token"]},
    )
    assert resp.status_code == HTTP_200_OK
