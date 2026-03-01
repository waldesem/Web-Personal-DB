from typing import TYPE_CHECKING

import pytest_asyncio
from litestar.exceptions import InternalServerException
from litestar.testing import AsyncTestClient

from app import app
from app.classes.classes import Tokens

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from litestar import Litestar

app.debug = True
app.openapi_config = None


async def create_tokens(test_client: AsyncTestClient[Litestar]) -> Tokens | None:
    """Create tokens for testing."""
    response = await test_client.post(
        "/routes/auth/login",
        json={
            "username": "",
            "password": "",
        },
    )
    resp = response.json()
    if resp and resp.pop("message", None) == "success":
        return Tokens(**resp)
    return None


@pytest_asyncio.fixture(scope="session")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    """Test client."""
    async with AsyncTestClient(app=app) as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def test_auth_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    """Test client."""
    async with AsyncTestClient(app=app) as client:
        if tokens := await create_tokens(client):
            client.headers = {"Authorization": tokens.access_token}
            yield client
        else:
            raise InternalServerException


@pytest_asyncio.fixture(scope="function")
async def test_token() -> Tokens | None:
    """Test token."""
    async with AsyncTestClient(app=app) as client:
        if tokens := await create_tokens(client):
            return tokens
        return None
