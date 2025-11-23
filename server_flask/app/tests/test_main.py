from pathlib import Path

from flask.testing import FlaskClient


def test_get_main(client: FlaskClient):
    response = client.get("/")

    # Проверяем статус код и тип контента
    assert response.status_code == 200
    assert response.content_type == "text/html; charset=utf-8"
    assert "text/html" in response.headers["Content-Type"]
    assert response.headers["Content-Encoding"] == "deflate"

    # Проверяем, что метод GET работает
    methods = ["POST", "PUT", "DELETE", "PATCH"]
    for method in methods:
        response = getattr(client, method.lower())("/")
        if method != "GET":
            assert response.status_code in [405, 404]  # Method Not Allowed

    # # Проверяем, что есть index.html
    app = client.application
    static_folder = Path(app.static_folder)
    index_file = static_folder / "index.html"
    assert index_file.exists()
