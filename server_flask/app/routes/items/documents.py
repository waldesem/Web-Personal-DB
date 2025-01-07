"""Document routes."""

from flask import Blueprint, Response, jsonify
from flask.views import MethodView
from sqlalchemy import select, text

from app.depends.depend import current_user, jwt_required, roles_required, validate
from app.model.classes import Roles
from app.model.models import Document
from app.model.tables import Documents, db_session

bp = Blueprint("documents", __name__, url_prefix="/documents")


class DocumentsView(MethodView):
    """Documents view."""

    @jwt_required()
    def get(self, item_id: int) -> Response:
        """Retrieve an item from the database based on the provided item ID.

        Args:
            item_id (int): The ID of the item to retrieve.

        Returns:
            Tuple[Response, int]: A tuple containing the JSON response containing
            the retrieved item(s) and an HTTP status code of 200.

        """
        stmt = select(Documents).filter_by(person_id=item_id)
        query = db_session.execute(stmt).scalars()
        return jsonify([row.to_dict() for row in query]), 200

    @validate()
    @roles_required(Roles.user.value)
    def post(self, item_id: int, json_data: Document) -> Response:
        """Insert or replaces a record in the specified table with the given item ID.

        Args:
            item_id (int): The ID of the record to insert or replace.
            json_data (Document): The data to insert or replace.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.

        """
        json_dict = json_data.dict()
        item = Documents(**json_dict, person_id=item_id, user_id=current_user.id)
        db_session.merge(item)
        db_session.commit()
        return jsonify({"message": "success"}), 201

    @roles_required(Roles.user.value)
    def delete(self, item_id: int) -> Response:
        """Delete an item from the database based on the provided item name and item ID.

        Args:
            item_id (int): The ID of the item to delete.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.

        """
        stmt = text("DELETE FROM documents WHERE id = :item_id")
        db_session.execute(stmt, {"item_id": item_id})
        db_session.commit()
        return jsonify({"message": "success"}), 201

bp.add_url_rule("/<int:item_id>", view_func=DocumentsView.as_view("document"))
