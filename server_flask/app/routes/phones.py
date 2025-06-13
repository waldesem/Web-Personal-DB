"""User routes."""

from typing import ClassVar

from flask import Blueprint, Response, current_app, jsonify
from flask.views import MethodView
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.depends.depend import auth_required, validate
from app.model.classes import Roles
from app.model.models import Phone
from app.model.tables import Phones, db_session

bp = Blueprint("phones", __name__)


class PhoneView(MethodView):
    """Phone view class."""

    decorators: ClassVar = [auth_required(roles=(Roles.admin.value, Roles.user.value))]

    def get(self) -> Response:
        """Retrieve a list of phones from the database.

        Arguments:
            item (str): The table name from which to retrieve the phones.

        Returns:
            tuple: A tuple containing the JSON-encoded list of phones.

        """
        results = db_session.execute(select(Phones)).scalars()
        orgs = set(db_session.execute(select(Phones.organization)).scalars())
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
            if json_data.id:
                phone = db_session.get(Phones, json_data.id)
                if not phone:
                    return jsonify({"message": "error"}), 200
                for key, value in json_data.dict().items():
                    if value:
                        setattr(phone, key, value)
            else:
                db_session.add(Phones(**json_data.dict()))
            db_session.commit()
            return jsonify({"message": "success"}), 201
        except SQLAlchemyError:
            current_app.logger.exception("Database error")
            db_session.rollback()
            return jsonify({"message": "error"}), 200

    def delete(self, phone_id: int) -> Response:
        """Handle the DELETE request to delete a phone from the database.

        Arguments:
            phone_id (int): The ID of the phone to be deleted.

        Returns:
            The HTTP status code is 200.

        """
        phone = db_session.get(Phones, phone_id)
        db_session.delete(phone)
        db_session.commit()
        return jsonify({"message": "success"}), 200


view_func = PhoneView.as_view("phones")
bp.add_url_rule("/phones", view_func=view_func, methods=["GET", "POST"])
bp.add_url_rule("/phones/<int:phone_id>", view_func=view_func, methods=["DELETE"])
