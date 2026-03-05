from typing import TYPE_CHECKING

import pytest_asyncio
from litestar.exceptions import InternalServerException
from litestar.testing import AsyncTestClient

from app import app
from app.structures.models import AuthResponse

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from litestar import Litestar

app.debug = True
app.openapi_config = None


@pytest_asyncio.fixture(scope="function")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    """Test client."""
    async with AsyncTestClient(app=app) as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def test_auth_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    """Test client."""
    async with AsyncTestClient(app=app) as client:
        response = await client.post(
            "/routes/auth/login",
            json={
                "username": "",
                "password": "",
            },
        )
        resp = response.json()
        auth = AuthResponse(**resp)
        if auth.message == "success" and auth.access_token and auth.refresh_token:
            client.headers = {"Authorization": auth.access_token}
            yield client
        else:
            raise InternalServerException
