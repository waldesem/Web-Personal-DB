import profile
from collections.abc import AsyncIterator

import pytest

from litestar import Litestar, MediaType, get
from litestar.status_codes import HTTP_201_CREATED
from litestar.testing import AsyncTestClient


@pytest.mark.asyncio
async def test_candidates(test_client: AsyncTestClient[Litestar]) -> None:
    response = await test_client.post("/routes/auth/login", json={
        "username": "",
        "password": "",
    })
    assert response.status_code == HTTP_201_CREATED
    resp = response.json()
    assert resp["message"] == "success"
    assert "Bearer" in resp["access_token"]
    assert "Bearer" in resp["refresh_token"]

    resp = await test_client.get(
        "/routes/candidates",
        headers={"Authorization": resp["access_token"]},
        params={
            "page": 1,
            "per_page": 10,
            "search": "",
        },
    )
    assert resp.status_code == 200
