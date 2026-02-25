import pytest
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from litestar.testing import AsyncTestClient

from app.classes.classes import Tokens


@pytest.mark.asyncio
async def test_login(test_client: AsyncTestClient[Litestar]) -> None:
    response = await test_client.post(
        "/routes/auth/login",
        json={
            "username": "",
            "password": "",
        },
    )
    assert response.status_code == HTTP_201_CREATED
    resp = response.json()
    assert resp["message"] == "success"
    assert "Bearer" in resp["access_token"]
    assert "Bearer" in resp["refresh_token"]


@pytest.mark.asyncio
async def test_update(test_client: AsyncTestClient[Litestar]) -> None:
    response = await test_client.post(
        "/routes/auth/update",
        json={
            "username": "",
            "password": "",
            "new_pswd": "",
        },
    )
    assert response.status_code == HTTP_201_CREATED
    resp = response.json()
    assert resp["message"] == "updated"


@pytest.mark.asyncio
async def test_logout(
    test_client: AsyncTestClient[Litestar], test_token: Tokens,
) -> None:
    response = await test_client.post(
        "/routes/auth/logout",
        headers={"Authorization": test_token.access_token},
        json={"refresh_token": test_token.refresh_token},
    )
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.asyncio
async def test_refresh(
    test_client: AsyncTestClient[Litestar],
    test_token: Tokens,
) -> None:
    response = await test_client.post(
        "/routes/auth/refresh",
        headers={"Authorization": test_token.access_token},
        json={"refresh_token": test_token.refresh_token},
    )
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.asyncio
async def test_session(
    test_client: AsyncTestClient[Litestar],
    test_token: Tokens,
) -> None:
    response = await test_client.get(
        "/routes/auth/session",
        headers={"Authorization": test_token.access_token},
    )
    assert response.status_code == HTTP_200_OK
