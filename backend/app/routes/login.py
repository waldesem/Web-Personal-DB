from datetime import datetime

from flask import jsonify, request
from flask.views import MethodView
from werkzeug.security import check_password_hash, generate_password_hash

from . import bp
from ..tools.depends import create_token
from ..tools.queries import select_single, execute


class LoginView(MethodView):
    """Login view"""

    @staticmethod
    def select_user(username):
        return select_single(
            "SELECT * FROM users WHERE username = ?", 
            (username,)
        )

    def post(self):
        """
        Post method for the given API endpoint.
        """
        json_data = request.get_json()
        user = self.select_user(json_data["username"])
        if user and not user["blocked"]:
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
                            "message": "Authenticated",
                            "user_token": create_token(
                                user["id"], user["has_admin"]
                            ),
                        }
                    ), 201
                return jsonify({"message": "Overdue"}), 201
            else:
                if user["attempt"] < 9:
                    execute(
                        "UPDATE users SET attempt = ? WHERE id = ?",
                        (user["attempt"] + 1, user["id"]),
                    )
                else:
                    execute(
                        "UPDATE users SET blocked = ? WHERE id = ?",
                        (True, user["id"]),
                    )
        return jsonify({"message": "Denied"}), 204

    def patch(self):
        """
        Patch method for updating user password.
        """
        json_data = request.get_json()
        user = self.select_user(json_data["username"])
        if (
            user
            and not user["blocked"]
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
            return jsonify({"message": "Changed"}), 201
        return jsonify({"message": "Denied"}), 204


bp.add_url_rule("/login", view_func=LoginView.as_view("login"))
