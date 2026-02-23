from typing import TYPE_CHECKING
from collections.abc import AsyncIterator

import pytest_asyncio

from litestar.testing import AsyncTestClient

from app import app

if TYPE_CHECKING:
    from litestar import Litestar

app.debug = True


@pytest_asyncio.fixture(scope="function")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app) as client:
        yield client
