from datetime import datetime

from flask import abort, jsonify, request
from flask.views import MethodView
from werkzeug.security import generate_password_hash

from config import Config
from . import bp
from ..tools.depends import Token, roles_required
from ..tools.queries import select_single, select_all, execute
from ..tools.classes import Roles


@roles_required(Roles.admin.value)
@bp.get("/users")
def get_users():
    """
    Endpoint to handle requests for getting users.
    """
    search_data = request.args.get("search")
    result = select_all(
        "SELECT * FROM users ORDER BY id DESC",
    )
    if search_data:
        result = select_all(
            "SELECT * FROM users WHERE username LIKE '%{}%' ORDER BY id DESC".format(
                search_data
            )
        )
    return jsonify(result)


class UserView(MethodView):
    decorators = [roles_required(Roles.admin.value)]

    def get(self, user_id):
        """
        Retrieves a user based on the specified action and user ID.
        """
        action_data = request.args.get("action")
        user = select_single("SELECT * FROM users WHERE id = ?", (user_id,))
        if not user:
            return abort(404)
        if action_data != "view":
            match action_data:
                case "block":
                    if user["username"] != Token.current_user["username"]:
                        execute(
                            "UPDATE users SET blocked = ? WHERE id = ?",
                            (not user["blocked"], user_id),
                        )
                case "drop":
                    execute(
                        "UPDATE users SET password = ?, attempt = ?, change_pswd = ? WHERE id = ?",
                        (
                            generate_password_hash(
                                Config.DEFAULT_PASSWORD,
                                method="scrypt",
                                salt_length=16,
                            ),
                            0,
                            True,
                            user_id,
                        ),
                    )
                case "region":
                    execute(
                        "UPDATE users SET region_id = ? WHERE id = ?",
                        (action_data, user_id),
                    )
                case _:
                    return abort, 404
        return jsonify(
            select_single("SELECT * FROM users WHERE id = ?", (user_id,))
        ), 200

    def post(self):
        """
        Creates a new user based on the provided JSON data.
        """
        json_data = request.get_json()
        user = select_single(
            "SELECT * FROM users WHERE username = ?", (json_data.get("username"),)
        )
        if user:
            return {"message": "Denied"}, 403
        execute(
            "INSERT INTO users (fullname, username, email, password, email, pswd_create, change_pswd, last_login, blocked, deleted, attempt, created, updated, region_id) VALUES (?, ?, ?, ?)",
            (
                json_data.get("fullname"),
                json_data.get("username"),
                json_data.get("email"),
                generate_password_hash(
                    Config.DEFAULT_PASSWORD, method="scrypt", salt_length=16
                ),
                datetime.now(),
                True,
                None,
                0,
                0,
                0,
                datetime.now(),
                datetime.now(),
                json_data.get("region_id"),
            ),
        )
        return {"message": "Created"}, 201

    def patch(self, user_id, json_data):
        """
        Patch a user's information.
        """
        json_data: dict = request.get_json()
        del (
            json_data["pswd_create"],
            json_data["change_pswd"],
            json_data["last_login"],
            json_data["created"],
            json_data["blocked"],
            json_data["deleted"],
            json_data["attempt"],
        )
        json_data["updated"] = datetime.now()
        execute(
            f"UPDATE users SET SET {','.join(key + '= ?' for key in json_data.keys())} WHERE id = ?",
            tuple(json_data.values()) + (user_id,),
        )
        return {"message": "Changed"}, 201

    def delete(self, user_id):
        """
        Delete a user by their ID.
        """
        execute(
            "UPDATE users SET deleted = 1 WHERE id = ? AND username = ?",
            (user_id, Token.current_user["username"]),
        )
        return "", 204


user_view = UserView.as_view("user")
bp.add_url_rule("/user", view_func=user_view, methods=["POST"])
bp.add_url_rule(
    "/user/<int:user_id>", view_func=user_view, methods=["DELETE", "GET", "PATCH"]
)


class RoleView(MethodView):
    """
    Change a user's role based on the value and user ID.
    """

    decorators = [roles_required(Roles.admin.value)]

    def get(self, value, user_id):
        roles = select_all(
            "SELECT * FROM user_roles \
                LEFT JOIN roles ON user_roles.role_id = roles.id \
                    WHERE user_id = ?",
            (user_id),
        )
        if value not in [r["role"] for r in roles]:
            execute(
                "INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)",
                (user_id, value),
            )
            return "", 201
        return "", 403

    def delete(self, value, user_id):
        """
        Deletes a role from a user.
        """
        roles = select_single(
            "SELECT * FROM user_roles \
                LEFT JOIN roles ON user_roles.role_id = roles.id \
                    WHERE roles.role <> 'admin' AND user_roles.user_id <> ?",
            (Token.current_user["id"]),
        )

        if roles:
            execute(
                "DELETE FROM user_roles WHERE user_id = ? AND role_id = ?",
                (user_id, value),
            )
            return "", 204
        return "", 403


bp.add_url_rule("/role/<value>/<int:user_id>", view_func=RoleView.as_view("role"))
