"""Items routes."""

from flask import Blueprint, current_app
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase

from app import db
from app.classes.classes import Roles
from app.decorators.depend import auth_required
from app.decorators.validate import serialize, validate
from app.models.models import (
    Items,
    ModelIn,
    ModelOut,
    PersonExists,
    PersonIn,
    PersonOut,
)
from app.tables.tables import Persons
from app.utils.utilities import upload_resume

bp = Blueprint("items", __name__, url_prefix="/items")


class PersonView(MethodView):
    """Person routes."""

    @serialize(PersonOut)
    @auth_required()
    def get(self, person_id: int) -> tuple[Persons, int]:
        """Retrieve an item from the database based on the provided item ID.

        Args:
            person_id (int): The ID of the item to retrieve.

        Returns:
            Tuple[Response, int]: A tuple containing the JSON response containing
            the retrieved item(s) and an HTTP status code of 200.

        """
        # Получаем данные кандидата
        return db.session.get(Persons, person_id), 200

    @serialize(PersonExists)
    @validate
    @auth_required(Roles.user.value)
    def post(self, json_data: PersonIn) -> tuple[dict, int]:
        """Replace a record in persons table.

        Args:
            json_data (InputPerson): The data to replace in the table.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.

        """
        # Загружаем отредактированное резюме и получаем id кандидата
        cand_id, existed = upload_resume(json_data)
        return {"person_id": cand_id, "exists": existed}, 201

    @serialize()
    @auth_required(Roles.user.value)
    def delete(self, person_id: int) -> tuple[str, int]:
        """Delete an item from the database based on the provided item name and item ID.

        Args:
            person_id (int): The ID of the item to delete.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.

        """
        try:
            person = db.session.get(Persons, person_id)
            db.session.delete(person)
            db.session.commit()
        except SQLAlchemyError:
            current_app.logger.exception("Database error")
            db.session.rollback()
            return "error", 500
        else:
            return "success", 201


view_func = PersonView.as_view("person")
bp.add_url_rule("/persons", view_func=view_func, methods=["POST"])
bp.add_url_rule(
    "/persons/<int:person_id>",
    view_func=view_func,
    methods=["GET", "DELETE"],
)


class ItemsView(MethodView):
    """Items view."""

    @serialize(ModelOut)
    @auth_required()
    def get(self, item: Items, item_id: int) -> tuple[DeclarativeBase, int]:
        """Retrieve an item from the database based on the provided item.

        Args:
            item (str): The type of item to retrieve.
            item_id (int): The ID of the item to retrieve.

        Returns:
            Tuple[Response, int]: A tuple containing the JSON response containing
            the retrieved item(s) and an HTTP status code of 200.

        """
        # Создаем запрос к таблице и сортируем результаты по id в обратном порядке
        stmt = (
            db.metatables[item]
            .select()
            .filter(db.metatables[item].c.person_id == item_id)
            .order_by(db.metatables[item].c.id.desc())
        )
        # Выполняем запрос и получаем результаты
        return db.session.execute(stmt).all(), 200

    @serialize()
    @validate
    @auth_required(Roles.user.value)
    def post(self, item: Items, item_id: int, json_data: ModelIn) -> tuple[str, int]:
        """Insert or replaces a record in the specified table with the given item ID.

        Args:
            item (str): The type of item to insert or replace.
            item_id (int): The ID of the record to insert or replace.
            json_data (Address): The data to insert or replace.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.

        """
        # Получаем таблицу из словаря таблиц по имени item
        json_dict = json_data.dict(exclude_none=True)
        # Добавляем ключ "person_id" в словарь json_dict с значением item_id
        json_dict["person_id"] = item_id
        try:
            # Проверяем, есть ли ключ "id" в словаре json_dict
            if table_id := json_dict.pop("id", None):
                # Если есть, создаем запрос на обновление записи с указанным id
                stmt = (
                    db.metatables[item]
                    .update()
                    .where(db.metatables[item].c.id == table_id)
                    .values(json_dict)
                )
            else:
                # Если нет, создаем запрос на вставку новой записи
                stmt = db.metatables[item].insert().values(json_dict)
            db.session.execute(stmt)
            db.session.commit()
        except SQLAlchemyError:
            current_app.logger.exception("Database error")
            db.session.rollback()
            return "error", 500
        else:
            return "success", 201

    @serialize()
    @auth_required(Roles.user.value)
    def delete(self, item: Items, item_id: int) -> tuple[str, int]:
        """Delete an item from the database based on the provided item name and item ID.

        Args:
            item (str): The type of item to delete.
            item_id (int): The ID of the item to delete.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.

        """
        try:
            # Удаляем запись из таблицы items с указанным id
            db.session.execute(
                db.metatables[item].delete().where(db.metatables[item].c.id == item_id),
            )
            db.session.commit()
        except SQLAlchemyError:
            current_app.logger.exception("Database error")
            db.session.rollback()
            return "error", 500
        else:
            return "success", 201


bp.add_url_rule("/<item>/<int:item_id>", view_func=ItemsView.as_view("item"))
