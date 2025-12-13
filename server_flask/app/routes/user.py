"""User routes."""

from flask import Blueprint, Response, current_app, g, jsonify
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from app import db
from app.classes.classes import Roles
from app.decorators.depend import auth_required, get_current_user
from app.decorators.pydantify import validize
from app.models.models import User, Actions, UserForm
from app.tables.tables import Users

bp = Blueprint("users", __name__)


@bp.get("/users")
@auth_required(Roles.admin.value)
def get_users() -> Response:
    """Retrieve a list of users from the database."""
    users = db.session.execute(select(Users)).scalars()
    return jsonify([User.model_validate(user).model_dump() for user in users]), 200


@bp.post("/user/<user_id>")
@validize()
@auth_required(Roles.admin.value)
def post_user_actions(user_id: int, json_data: Actions) -> Response:
    """Change a user's information in the database based on their user ID."""
    user = db.session.get(Users, user_id)
    # Если пользователь не найден или пытается изменить собственный профиль
    if not user or g.user.id == user.id:
        return jsonify({"message": "error"}), 200

    if json_data.item == "reset":
        # Сбросить пароль пользователя и обнулить попытки входа
        user.passhash = generate_password_hash(
            current_app.config["DEFAULT_PASSWORD"],
        )
        user.attempt = 0
        user.blocked = False
        user.change_pswd = True
    elif json_data.item == "block":
        # Заблокировать или разблокировать пользователя
        user.blocked = not user.blocked
    elif json_data.item == "delete":
        # Удалить или восстановить пользователя
        user.deleted = not user.deleted
    elif json_data.item in [reg.value for reg in Roles]:
        # Изменить роль пользователя
        user.role = json_data.item
    db.session.commit()
    # Очистить кэш для id пользователей
    get_current_user.cache_clear()
    return jsonify({"message": "success"}), 201


@bp.post("/user")
@validize()
@auth_required(Roles.admin.value)
def post_user(json_data: UserForm) -> Response:
    """Handle the POST request to create a user in the database."""
    # Проверить, существует ли уже пользователь с таким именем
    user = db.session.execute(
        select(Users).filter(Users.username == json_data.username),
    ).all()
    if user:
        return {"message": "error"}, 200
    db.session.add(Users(**json_data.model_dump()))
    db.session.commit()
    return jsonify({"message": "success"}), 201
