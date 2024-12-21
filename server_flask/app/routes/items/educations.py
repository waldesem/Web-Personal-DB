"""Education routes."""

from flask import Blueprint, Response, jsonify
from flask.views import MethodView
from sqlalchemy import desc, select

from app.depends.depend import current_user, jwt_required, roles_required, validate
from app.model.classes import Roles
from app.model.models import Education
from app.model.tables import Educations, db_session

bp = Blueprint("educations", __name__, url_prefix="/educations")


class EducationView(MethodView):
    """Education view."""

    @jwt_required()
    def get(self, item_id: int) -> Response:
        """Retrieve an item from the database based on the provided item ID.

        Args:
            item_id (int): The ID of the item to retrieve.

        Returns:
            Tuple[Response, int]: A tuple containing the JSON response containing
            the retrieved item(s) and an HTTP status code of 200.

        """
        stmt = select(Educations).filter(Educations.person_id == item_id)
        query = db_session.execute(stmt.order_by(desc(Educations.id))).scalars()
        return jsonify([row.to_dict() for row in query]), 200

    @validate()
    @roles_required(Roles.user.value)
    def post(self, item_id: int, json_data: Education) -> Response:
        """Insert or replace a record in the specified table with the given item ID.

        Args:
            item_id (int): The ID of the record to insert or replace.
            json_data (Education): The data to insert or replace.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.

        """
        json_dict = json_data.dict()
        json_dict["person_id"] = item_id
        json_dict["user_id"] = current_user.id
        item_id = json_dict.pop("id", None)
        if item_id:
            item = db_session.get(Educations, item_id)
            for key, value in json_dict.items():
                setattr(item, key, value)
        else:
            table = Educations(**json_dict)
            db_session.add(table)
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
        table = db_session.get(Educations, item_id)
        db_session.delete(table)
        db_session.commit()
        return jsonify({"message": "success"}), 201


bp.add_url_rule("/<int:item_id>", view_func=EducationView.as_view("education"))
