"""Items routes."""

from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify
from flask.views import MethodView
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.depends.depend import auth_required, current_user, validate
from app.structures.classes import Roles
from app.structures.models import Items, Model, Person
from app.structures.tables import Persons
from app.utils.utilities import create_destination, upload_resume

bp = Blueprint("items", __name__, url_prefix="/items")


class PersonView(MethodView):
    """Person routes."""

    @auth_required()
    def get(self, person_id: int) -> Response:
        """Retrieve an item from the database based on the provided item ID.

        Args:
            person_id (int): The ID of the item to retrieve.

        Returns:
            Tuple[Response, int]: A tuple containing the JSON response containing
            the retrieved item(s) and an HTTP status code of 200.

        """
        # Получаем данные кандидата и создаем папку для него, если ее нет
        person = db.session.get(Persons, person_id)
        if not person.destination or not Path(person.destination).is_dir():
            person.destination = create_destination(person)
            db.session.commit()
        return jsonify(person.to_dict()), 200

    @validate
    @auth_required(Roles.user.value)
    def post(self, json_data: Person) -> Response:
        """Replace a record in persons table.

        Args:
            json_data (Person): The data to replace in the table.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.

        """
        # Загружаем отредактированное резюме и получаем id кандидата
        cand_id, _ = upload_resume(json_data)
        if cand_id:
            return jsonify({"message": "success"}), 201
        return jsonify({"message": "error"}), 200

    @auth_required(Roles.user.value)
    def delete(self, person_id: int) -> Response:
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
            return jsonify({"message": "success"}), 201
        except SQLAlchemyError:
            current_app.logger.exception("Database error")
            db.session.rollback()
            return jsonify({"message": "error"}), 200


view_func = PersonView.as_view("person")
bp.add_url_rule("/persons", view_func=view_func, methods=["POST"])
bp.add_url_rule(
    "/persons/<int:person_id>",
    view_func=view_func,
    methods=["GET", "DELETE"],
)


class ItemsView(MethodView):
    """Items view."""

    @auth_required()
    def get(self, item: Items, item_id: int) -> Response:
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
            db.metadata[item].select().filter(db.metadata[item].c.person_id == item_id)
        )
        # Выполняем запрос и получаем результаты
        query = db.session.execute(stmt.order_by(desc(db.metadata[item].c.id)))
        # Преобразуем результаты в словарь и возвращаем их в формате JSON
        return jsonify([row._asdict() for row in query])

    @validate
    @auth_required(Roles.user.value)
    def post(self, item: Items, item_id: int, json_data: Model) -> Response:
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
        # Добавляем ключ "user_id" в словарь json_dict с значением текущего пользователя
        json_dict["user_id"] = current_user.id
        try:
            # Проверяем, есть ли ключ "id" в словаре json_dict
            if table_id := json_dict.pop("id", None):
                # Если есть, создаем запрос на обновление записи с указанным id
                stmt = (
                    db.metadata[item]
                    .update()
                    .where(db.metadata[item].c.id == table_id)
                    .values(json_dict)
                )
            else:
                # Если нет, создаем запрос на вставку новой записи
                stmt = db.metadata[item].insert().values(json_dict)
            db.session.execute(stmt)
            db.session.commit()
            return jsonify({"message": "success"}), 201
        except SQLAlchemyError:
            current_app.logger.exception("Database error")
            db.session.rollback()
            return jsonify({"message": "error"}), 200

    @auth_required(Roles.user.value)
    def delete(self, item: Items, item_id: int) -> Response:
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
                db.metadata[item].delete().where(db.metadata[item].c.id == item_id),
            )
            db.session.commit()
            return jsonify({"message": "success"}), 201
        except SQLAlchemyError:
            current_app.logger.exception("Database error")
            db.session.rollback()
            return jsonify({"message": "error"}), 200


bp.add_url_rule("/<item>/<int:item_id>", view_func=ItemsView.as_view("item"))
