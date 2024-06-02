import sqlite3
from datetime import datetime

from flask import abort, jsonify, request
from flask.views import MethodView
from werkzeug.security import check_password_hash, generate_password_hash

from config import Config
from . import bp
from ..utils.dependencies import Token, create_token, jwt_required


class AuthView(MethodView):
    """Login view"""

    decorators = [jwt_required()]

    def get(self):
        """
        Retrieves the current authenticated user from the database.
        """
        if (
            Token.current_user
            and not Token.current_user['blocked']
            and not Token.current_user['deleted']
        ):
            with sqlite3.connect(Config.DATABASE_URI) as conn:
                cursor = conn.cursor()
                Token.current_user['last_login'] = datetime.now()
                user_dict = Token.current_user
                query = cursor.execute(
                    "SELECT * FROM user_roles LEFT JOIN roles ON user_roles.role_id = roles.id WHERE user_id = ?",
                    (Token.current_user["id"],),
                )
                user_dict["roles"] = [r["role"] for r in query.fetchall()]
                return jsonify(user_dict)
        return abort(404)


bp.add_url_rule("/auth", view_func=AuthView.as_view("auth"))


class LoginView(MethodView):
    """Login view"""

    def post(self):
        """
        Post method for the given API endpoint.
        """
        json_data = request.get_json()
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            query = cursor.execute(
                "SELECT * FROM users WHERE username = ?",
                (json_data["username"],),
            )
            user = query.fetchone()
            if user and not user['blocked'] and not user['deleted']:
                if check_password_hash(user['password'], json_data["password"]):
                    delta_change = datetime.now() - user['pswd_create']
                    if user['pswd_change'] and delta_change.days < 365:
                        cursor.execute(
                            "UPDATE users SET last_login = ? attempt = 0 WHERE id = ?",
                            (datetime.now(), user['id']),
                        )
                        conn.commit()
                        return jsonify({
                            "message": "Authenticated",
                            "user_token": create_token(str(user.id)),
                        }), 201
                    return jsonify({"message": "Overdue"}), 201
                else:
                    if user['attempt'] < 9:
                        cursor.execute(
                            "UPDATE users SET attempt = ? WHERE id = ?",
                            (user['attempt'] + 1, user['id']),
                        )
                    else:
                        cursor.execute(
                            "UPDATE users SET blocked = ? WHERE id = ?",
                            (True, user['id']),
                        )
                    conn.commit()
            return jsonify({"message": "Denied"}), 201

    def patch(self):
        """
        Patch method for updating user password.
        """
        json_data = request.get_json()
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            query = cursor.execute(
                "SELECT * FROM users WHERE username = ?", (json_data["username"],)
            )
            user = query.fetchone()
            if (
                user
                and not user['blocked']
                and not user['deleted']
                and check_password_hash(user['password'], json_data["password"])
            ):
                cursor.execute(
                    "UPDATE users SET password = ?, pswd_change = ? WHERE id = ?",
                    (
                        generate_password_hash(
                            json_data["new_pswd"],
                            method="scrypt",
                            salt_length=16,
                        ),
                        datetime.now(),
                        user['id'],
                    ),
                )
                conn.commit()
                return jsonify({"message": "Changed"})
        return jsonify({"message": "Denied"})


bp.add_url_rule("/login", view_func=LoginView.as_view("login"))
