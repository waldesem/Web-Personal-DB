"""User routes."""

from flask import Blueprint, Response, current_app, jsonify
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash

from app import db
from app.decorators.depend import auth_required, current_user, get_current_user
from app.decorators.validate import validate
from app.models.models import UserActions, UserIn, UserOut
from app.tables.tables import Users
from app.utils.utilities import Regions, Roles

bp = Blueprint("users", __name__)


@bp.get("/users")
@auth_required(Roles.admin.value)
def get_users() -> Response:
    """Retrieve a list of users from the database.

    Arguments:
       None.

    Returns:
        tuple: A tuple containing the JSON-encoded list of users.

    """
    # Выбрать все столбцы, кроме passhash
    columns = filter(lambda x: x != "passhash", Users.__table__.columns.keys())
    # Создать запрос для выборки пользователей
    stmt = select(*[getattr(Users, column) for column in columns])
    users = db.session.execute(stmt).all()
    # Преобразовать результат в список словарей и вернуть в качестве ответа
    return jsonify([UserOut.from_orm(user).dict() for user in users]), 200


@bp.post("/user")
@validate
@auth_required(Roles.admin.value)
def post_user_actions(user_id: int, json_data: UserActions) -> Response:
    """Change a user's information in the database based on their user ID.

    Args:
        user_id (int): The ID of the user.
        json_data (UserActions): The user data to be updated in the database.

    Returns:
        The HTTP status code is 201.

    """
    # Получить пользователя по ID
    user = db.session.get(Users, user_id)
    # Если пользователь не найден или пытается изменить собственный профиль
    if not user or current_user.id == user.id:
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
    elif json_data.item in [reg.value for reg in Regions]:
        # Изменить регион пользователя
        user.region = json_data.item
    else:
        return jsonify({"message": "error"}), 200
    db.session.commit()
    # Очистить кэш для id пользователей
    get_current_user.cache_clear()
    return jsonify({"message": "success"}), 201


@bp.post("/user/<int:user_id>")
@validate
@auth_required(Roles.admin.value)
def post_user(json_data: UserIn) -> Response:
    """Handle the POST request to create a user in the database.

    Arguments:
        json_data (User): The user data to be added to the database.

    Returns:
        - If the user already exists returns an empty response with status code 200.
        - Otherwise returns a response with status code 201.

    """
    # Проверить, существует ли уже пользователь с таким именем
    user = db.session.execute(
        select(Users).filter(Users.username == json_data.username),
    ).all()
    if user:
        return jsonify({"message": "error"}), 200
    try:
        # Создать нового пользователя
        db.session.add(Users(**json_data.dict()))
        db.session.commit()
        return jsonify({"message": "success"}), 201
    except SQLAlchemyError:
        current_app.logger.exception("Database error")
        db.session.rollback()
        return jsonify({"message": "error"}), 200
