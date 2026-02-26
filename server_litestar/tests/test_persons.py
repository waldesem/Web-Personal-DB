import json
from pathlib import Path

import pytest
from faker import Faker
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED
from litestar.testing import AsyncTestClient

from app.classes.classes import ItemCategory

fake = Faker("ru-RU")

TEST_DIR = ""


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "person_id",
    list(range(len(ItemCategory))),
)
async def test_get_person(
    test_auth_client: AsyncTestClient[Litestar],
    person_id: int,
) -> None:
    resp = await test_auth_client.get(
        f"/routes/persons/{person_id}",
    )
    assert resp.status_code == HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        {
            "surname": fake.last_name_female(),
            "firstname": fake.first_name_female(),
            "patronymic": fake.middle_name_female() if i != 0 else None,
            "birthday": fake.date(),
            "birthplace": fake.city() if i == 0 else None,
            "citizenship": fake.country() if i == 0 else None,
            "dual": fake.country() if i != 0 else None,
            "snils": fake.snils() if i != 0 else None,
            "inn": fake.individuals_inn() if i == 0 else None,
            "marital": fake.sentence(2) if i == 0 else None,
            "addition": fake.sentence(5) if i != 0 else None,
        }
        for i in range(len(ItemCategory))
    ],
)
async def test_post_person(
    test_auth_client: AsyncTestClient[Litestar],
    data: dict,
) -> None:
    resp = await test_auth_client.post(
        "/routes/persons/",
        json=data,
    )
    assert resp.status_code == HTTP_201_CREATED


@pytest.mark.asyncio
@pytest.mark.parametrize("file", [list(Path(TEST_DIR).glob("*.json"))])
async def test_post_json(
    test_auth_client: AsyncTestClient[Litestar],
    file: Path,
) -> None:
    with file.open(encoding="utf-8") as f:
        anketa = json.loads(f.readline())
        resp = await test_auth_client.post(
            "/routes/persons/json",
            json=anketa,
        )
        assert resp.status_code == HTTP_201_CREATED
