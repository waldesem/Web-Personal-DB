"""User routes."""

from flask import Blueprint, current_app, g
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash

from app import db
from app.classes.classes import Roles
from app.decorators.depend import auth_required, get_current_user
from app.decorators.validize import pydantify
from app.models.models import User, UserActions, UserForm
from app.tables.tables import Users

bp = Blueprint("users", __name__)


@bp.get("/users")
@pydantify(User, orm=True, many=True)
@auth_required(Roles.admin.value)
def get_users() -> tuple[list[Users], int]:
    """Retrieve a list of users from the database."""
    # Выбрать все столбцы, кроме passhash
    columns = filter(lambda x: x != "passhash", Users.__table__.columns.keys())
    # Создать запрос для выборки пользователей
    stmt = select(*[getattr(Users, column) for column in columns])
    # Преобразовать результат в список словарей и вернуть в качестве ответа
    return db.session.execute(stmt).all(), 200


@bp.post("/user/<user_id>")
@pydantify()
@auth_required(Roles.admin.value)
def post_user_actions(user_id: int, json_query: UserActions) -> tuple[dict, int]:
    """Change a user's information in the database based on their user ID."""
    user = db.session.get(Users, user_id)
    # Если пользователь не найден или пытается изменить собственный профиль
    if not user or g.user.id == user.id:
        return {"message": "error"}, 400

    if json_query.item == "reset":
        # Сбросить пароль пользователя и обнулить попытки входа
        user.passhash = generate_password_hash(
            current_app.config["DEFAULT_PASSWORD"],
        )
        user.attempt = 0
        user.blocked = False
        user.change_pswd = True
    elif json_query.item == "block":
        # Заблокировать или разблокировать пользователя
        user.blocked = not user.blocked
    elif json_query.item == "delete":
        # Удалить или восстановить пользователя
        user.deleted = not user.deleted
    elif json_query.item in [reg.value for reg in Roles]:
        # Изменить роль пользователя
        user.role = json_query.item
    db.session.commit()
    # Очистить кэш для id пользователей
    get_current_user.cache_clear()
    return {"message": "success"}, 201


@bp.post("/user")
@pydantify()
@auth_required(Roles.admin.value)
def post_user(json_data: UserForm) -> tuple[dict, int]:
    """Handle the POST request to create a user in the database."""
    # Проверить, существует ли уже пользователь с таким именем
    user = db.session.execute(
        select(Users).filter(Users.username == json_data.username),
    ).all()
    if user:
        return {"message": "error"}, 400
    try:
        # Создать нового пользователя
        db.session.add(Users(**json_data.dict()))
        db.session.commit()
    except SQLAlchemyError:
        current_app.logger.exception("Database error")
        db.session.rollback()
        return {"message": "error"}, 400
    else:
        return {"message": "success"}, 201
