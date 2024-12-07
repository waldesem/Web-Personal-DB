from flask import Blueprint, jsonify
from flask.views import MethodView

from ...depends.depend import current_user, jwt_required, roles_required, validate
from ...model.classes import Roles
from ...model.models import Person
from ...model.tables import Persons, association_table, db_session, tables

bp = Blueprint("persons", __name__, url_prefix="/persons")


class PersonView(MethodView):
    @jwt_required()
    def get(self, item_id):
        """
        Retrieves an item from the database based on the provided item name and item ID.

        Parameters:
            item_id (int): The ID of the item to retrieve.

        Returns:
            Tuple[Response, int]: A tuple containing the JSON response containing
            the retrieved item(s) and an HTTP status code of 200.
        """
        person = db_session.get(Persons, item_id)
        if not person:
            return "", 404
        return jsonify(person.to_dict()), 200

    @validate()
    @roles_required(Roles.user.value)
    def post(self, item_id, json_data: Person):
        """
        Inserts or replaces a record in the specified table with the given item ID.

        Parameters:
            json_data (Person): The data to insert or replace in the table.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.
        """
        json_data.user_id = current_user.get("id")
        person = db_session.get(Persons, item_id)
        for key, value in json_data.dict().items():
            setattr(person, key, value)
        db_session.commit()
        return jsonify({"message": "success"}), 201

    @roles_required(Roles.user.value)
    def delete(self, item_id):
        """
        Deletes an item from the database based on the provided item name and item ID.

        Parameters:
            item_id (int): The ID of the item to delete.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 204.
        """
        for model, tbl in tables.items():
            if model not in ["users", "persons", "person_relationships"]:
                db_session.execute(tbl.delete().where(tbl.c.person_id == item_id))
        db_session.execute(
            association_table.delete().where(association_table.c.left_id == item_id)
        )
        db_session.execute(
            association_table.delete().where(association_table.c.right_id == item_id)
        )
        person = db_session.get(Persons, item_id)
        db_session.delete(person)
        db_session.commit()
        return jsonify({"message": "success"}), 201


bp.add_url_rule("/<int:item_id>", view_func = PersonView.as_view("person"))
