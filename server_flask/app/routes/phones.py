"""User routes."""

from typing import ClassVar

from flask import Blueprint, Response, current_app, jsonify
from flask.views import MethodView
from sqlalchemy import select, text, update
from sqlalchemy.exc import SQLAlchemyError

from app.depends.depend import auth_required, validate
from app.model.classes import Roles
from app.model.models import Phone
from app.model.tables import Phones, db_session

bp = Blueprint("phones", __name__)


class PhoneView(MethodView):
    """Phone view class."""

    decorators: ClassVar = [auth_required(roles=[Roles.admin.value, Roles.user.value])]

    def get(self) -> Response:
        """Retrieve a list of phones from the database.

        Arguments:
            item (str): The table name from which to retrieve the phones.

        Returns:
            tuple: A tuple containing the JSON-encoded list of phones.

        """
        # Запрос к базе данных для получения списка телефонов
        results = db_session.execute(select(Phones)).scalars()
        # Запрос к базе данных для получения списка организаций
        orgs = set(db_session.execute(select(Phones.organization)).scalars())
        # Возврат данных в формате JSON и в виде ответа на запрос
        return jsonify(
            {
                "results": [result.to_dict() for result in results],
                "organizations": list(orgs),
            },
        ), 200

    @validate
    def post(self, json_data: Phone) -> Response:
        """Handle the POST request to create a user in the database.

        Arguments:
            json_data (User): The user data to be added to the database.

        Returns:
            - If the user already exists returns an empty response with status code 200.
            - Otherwise returns a response with status code 201.

        """
        try:
            json_dict = json_data.dict(exclude_none=True)
            # Обновление существующей записи
            if item_id := json_dict.pop("id", None):
                db_session.execute(
                    update(Phones)
                    .where(Phones.id == item_id)
                    .values(**json_dict),
                )
            else:
                # Создание новой записи
                db_session.add(Phones(**json_dict))
        except SQLAlchemyError:
            current_app.logger.exception("Database error")
            db_session.rollback()
            return jsonify({"message": "error"}), 200
        else:
            db_session.commit()
            return jsonify({"message": "success"}), 201

    def delete(self, phone_id: int) -> Response:
        """Handle the DELETE request to delete a phone from the database.

        Arguments:
            phone_id (int): The ID of the phone to be deleted.

        Returns:
            The HTTP status code is 200.

        """
        # Удаление записи из таблицы phones
        db_session.execute(text("DELETE FROM phones WHERE id = :id"), {"id": phone_id})
        db_session.commit()
        return jsonify({"message": "success"}), 200


view_func = PhoneView.as_view("phones")
bp.add_url_rule("/phones", view_func=view_func, methods=["GET", "POST"])
bp.add_url_rule("/phones/<int:phone_id>", view_func=view_func, methods=["DELETE"])
