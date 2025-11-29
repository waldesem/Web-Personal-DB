import zlib

import pytest

from flask import json
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "page, per_page, search", [(1, 10, ""), (2, 10, ""), (1, 10, "test"), (2, 10, "test")]
)
def test_get_index(client: FlaskClient, page, per_page, search):
    response = client.get(
        f"/routes/candidates?page={page}&per_page={per_page}&search={search}"        )

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
