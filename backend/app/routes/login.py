from datetime import datetime, timezone

from flask import jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from ..tools.depends import create_token
from ..tools.queries import execute, select_single
from . import bp


@bp.post("/login/<action>")
def post_login(action):
    json_data = request.get_json()
    user = select_single(
        "SELECT * FROM users WHERE username = ?", 
        (json_data.get("username"),)
    )
    if not user or user["blocked"] or user["deleted"]:
        return "", 204
        
    if not check_password_hash(user["password"], json_data["password"]):
        if user["attempt"] < 5:
            execute(
                "UPDATE users SET attempt = ? WHERE id = ?",
                (
                    user["attempt"] + 1,
                    user["id"],
                ),
            )
        else:
            execute("UPDATE users SET blocked = 1 WHERE id = ?", (user["id"],))
        return "", 204
    
    if action == "change":
        execute(
            "UPDATE users SET password = ?, change_pswd = 0, attempt = 0 WHERE id = ?",
            (
                generate_password_hash(json_data["new_pswd"]),
                user["id"],
            ),
        )
        return "", 201
    else:
        delta_change = datetime.now() - datetime.fromisoformat(user["pswd_create"])
        if not user["change_pswd"] and delta_change.days < 30:
            execute(
                "UPDATE users SET last_login = ?, attempt = ? WHERE id = ?",
                (datetime.now(timezone.utc), 0, user["id"]),
            )
            return jsonify(
                {
                    "user_token": create_token(user),
                }
            ), 200
        return "", 205
