import random

import pytest
from faker import Faker
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from litestar.testing import AsyncTestClient

from app.classes.classes import Roles, Tokens

INTEG = 5

fake = Faker("ru-RU")

@pytest.mark.asyncio
async def test_get_users(
    test_client: AsyncTestClient[Litestar],
    test_token: Tokens,
) -> None:
    resp = await test_client.get(
        "/routes/users",
        headers={"Authorization": test_token.access_token},
    )
    assert resp.status_code == HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        (
            {
                "username": fake.user_name(),
                "fullname": fake.name(),
                "email": fake.email(),
            }
            for _ in range(INTEG)
        ),
    ],
)
async def test_post_user(
    test_client: AsyncTestClient[Litestar],
    test_token: Tokens,
    data: dict,
) -> None:
    resp = await test_client.post(
        "/routes/users/",
        headers={"Authorization": test_token.access_token},
        json=data,
    )
    assert resp.status_code == HTTP_201_CREATED


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("user_id", "data"),
    [
        (random.randint(2, INTEG), item)  # noqa: S311
        for item in ["reset", "block", "delete"] + [role.value for role in Roles]
    ],
)
async def test_user_action(
    test_client: AsyncTestClient[Litestar],
    test_token: Tokens,
    user_id: int,
    data: dict,
) -> None:
    resp = await test_client.post(
        f"/routes/users/{user_id}",
        headers={"Authorization": test_token.access_token},
        json=data,
    )
    assert resp.status_code == HTTP_201_CREATED
