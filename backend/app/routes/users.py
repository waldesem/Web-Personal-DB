from flask import jsonify, request
from flask.views import MethodView
from werkzeug.security import generate_password_hash

from config import Config
from . import bp
from ..models.models import User
from ..tools.depends import user_required, current_user
from ..tools.queries import select_single, select_all, execute


@user_required(admin=True)
@bp.get("/users")
def get_users():
    """
    Endpoint to handle requests for getting users.
    """
    search_data = request.args.get("search", "")
    users = select_all(
        "SELECT * FROM users WHERE username LIKE '%{}%' ORDER BY id DESC".format(
            search_data
        ),
    )
    return jsonify(users), 200


class UserView(MethodView):
    @user_required()
    def get(self, user_id):
        """
        Retrieves a user based on the specified action and user ID.
        """
        action_data = request.args.get("action")
        if action_data != "view":
            query = "UPDATE users SET "
            values = []
            if action_data == "drop":
                query += "password = ?, attempt = ?, change_pswd = ? "
                values.extend(
                    [generate_password_hash(Config.DEFAULT_PASSWORD), 0, True]
                )
            elif action_data == "block":
                query += "blocked = ? "
                user = select_single("SELECT blocked FROM users WHERE id = ?", (user_id,))
                values.append(int(not user["blocked"]))
            execute(query + "WHERE id = ?", tuple(values + [user_id]))
        user = select_single("SELECT * FROM users WHERE id = ?", (user_id,))
        return jsonify(user), 200

    @user_required()
    def post(self):
        """
        Creates a new user based on the provided JSON data.
        """
        json_data = request.get_json()
        user = select_single(
            "SELECT * FROM users WHERE username = ?", (json_data.get("username"),)
        )
        if user:
            return "", 205
        try:
            json_dict = User(**json_data).model_dump()
            json_dict["password"] = generate_password_hash(Config.DEFAULT_PASSWORD)
            keys, args = zip(*json_dict.items())
            query = "INSERT INTO users ({}) VALUES ({})".format(
                ",".join(keys), ",".join("?" for _ in keys)
            )
            execute(query, args)
            return "", 201
        except Exception as e:
            print(e)
            return "", 400

    @user_required()
    def patch(self, user_id):
        json_data = request.get_json()
        try:
            json_dict = User(**json_data).model_dump()
            keys, args = zip(*json_dict.items())
            query = "UPDATE users SET {} WHERE id = ?".format(
                ",".join(f"{key} = ?" for key in keys)
            )
            execute(query, args + (user_id,))
            return "", 201
        except Exception as e:
            print(e)
            return "", 400

    @user_required(admin=True)
    def delete(self, user_id):
        """
        Delete a user by their ID.
        """
        if user_id == current_user["id"]:
            return "", 205
        execute(
            "UPDATE users SET deleted = 1 WHERE id = ?",
            (user_id,),
        )
        return "", 204


user_view = UserView.as_view("user")
bp.add_url_rule("/user", view_func=user_view, methods=["POST"])
bp.add_url_rule(
    "/user/<int:user_id>", view_func=user_view, methods=["DELETE", "GET", "PATCH"]
)
