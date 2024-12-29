"""Relation routes."""

from flask import Blueprint, Response, jsonify
from flask.views import MethodView
from sqlalchemy import text

from app.depends.depend import roles_required, validate
from app.model.classes import Roles
from app.model.models import Relation
from app.model.tables import Persons, association_table, db_session

bp = Blueprint("relations", __name__, url_prefix="/relations")


class RelationView(MethodView):
    """Relation view class."""

    @roles_required(Roles.user.value)
    def get(self, person_id: int) -> Response:
        """Retrieve a person's relationships from the database based on their person ID.

        Args:
            person_id (int): The ID of the person.

        Returns:
            Tuple[Response, int]: A tuple containing the JSON response containing
            the retrieved person's relationships and an HTTP status code of 200.

        """
        relation = db_session.execute(
            association_table.select().where(association_table.c.left_id == person_id),
        )
        relationship = db_session.execute(
            association_table.select().where(association_table.c.right_id == person_id),
        )
        return jsonify(
            [
                [i._asdict() for i in relation],
                [i._asdict() for i in relationship],
            ],
        ), 200

    @validate()
    @roles_required(Roles.user.value)
    def post(self, person_id: int, json_data: Relation) -> Response:
        """Insert or replace a record in the specified table with the given item ID.

        Args:
            person_id (int): The ID of the record to insert or replace.
            json_data (Relation): The data to insert or replace.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.

        """
        if json_data.right_id != person_id and db_session.get(
            Persons,
            json_data.right_id,
        ):
            relationship = association_table.insert().values(
                left_id=person_id,
                right_id=json_data.right_id,
                type=json_data.type,
            )
            db_session.execute(relationship)
            db_session.commit()
            return jsonify({"message": "success"}), 201
        return jsonify({"message": "error"}), 200

    @roles_required(Roles.user.value)
    def delete(self, person_id: int, relation_id: int) -> Response:
        """Delete an item from the database based on the provided item name and item ID.

        Args:
            person_id (int): The ID of the item to delete.
            relation_id (int): The ID of the item to delete.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 204.

        """
        stmt = text(
            "DELETE FROM relations \
                WHERE left_id = :person_id AND right_id = :relation_id",
        )
        db_session.execute(stmt, {"person_id": person_id, "relation_id": relation_id})
        """person = db_session.get(Persons, person_id)
        related_person = db_session.get(Persons, relation_id)
        person.relationships.remove(related_person)"""
        db_session.commit()
        return jsonify({"message": "success"}), 201


view_func = RelationView.as_view("relation")
bp.add_url_rule("/<int:person_id>", view_func=view_func, methods=["GET", "POST"])
bp.add_url_rule(
    "/<int:person_id>/<int:relation_id>",
    view_func=view_func,
    methods=["DELETE"],
)
