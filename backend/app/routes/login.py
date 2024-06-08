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
        query = "SELECT id, password, last_login, attempt, change_pswd, blocked, deleted, has_admin, region, username, fullname FROM users WHERE username = ? FOR UPDATE"
        user = select_single(query, (json_data.get("username"),))
        if not user or user["blocked"] or user["deleted"]:
            return "", 204
        password = json_data["password"]
        if not check_password_hash(user["password"], password):
            user["attempt"] = min(user["attempt"] + 1, 5)
            if user["attempt"] == 5:
                execute("UPDATE users SET blocked = ? WHERE id = ?", (True, user["id"]))
            return "", 401
        delta_change = datetime.now() - user["last_login"]
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
                },
                200,
            )
        return "", 205

    def patch(self):
        """
        Patch method for updating user password.
        """
        json_data = request.get_json()
        user = select_single(
            "SELECT id, password FROM users WHERE username = %s FOR UPDATE",
            (json_data["username"],),
        )
        if user and not user["blocked"] and not user["deleted"]:
            if check_password_hash(user["password"], json_data["password"]):
                execute(
                    "UPDATE users SET password = %s, change_pswd = FALSE, attempt = 0 WHERE id = %s",
                    (generate_password_hash(json_data["new_pswd"]), user["id"]),
                )
                return "", 201
        return "", 204


bp.add_url_rule("/login", view_func=LoginView.as_view("login"))
