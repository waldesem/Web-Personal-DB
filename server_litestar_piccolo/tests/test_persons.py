import json
from pathlib import Path

import pytest
from faker import Faker
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from litestar.testing import AsyncTestClient

fake = Faker("ru-RU")

TEST_DIR = "/home/semenenko/MyProjects/XData"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "person_id",
    [1],
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
            "surname": fake.name_male(),
            "firstname": fake.first_name_male(),
            "patronymic": fake.middle_name_male(),
            "birthday": "2000-01-01",
            "birthplace": fake.city() if i == 0 else None,
            "citizenship": fake.country() if i == 0 else None,
            "dual": fake.country() if i != 0 else None,
            "snils": fake.snils() if i != 0 else None,
            "inn": fake.individuals_inn(),
            "marital": fake.sentence(2) if i == 0 else None,
            "addition": fake.sentence(5) if i != 0 else None,
        }
        for i in range(5)
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
@pytest.mark.parametrize(
    ("person_id", "data"),
    [
        (
            1,
            {
                "surname": fake.last_name_male(),
                "firstname": fake.first_name_male(),
                "patronymic": fake.middle_name_male(),
                "birthday": "2000-01-01",
                "birthplace": fake.city(),
                "citizenship": fake.country(),
                "dual": fake.country(),
                "marital": fake.sentence(2),
                "addition": fake.sentence(5),
            },
        ),
    ],
)
async def test_patch_person(
    test_auth_client: AsyncTestClient[Litestar],
    person_id: int,
    data: dict,
) -> None:
    resp = await test_auth_client.patch(
        f"/routes/persons/{person_id}",
        json=data,
    )
    assert resp.status_code == HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "person_id",
    [2],
)
async def test_delete_person(
    test_auth_client: AsyncTestClient[Litestar],
    person_id: int,
) -> None:
    resp = await test_auth_client.delete(
        f"/routes/persons/{person_id}",
    )
    assert resp.status_code == HTTP_204_NO_CONTENT


@pytest.mark.asyncio
@pytest.mark.parametrize("file", list(Path(TEST_DIR).glob("*.json")))
async def test_post_json(
    test_auth_client: AsyncTestClient[Litestar],
    file: Path,
) -> None:
    with file.open(encoding="utf-8") as f:
        anketa = json.loads(f.readline())
        resp = await test_auth_client.post(
            "/routes/json",
            json=anketa,
        )
        assert resp.status_code == HTTP_201_CREATED


@pytest.mark.asyncio
@pytest.mark.parametrize("person_id", [2])
async def test_switch_user(
    test_auth_client: AsyncTestClient[Litestar],
    person_id: int,
) -> None:
    resp = await test_auth_client.get(
        f"/routes/persons/status/{person_id}",
    )
    assert resp.status_code == HTTP_200_OK
