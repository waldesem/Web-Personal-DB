import zlib
from flask import json
from flask.testing import FlaskClient

def test_get_index(client: FlaskClient):
    response = client.get("/routes/candidates?page=1&per_page=10&search=")

    assert response.status_code == 200
    assert response.mimetype == "application/json"
    assert response.headers["Content-Type"] == "application/json"

    # Проверяем, что метод GET работает
    methods = ["POST", "PUT", "DELETE", "PATCH"]
    for method in methods:
        response = getattr(client, method.lower())("/")
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
        if response.content_length > 0:
            json_data = json.loads(response.get_data().decode("utf-8"))
        else:
            json_data = []
        
    assert isinstance(json_data, list)

    for item in json_data:
        assert "id" in item
        assert "surname" in item
        assert "firstname" in item
        assert "patronymic" in item
        assert "birthday" in item
        assert "created" in item
        assert "editable" in item 
        assert "total" in item
        assert isinstance(item["total"], int)
