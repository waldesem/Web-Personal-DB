from datetime import datetime

from flask import jsonify, request
from flask.views import MethodView
from werkzeug.security import check_password_hash, generate_password_hash

from ..tools.depends import create_token
from ..tools.queries import execute, select_single
from . import bp


class LoginView(MethodView):
    """Login view"""

    def post(self):
        """
        Post method for the given API endpoint.
        """
        json_data = request.get_json()
        user = select_single(
            "SELECT * FROM users WHERE username = ?", (json_data.get("username"),)
        )
        if user and not user["blocked"] and not user["deleted"]:
            if check_password_hash(user["password"], json_data["password"]):
                delta_change = datetime.now() - datetime.fromisoformat(
                    user["pswd_create"]
                )
                if not user["change_pswd"] and delta_change.days < 365:
                    execute(
                        "UPDATE users SET last_login = ?, attempt = ? WHERE id = ?",
                        (datetime.now(), 0, user["id"]),
                    )
                    return jsonify(
                        {
                            "user_token": create_token(
                                user["id"],
                                user["fullname"],
                                user["username"],
                                user["region"],
                                user["has_admin"],
                            ),
                        }
                    ), 200
                return "", 205
            else:
                if user["attempt"] < 5:
                    execute(
                        "UPDATE users SET attempt = ? WHERE id = ?",
                        (user["attempt"] + 1, user["id"]),
                    )
                else:
                    execute(
                        "UPDATE users SET blocked = ? WHERE id = ?",
                        (True, user["id"]),
                    )
        return "", 204

    def patch(self):
        """
        Patch method for updating user password.
        """
        json_data = request.get_json()
        user = select_single(
            "SELECT * FROM users WHERE username = ?", (json_data["username"],)
        )
        if (
            user
            and not user["blocked"]
            and not user["deleted"]
            and check_password_hash(user["password"], json_data["password"])
        ):
            execute(
                "UPDATE users SET password = ?, change_pswd = ? attempt = ? WHERE id = ?",
                (
                    generate_password_hash(json_data["new_pswd"]),
                    False,
                    0,
                    user["id"],
                ),
            )
            return "", 201
        return "", 204


bp.add_url_rule("/login", view_func=LoginView.as_view("login"))
