from datetime import datetime

from flask import jsonify, request
from flask.views import MethodView
from werkzeug.security import generate_password_hash

from config import Config
from . import bp
from ..tools.depends import admin_required
from ..tools.queries import select_single, select_all, execute


@admin_required()
@bp.get("/users")
def get_users():
    """
    Endpoint to handle requests for getting users.
    """
    search_data = request.args.get("search")
    return jsonify(select_all(
        "SELECT * FROM users WHERE username ILIKE '%{}%' ORDER BY id DESC"
        .format(search_data)
    )), 200


class UserView(MethodView):
    decorators = [admin_required()]

    def get(self, user_id):
        """
        Retrieves a user based on the specified action and user ID.
        """
        action_data = request.args.get("action")
        if action_data == "drop":
            execute(
                "UPDATE users SET password = ?, attempt = ?, change_pswd = ? WHERE id = ?",
                (
                    generate_password_hash(Config.DEFAULT_PASSWORD),
                    0,
                    True,
                    user_id,
                ),
            )
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
            "INSERT INTO users (fullname, username, email, password, has_admin, region) \
                VALUES (?, ?, ?, ?, ?, ?)",
            (
                json_data.get("fullname"),
                json_data.get("username"),
                json_data.get("email"),
                generate_password_hash(Config.DEFAULT_PASSWORD),
                bool(json_data.get("has_admin")),
                json_data.get("region"),
            ),
        )
        return {"message": "Created"}, 201

    def patch(self, user_id, json_data):
        """
        Patch a user's information.
        """
        json_data: dict = request.get_json()
        execute(
            "UPDATE users SET fullname=?, username=?, email=?, has_admin=?, updated =?, region=? \
                 WHERE id = ?",
            (
                json_data.get("fullname"),
                json_data.get("username"),
                json_data.get("email"),
                bool(json_data.get("has_admin")),
                datetime.now(),
                json_data.get("region"),
                user_id,
            ),
        )
        return {"message": "Changed"}, 201

    def delete(self, user_id):
        """
        Delete a user by their ID.
        """
        execute(
            "UPDATE users SET blocked = 1 WHERE id = ?",
            (user_id,),
        )
        return "", 204


user_view = UserView.as_view("user")
bp.add_url_rule("/user", view_func=user_view, methods=["POST"])
bp.add_url_rule(
    "/user/<int:user_id>", view_func=user_view, methods=["DELETE", "GET", "PATCH"]
)
