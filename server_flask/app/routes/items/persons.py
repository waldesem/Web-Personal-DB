"""Person routes."""

from flask import Blueprint, Response, jsonify
from flask.views import MethodView
from sqlalchemy import text

from app.depends.depend import jwt_required, roles_required, validate
from app.model.classes import Roles
from app.model.models import Person
from app.model.tables import Persons, db_session

bp = Blueprint("persons", __name__, url_prefix="/persons")


class PersonView(MethodView):
    """Person routes."""

    @jwt_required()
    def get(self, person_id: int) -> Response:
        """Retrieve an item from the database based on the provided item ID.

        Args:
            person_id (int): The ID of the item to retrieve.

        Returns:
            Tuple[Response, int]: A tuple containing the JSON response containing
            the retrieved item(s) and an HTTP status code of 200.

        """
        person = db_session.get(Persons, person_id)
        if not person:
            return "", 404
        return jsonify(person.to_dict()), 200

    @validate()
    @roles_required(Roles.user.value)
    def post(self, json_data: Person) -> Response:
        """Insert or replaces a record in the specified table with the given item ID.

        Args:
            json_data (Person): The data to replace in the table.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.

        """
        json_dict = json_data.dict()
        db_session.merge(Persons(**json_dict))
        db_session.commit()
        return jsonify({"message": "success"}), 201

    @roles_required(Roles.user.value)
    def delete(self, person_id: int) -> Response:
        """Delete an item from the database based on the provided item name and item ID.

        Args:
            person_id (int): The ID of the item to delete.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.

        """
        for table in [
            "previous",
            "educations",
            "addresses",
            "affilations",
            "staffs",
            "workplaces",
            "contacts",
            "documents",
            "checks",
            "poligrafs",
            "inquiries",
            "investigations",
        ]:
            db_session.execute(
                text(f"DELETE FROM {table} WHERE person_id = :person_id"),  # noqa: S608
                {"person_id": person_id},
            )
        db_session.execute(
            text("DELETE FROM person_relationships WHERE left_id = :person_id"),
            {"person_id": person_id},
        )
        db_session.execute(
            text("DELETE FROM person_relationships WHERE right_id = :person_id"),
            {"person_id": person_id},
        )
        db_session.execute(
            text("DELETE FROM persons WHERE id = :person_id"), {"person_id": person_id},
        )
        db_session.commit()
        return jsonify({"message": "success"}), 201


view_func = PersonView.as_view("person")
bp.add_url_rule("", view_func=view_func, methods=["POST"])
bp.add_url_rule("/<int:person_id>", view_func=view_func, methods=["GET", "DELETE"])
