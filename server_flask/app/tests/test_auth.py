from flask.testing import FlaskClient

from app.utils.utilities import decode_token


def test_auth(client: FlaskClient):
    response = client.post(
        "/routes/auth/login",
        json={
            "username": "pytest",
            "password": "88888888",
        },
    )

    assert response.content_type == "application/json"
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code in [200, 201]

    json_data = response.get_json()

    if response.status_code == 201:
        print("[DEBUG] Response status - 201")
        assert (
            "message" in json_data
            and "access_token" in json_data
            and "refresh_token" in json_data
        )

        with client.application.app_context():
            assert json_data["message"] == "success"
            assert decode_token(f"Bearer {json_data['access_token']}")["id"] == 16
            assert (
                decode_token(f"Bearer {json_data['refresh_token']}", refresh=True)["id"]
                == 16
            )

            # Проверяем обновление токена
            resp = client.post(
                "/routes/auth/refresh",
                json={"refresh_token": f"Bearer {json_data['refresh_token']}"},
            )

            assert resp.content_type == "application/json"
            assert resp.headers["Content-Type"] == "application/json"
            assert resp.status_code == 201

            j_data = response.get_json()
            assert "message" in j_data
            assert "access_token" in j_data

            assert decode_token(f"Bearer {j_data['access_token']}")["id"] == 16

            # Проверяем выход получение сессии
            r = client.get(
                "/routes/auth/session",
                headers={"Authorization": f"Bearer {json_data['access_token']}"},
            )

            assert r.content_type == "application/json"
            assert r.headers["Content-Type"] == "application/json"
            assert r.status_code == 200

            j_d = r.get_json()
            assert "id" in j_d
            assert "fullname" in j_d
            assert "username" in j_d
            assert "email" in j_d
            assert "role" in j_d

    elif response.status_code == 200:
        print("[DEBUG] Response status - 200")
        assert json_data["message"] == "invalid"

        response = client.post(
            f"/routes/auth/update",
            json={"username": "pytest", "password": "00000000", "new_pswd": "88888888"},
        )

        # Проверяем статус код и тип контента
        assert response.content_type == "application/json"
        assert response.headers["Content-Type"] == "application/json"
        assert response.status_code in [200, 201]

        json_data = response.get_json()
        assert "message" in json_data

        if response.status_code == 200:
            assert json_data["message"] in ["invalid", "denied"]
        else:
            assert json_data["message"] in ["updated", "success"]
