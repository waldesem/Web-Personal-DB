import json
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
import pytest_asyncio
from litestar.exceptions import InternalServerException
from litestar.testing import AsyncTestClient

from app import app

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from litestar import Litestar

app.debug = True


@pytest_asyncio.fixture(scope="session")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app) as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def test_token(test_client: AsyncTestClient[Litestar]) -> dict:
    response = await test_client.post(
        "/routes/auth/login",
        json={
            "username": "vsemenenko",
            "password": "Truxan0va",
        },
    )
    resp = response.json()
    if resp.pop("message") == "success":
        return resp
    raise InternalServerException


@pytest.fixture
def test_json(file: str) -> dict:
    with Path(file).open(encoding="utf-8") as f:
        return json.loads(f.readline())
