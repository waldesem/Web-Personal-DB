from flask import Blueprint, jsonify
from flask.views import MethodView
from sqlalchemy import desc, select

from ...depends.depend import current_user, jwt_required, roles_required, validate
from ...model.classes import Roles
from ...model.models import Inquiry
from ...model.tables import Inquiries, db_session

bp = Blueprint("inquiries", __name__, url_prefix="/inquiries")


class InquiriesView(MethodView):
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
        stmt = select(Inquiries).filter(Inquiries.person_id == item_id)
        query = db_session.execute(stmt.order_by(desc(Inquiries.id)))
        return jsonify([row._asdict() for row in query]), 200

    @validate()
    @roles_required(Roles.user.value)
    def post(self, item_id, json_data: Inquiry):
        """
        Inserts or replaces a record in the specified table with the given item ID.

        Parameters:
            item_id (int): The ID of the record to insert or replace.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.
        """
        json_dict = json_data.dict()
        json_dict["person_id"] = item_id
        json_dict["user_id"] = current_user.get("id")
        item_id = json_dict.pop("id", None)
        if item_id:
            item = db_session.get(Inquiries, item_id)
            for key, value in json_dict.items():
                setattr(item, key, value)
        else:
            db_session.add(Inquiries(**json_dict))
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
        table = db_session.get(Inquiries, item_id)
        db_session.delete(table)
        db_session.commit()
        return jsonify({"message": "success"}), 201


bp.add_url_rule("/<int:item_id>", view_func=InquiriesView.as_view("inquiry"))
