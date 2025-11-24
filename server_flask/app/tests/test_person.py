from unittest.mock import Mock
import zlib

from flask import json
import pytest
from flask.testing import FlaskClient


@pytest.fixture
def mock_db_delete(monkeypatch):
    # Создаем моки методов execute и commit
    session_mock = Mock()

    def fake_delete(*args, **kwargs):
        pass  # Ничего не делаем, блокируем реальный вызов метода

    def fake_commit():
        pass  # Блокируем реальный метод commit

    # Подменяем реальные методы на наши заглушки
    monkeypatch.setattr("db.session", session_mock)
    monkeypatch.setattr(session_mock, "delete", fake_delete)
    monkeypatch.setattr(session_mock, "commit", fake_commit)


@pytest.fixture
def mock_db_post(monkeypatch):

    def fake_upload(*args, **kwargs):
        return 1, True

    # Подменяем реальные методы на заглушки
    monkeypatch.setattr("upload_resume", fake_upload)


def test_get_item(client: FlaskClient):
    response = client.get(f"/routes/persons/{1}")

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.headers["Content-Type"] == "application/json"

    json_data = None
    if response.content_length > 1000:
        assert response.headers["Content-Encoding"] == "deflate"
        decompressed_content = zlib.decompress(response.get_data(), zlib.MAX_WBITS | 32)
        json_data = json.loads(decompressed_content.decode("utf-8"))
    else:
        json_data = response.get_json()

    assert isinstance(json_data, dict)


def test_delete_item(mock_db_delete, client: FlaskClient):
    response = client.delete(f"/routes/persons/{1}")

    assert response.status_code == 201
    assert response.mimetype == "application/json"
    assert response.headers["Content-Type"] == "application/json"

    assert mock_db_delete == None

    json_data = response.get_json()

    assert "message" in json_data


def test_post_item(mock_db_session, client: FlaskClient):
    response = client.post(f"/routes/persons/{1}")

    assert response.status_code == 201
    assert response.mimetype == "application/json"
    assert response.headers["Content-Type"] == "application/json"

    assert mock_db_session == None

    json_data = response.get_json()

    assert "message" in json_data
