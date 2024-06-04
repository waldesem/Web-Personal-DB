from datetime import datetime
import sqlite3
from flask import abort, jsonify, request
from flask.views import MethodView
from werkzeug.security import generate_password_hash

from config import Config
from . import bp
from ..utils.dependencies import Token, roles_required
from ..models.classes import Roles


@roles_required(Roles.admin.value)
@bp.get("/users")
def get_users():
    """
    Endpoint to handle requests for getting users.
    """
    search_data = request.args.get("search")
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        cursor = conn.cursor()
        query = cursor.execute(
            "SELECT * FROM users ORDER BY id DESC",
        )
        if search_data:
            query = cursor.execute(
                "SELECT * FROM users WHERE username LIKE '%{}%' ORDER BY id DESC".format(
                    search_data
                )
            )
        col_names = [i[0] for i in query.description]
        return jsonify([zip(col_names, q) for q in query.fetchall()])


class UserView(MethodView):
    decorators = [roles_required(Roles.admin.value)]

    @staticmethod
    def select_user_by_id(user_id):
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            query = cursor.execute(
                "SELECT * FROM users WHERE id = ?", (user_id,)
            )
            col_names = [i[0] for i in query.description]
            return zip(col_names, query.fetchone())
        
    def get(self, user_id):
        """
        Retrieves a user based on the specified action and user ID.
        """
        action_data = request.args.get("action")
        user = self.select_user_by_id(user_id)
        if not user:
            return abort(404)
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            if action_data != "view":
                match action_data:
                    case "block":
                        if user['username'] != Token.current_user['username']:
                            cursor.execute(
                                "UPDATE users SET blocked = ? WHERE id = ?",
                                (not user['blocked'], user_id),
                            )
                    case "drop":
                        cursor.execute(
                            "UPDATE users SET password = ?, attempt = ?, pswd_change = ? WHERE id = ?",
                            (
                                generate_password_hash(
                                    Config.DEFAULT_PASSWORD,
                                    method="scrypt",
                                    salt_length=16,
                                ),
                                0,
                                None,
                                user_id,
                            ),
                        )
                    case "region":
                        cursor.execute(
                            "UPDATE users SET region_id = ? WHERE id = ?",
                            (action_data, user_id),
                        )
                    case _:
                        return abort, 404
                conn.commit()
            return jsonify(self.select_user_by_id(user_id))

    def post(self):
        """
        Creates a new user based on the provided JSON data.
        """
        json_data = request.get_json()
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            query = cursor.execute(
                "SELECT * FROM users WHERE username = ?", (json_data.get("username"),)
            )
            user = query.fetchone()
            if user:
                return {"message": "Denied"}, 403
            cursor.execute(
                "INSERT INTO users (fullname, username, email, password, email, pswd_create, pswd_change, last_login, blocked, deleted, attempt, created, updated, region_id) VALUES (?, ?, ?, ?)",
                (
                    json_data.get("fullname"),
                    json_data.get("username"),
                    json_data.get("email"),
                    generate_password_hash(
                        Config.DEFAULT_PASSWORD, method="scrypt", salt_length=16
                    ),
                    datetime.now(),
                    None,
                    None,
                    0,
                    0,
                    0,
                    datetime.now(),
                    datetime.now(),
                    json_data.get("region_id"),

                ),
            )
            conn.commit()
            return {"message": "Created"}, 201

    def patch(self, user_id, json_data):
        """
        Patch a user's information.
        """
        json_data: dict = request.get_json()
        del (
            json_data["pswd_create"], 
            json_data["pswd_change"], 
            json_data["last_login"],
            json_data["created"],
            json_data["blocked"],
            json_data["deleted"],
            json_data["attempt"],
            )
        json_data["updated"] = datetime.now()
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE users SET SET {','.join(key + '= ?' for key in json_data.keys())} WHERE id = ?", 
                tuple(json_data.values()) + (user_id,)
            )
            conn.commit()
            return {"message": "Changed"}, 201

    def delete(self, user_id):
        """
        Delete a user by their ID.
        """
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET deleted = 1 WHERE id = ? AND username = ?", 
                (user_id, Token.current_user['username'])
            )
            conn.commit()
            return "", 204


user_view = UserView.as_view("user")
bp.add_url_rule("/user", view_func=user_view, methods=["POST"])
bp.add_url_rule(
    "/user/<int:user_id>", view_func=user_view, methods=["DELETE", "GET", "PATCH"]
)


class RoleView(MethodView):
    """
    Get a user's role based on the value and user ID.
    """

    decorators = [roles_required(Roles.admin.value)]

    def get(self, value, user_id):
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            query = cursor.execute(
                "SELECT * FROM user_roles JOIN roles ON user_roles.role_id = roles.id WHERE user_id = ?",
                (user_id),
            )
            roles = query.fetchall()
            if value not in [r[0] for r in roles]:
                cursor.execute(
                    "INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)",
                    (user_id, value),
                )
                conn.commit()
                return "", 201
            return "", 403

    def delete(self, value, user_id):
        """
        Deletes a role from a user.
        """
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            query_role = cursor.execute(
                "SELECT * FROM user_roles JOIN roles ON user_roles.role_id = roles.id WHERE user_id = ? AND roles.role = 'admin'",
                (user_id),
            )
            role = query_role.fetchone()
            query_user = cursor.execute(
                "SELECT username FROM users WHERE id = ?", (user_id)
            )
            username = query_user.fetchone()[0]

            if role and username != Token.current_user['username']:
                cursor.execute(
                    "DELETE FROM user_roles WHERE user_id = ? AND role_id = ?", 
                    (user_id, value)
                )
                conn.commit()
                return "", 204
        return "", 403


bp.add_url_rule("/role/<value>/<int:user_id>", view_func=RoleView.as_view("role"))

