import pytest
from faker import Faker
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from litestar.testing import AsyncTestClient

fake = Faker("ru-RU")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "person_id",
    [(1), (2)],
)
async def test_get_person(
    test_client: AsyncTestClient[Litestar],
    test_token: dict,
    person_id: int,
) -> None:
    resp = await test_client.get(
        f"/routes/persons/{person_id}",
        headers={"Authorization": test_token["access_token"]},
    )
    assert resp.status_code == HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        {
            "surname": fake.last_name_female(),
            "firstname": fake.first_name_female(),
            "patronymic": fake.middle_name_female(),
            "birthday": fake.date(),
            "birthplace": fake.city(),
            "citizenship": fake.country(),
            "dual": fake.country(),
            "snils": fake.snils(),
            "inn": fake.individuals_inn(),
            "marital": fake.sentence(2),
            "destination": fake.sentence(1),
            "addition": fake.sentence(5),
        }
        for _ in range(3)
    ],
)
async def test_post_person(
    test_client: AsyncTestClient[Litestar],
    test_token: dict,
    data: dict,
) -> None:
    resp = await test_client.post(
        "/routes/persons/",
        headers={"Authorization": test_token["access_token"]},
        json=data,
    )
    assert resp.status_code == HTTP_201_CREATED


@pytest.mark.asyncio
@pytest.mark.parametrize("data", [])
async def test_post_json(
    test_client: AsyncTestClient[Litestar],
    test_token: dict,
    data: dict,
) -> None:
    resp = await test_client.post(
        "/routes/persons/json",
        headers={"Authorization": test_token["access_token"]},
        json=data,
    )
    assert resp.status_code == HTTP_200_OK
