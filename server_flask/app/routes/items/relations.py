from flask import Blueprint, jsonify
from flask.views import MethodView

from ...depends.depend import roles_required, validate
from ...model.classes import Roles
from ...model.models import Relation
from ...model.tables import Persons, association_table, db_session


bp = Blueprint("relations", __name__, url_prefix="/relations")


class RelationView(MethodView):
    @roles_required(Roles.user.value)
    def get_relation(person_id: int):
        """
        Retrieves a person's relationships from the database based on their person ID.

        Parameters:
            person_id (int): The ID of the person.

        Returns:
            Tuple[Response, int]: A tuple containing the JSON response containing
            the retrieved person's relationships and an HTTP status code of 200.
        """
        relation = db_session.execute(
            association_table.select().where(association_table.c.left_id == person_id)
        )
        relationship = db_session.execute(
            association_table.select().where(association_table.c.right_id == person_id)
        )
        return jsonify(
            [
                [i._asdict() for i in relation],
                [i._asdict() for i in relationship],
            ]
        ), 200

    @validate()
    @roles_required(Roles.user.value)
    def post_relation(person_id: int, json_data: Relation):
        """
        Inserts or replaces a record in the specified table with the given item ID.

        Parameters:
            item (str): The name of the table to insert or replace the record in.
            item_id (int): The ID of the record to insert or replace.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.
        """
        if json_data["right_id"] != person_id and db_session.get(
            Persons, json_data["right_id"]
        ):
            relationship = association_table.insert().values(
                left_id=person_id,
                right_id=json_data["right_id"],
                type=json_data["type"],
            )
            db_session.execute(relationship)
            db_session.commit()
            return jsonify({"message": "success"}), 201
        return jsonify({"message": "error"}), 200

    @roles_required(Roles.user.value)
    def delete_relation(person_id: int, relation_id: int):
        """
        Deletes an item from the database based on the provided item name and item ID.

        Parameters:
            item (str): The name of the table to delete the item from.
            item_id (int): The ID of the item to delete.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 204.
        """
        person = db_session.get(Persons, person_id)
        related_person = db_session.get(Persons, relation_id)
        person.relationships.remove(related_person)
        db_session.commit()
        return jsonify({"message": "success"}), 201


view_func = RelationView.as_view("relation")
bp.add_url_rule("/<int:person_id>", view_func=view_func, methods=["GET", "POST"])
bp.add_url_rule(
    "/<int:person_id>/<int:relation_id>", view_func=view_func, methods=["DELETE"]
)
