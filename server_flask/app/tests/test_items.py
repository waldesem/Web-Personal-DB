from unittest.mock import Mock
import zlib

import pytest

from flask import json
from flask.testing import FlaskClient


params = [
    (param, 9)
    for param in [
        "addresses",
        "affilations",
        "checks",
        "contacts",
        "documents",
        "educations",
        "inquiries",
        "investigations",
        "previous",
        "poligrafs",
        "staffs",
        "workplaces",
    ]
]
print(params)


@pytest.fixture
def mock_db_session(monkeypatch):
    # Создаем моки методов execute и commit
    session_mock = Mock()

    def fake_execute(*args, **kwargs):
        pass  # Ничего не делаем, блокируем реальный вызов метода

    def fake_commit():
        pass  # Блокируем реальный метод commit

    # Подменяем реальные методы на наши заглушки
    monkeypatch.setattr("db.session", session_mock)
    monkeypatch.setattr(session_mock, "execute", fake_execute)
    monkeypatch.setattr(session_mock, "commit", fake_commit)


@pytest.mark.parametrize("item, person_id", params)
def test_get_item(client: FlaskClient, item, person_id):
    response = client.get(f"/routes/items/{item}/{person_id}")

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.headers["Content-Type"] == "application/json"

    json_data = None
    if response.headers.get("Content-Encoding") == "deflate":
        decompressed_content = zlib.decompress(response.get_data(), zlib.MAX_WBITS | 32)
        json_data = json.loads(decompressed_content.decode("utf-8"))
    else:
        json_data = response.get_json()

    assert isinstance(json_data, list)


@pytest.mark.parametrize("item, person_id", params)
def test_delete_item(mock_db_session, client: FlaskClient, item, person_id):
    response = client.delete(f"/routes/items/{item}/{person_id}")

    assert response.status_code == 201
    assert response.mimetype == "application/json"
    assert response.headers["Content-Type"] == "application/json"

    assert mock_db_session == None

    json_data = response.get_json()

    assert "message" in json_data


@pytest.mark.parametrize("item, person_id", params)
def test_post_item(mock_db_session, client: FlaskClient, item, person_id):
    response = client.post(f"/routes/{item}/items/{person_id}")

    assert response.status_code == 201
    assert response.mimetype == "application/json"
    assert response.headers["Content-Type"] == "application/json"

    assert mock_db_session == None

    json_data = response.get_json()

    assert "message" in json_data
