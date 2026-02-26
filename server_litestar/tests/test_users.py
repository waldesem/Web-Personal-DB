import pytest
from faker import Faker
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from litestar.testing import AsyncTestClient

from app.classes.classes import Roles

fake = Faker("ru-RU")

@pytest.mark.asyncio
async def test_get_users(
    test_auth_client: AsyncTestClient[Litestar],
) -> None:
    resp = await test_auth_client.get(
        "/routes/users",
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
            for _ in range(5)
        ),
    ],
)
async def test_post_user(
    test_auth_client: AsyncTestClient[Litestar],
    data: dict,
) -> None:
    resp = await test_auth_client.post(
        "/routes/users/",
        json=data,
    )
    assert resp.status_code == HTTP_201_CREATED


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("user_id", "data"),
    [
        (2, item)
        for item in ["reset", "block", "delete"] + [role.value for role in Roles]
    ],
)
async def test_user_action(
    test_auth_client: AsyncTestClient[Litestar],
    user_id: int,
    data: dict,
) -> None:
    resp = await test_auth_client.post(
        f"/routes/users/{user_id}",
        json=data,
    )
    assert resp.status_code == HTTP_201_CREATED
