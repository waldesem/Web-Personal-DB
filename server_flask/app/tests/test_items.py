from unittest.mock import Mock

import pytest 
from flask.testing import FlaskClient


@pytest.fixture
def mock_db_session(monkeypatch):
    # Создаем моки методов execute и commit
    session_mock = Mock()
    
    def fake_execute(*args, **kwargs):
        pass  # Ничего не делаем, блокируем реальный вызов метода
    
    def fake_commit():
        pass  # Блокируем реальный метод commit
    
    # Подменяем реальные методы на наши заглушки
    monkeypatch.setattr('db.session', session_mock)
    monkeypatch.setattr(session_mock, 'execute', fake_execute)
    monkeypatch.setattr(session_mock, 'commit', fake_commit)


@pytest.mark.parametrize("item, person_id", [()])
def test_get_item(client: FlaskClient, item, person_id):
    response = client.get(f"/routes/{item}/{person_id}")

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.headers["Content-Type"] == "application/json"

    # Проверяем, что метод GET работает
    methods = ["POST", "PUT", "DELETE", "PATCH"]
    for method in methods:
        response = getattr(client, method.lower())(f"/routes/{item}/{person_id}")
        if method != "GET":
            assert response.status_code in [405, 404]  # Method Not Allowed

    json_data = None
    if response.content_length > 1000:
        assert response.headers["Content-Encoding"] == "deflate"
        decompressed_content = zlib.decompress(
            response.get_data(), zlib.MAX_WBITS | 32
        )
        json_data = json.loads(decompressed_content.decode("utf-8"))
    else:
        json_data = response.get_json())

    assert isinstance(json_data, list)

    
@pytest.mark.parametrize("item, person_id", [()])
def test_delete_item(mock_db_session, client: FlaskClient, item, person_id):
    response = client.delete(f"/routes/{item}/{person_id}")

    assert response.status_code == 201
    assert response.mimetype == "application/json"
    assert response.headers["Content-Type"] == "application/json"

    # Проверяем, что метод GET работает
    methods = ["POST", "PUT", "GET", "PATCH"]
    for method in methods:
        response = getattr(client, method.lower())(f"/routes/{item}/{person_id}")
        if method != "DELETE":
            assert response.status_code in [405, 404]  # Method Not Allowed
    
    json_data = response.get_json())

    assert "message" in json_data


@pytest.mark.parametrize("item, person_id", [()])
def test_delete_item(mock_db_session, client: FlaskClient, item, person_id):
    response = client.post(f"/routes/{item}/{person_id}")

    assert response.status_code == 201
    assert response.mimetype == "application/json"
    assert response.headers["Content-Type"] == "application/json"

    # Проверяем, что метод GET работает
    methods = ["DELETE", "PUT", "GET", "PATCH"]
    for method in methods:
        response = getattr(client, method.lower())(f"/routes/{item}/{person_id}")
        if method != "POST":
            assert response.status_code in [405, 404]  # Method Not Allowed
    
    json_data = response.get_json())

    assert "message" in json_data
