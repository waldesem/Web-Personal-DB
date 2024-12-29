"""Workplace routes."""

from flask import Blueprint, Response, jsonify
from flask.views import MethodView
from sqlalchemy import select, text

from app.depends.depend import current_user, jwt_required, roles_required, validate
from app.model.classes import Roles
from app.model.models import Workplace
from app.model.tables import Workplaces, db_session

bp = Blueprint("workplaces", __name__, url_prefix="/workplaces")


class WorkplacesView(MethodView):
    """Workplace view."""

    @jwt_required()
    def get(self, item_id: int) -> Response:
        """Retrieve an item from the database based on the provided item ID.

        Args:
            item_id (int): The ID of the item to retrieve.

        Returns:
            Tuple[Response, int]: A tuple containing the JSON response containing
            the retrieved item(s) and an HTTP status code of 200.

        """
        stmt = select(Workplaces).filter_by(person_id=item_id)
        query = db_session.execute(stmt).scalars()
        return jsonify([row.to_dict() for row in query]), 200

    @validate()
    @roles_required(Roles.user.value)
    def post(self, item_id: int, json_data: Workplace) -> Response:
        """Insert or replace a record in the specified table with the given item ID.

        Args:
            item_id (int): The ID of the record to insert or replace.
            json_data (Workplace): The data to insert or replace.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.

        """
        json_dict = json_data.dict()
        item = Workplaces(**json_dict, person_id=item_id, user_id=current_user.id)
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
            code of 204.

        """
        stmt = text("DELETE FROM workplaces WHERE person_id = :item_id")
        db_session.execute(stmt, {"item_id": item_id})
        db_session.commit()
        return jsonify({"message": "success"}), 204


bp.add_url_rule("/<int:item_id>", view_func=WorkplacesView.as_view("workplace"))
