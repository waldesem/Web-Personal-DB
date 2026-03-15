import pytest
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from litestar.testing import AsyncTestClient


@pytest.mark.asyncio
async def test_relogin(
    test_client: AsyncTestClient[Litestar],
) -> None:
    response = await test_client.post(
        "/routes/auth/update",
        json={
            "username": "",
            "password": "",
            "new_pswd": "",
        },
    )
    resp = response.json()
    assert resp.pop("message") == "updated"
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.asyncio
async def test_logout(
    test_client: AsyncTestClient[Litestar],
) -> None:
    response = await test_client.post(
        "/routes/auth/logout",
        json={
            "refresh_token": "refresh_token",
            "access_token": "access_token",
        },
    )
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.asyncio
async def test_refresh(
    test_auth_client: AsyncTestClient[Litestar],
) -> None:
    response = await test_auth_client.get(
        "/routes/auth/refresh",
    )
    assert "token"in response.json()
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.asyncio
async def test_session(
    test_auth_client: AsyncTestClient[Litestar],
) -> None:
    response = await test_auth_client.get(
        "/routes/auth/session",
    )
    assert response.status_code == HTTP_200_OK
