import sqlite3
from datetime import datetime

from flask import jsonify, request
from flask.views import MethodView
from werkzeug.security import check_password_hash, generate_password_hash

from config import Config
from . import bp
from ..utils.dependencies import create_token, select_roles


class LoginView(MethodView):
    """Login view"""

    @staticmethod
    def select_user(username):
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            query = cursor.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            )
            user = query.fetchone()
            if not user:
                return None
            return dict(zip([desc[0] for desc in query.description], user))

    def post(self):
        """
        Post method for the given API endpoint.
        """
        json_data = request.get_json()
        user = self.select_user(json_data["username"])
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            if user and not user["blocked"] and not user["deleted"]:
                if check_password_hash(user["password"], json_data["password"]):
                    delta_change = datetime.now() - datetime.fromisoformat(
                        user["pswd_create"]
                    )
                    if user["pswd_change"] and delta_change.days < 365:
                        cursor.execute(
                            "UPDATE users SET last_login = ?, attempt = ? WHERE id = ?",
                            (datetime.now(), 0, user["id"]),
                        )
                        conn.commit()
                        return jsonify(
                            {
                                "message": "Authenticated",
                                "user_token": create_token(
                                    user["id"], select_roles(user["id"])
                                ),
                            }
                        ), 201
                    return jsonify({"message": "Overdue"}), 201
                else:
                    if user["attempt"] < 9:
                        cursor.execute(
                            "UPDATE users SET attempt = ? WHERE id = ?",
                            (user["attempt"] + 1, user["id"]),
                        )
                        print(user["attempt"] + 1)
                    else:
                        cursor.execute(
                            "UPDATE users SET blocked = ? WHERE id = ?",
                            (True, user["id"]),
                        )
                    conn.commit()
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
            and not user["deleted"]
            and check_password_hash(user["password"], json_data["password"])
        ):
            with sqlite3.connect(Config.DATABASE_URI) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET password = ?, pswd_change = ? WHERE id = ?",
                    (
                        generate_password_hash(
                            json_data["new_pswd"],
                            method="scrypt",
                            salt_length=16,
                        ),
                        datetime.now(),
                        user["id"],
                    ),
                )
                conn.commit()
                return jsonify({"message": "Changed"}), 201
        return jsonify({"message": "Denied"}), 204


bp.add_url_rule("/login", view_func=LoginView.as_view("login"))
