"""Items routes."""

from flask import Blueprint, Response, current_app, jsonify
from flask.views import MethodView
from sqlalchemy import desc, text
from sqlalchemy.exc import SQLAlchemyError

from app.depends.depend import current_user, jwt_required, roles_required, validate
from app.model.classes import Roles
from app.model.models import Model, Person, Relation
from app.model.tables import Base, Persons, association_table, db_session

bp = Blueprint("items", __name__, url_prefix="/items")


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
        return jsonify(db_session.get(Persons, person_id).to_dict()), 200

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
        try:
            db_session.merge(Persons(**json_data.dict()))
            db_session.commit()
            return jsonify({"message": "success"}), 201
        except SQLAlchemyError:
            current_app.logger.exception("Database error")
            db_session.rollback()
            return jsonify({"message": "error"}), 200

    @roles_required(Roles.user.value)
    def delete(self, person_id: int) -> Response:
        """Delete an item from the database based on the provided item name and item ID.

        Args:
            person_id (int): The ID of the item to delete.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.

        """
        try:
            for item in [
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
                table = Base.metadata.tables.get(item)
                db_session.execute(table.delete().where(table.c.person_id == person_id))
            db_session.execute(
                text("DELETE FROM person_relationships WHERE left_id = :person_id"),
                {"person_id": person_id},
            )
            db_session.execute(
                text("DELETE FROM person_relationships WHERE right_id = :person_id"),
                {"person_id": person_id},
            )
            db_session.execute(
                text("DELETE FROM persons WHERE id = :person_id"),
                {"person_id": person_id},
            )
            db_session.commit()
            return jsonify({"message": "success"}), 201
        except SQLAlchemyError:
            current_app.logger.exception("Database error")
            db_session.rollback()
            return jsonify({"message": "error"}), 200


view_func = PersonView.as_view("person")
bp.add_url_rule("/persons", view_func=view_func, methods=["POST"])
bp.add_url_rule(
    "/persons/<int:person_id>",
    view_func=view_func,
    methods=["GET", "DELETE"],
)


class RelationView(MethodView):
    """Relation view class."""

    @jwt_required()
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
            try:
                db_session.execute(
                    association_table.insert().values(
                        left_id=person_id,
                        right_id=json_data.right_id,
                        type=json_data.type,
                    ),
                )
                db_session.commit()
                return jsonify({"message": "success"}), 201
            except SQLAlchemyError:
                current_app.logger.exception("Database error")
                db_session.rollback()
        return jsonify({"message": "error"}), 200

    @roles_required(Roles.user.value)
    def delete(self, person_id: int, relation_id: int) -> Response:
        """Delete an item from the database based on the provided item name and item ID.

        Args:
            person_id (int): The ID of the item to delete.
            relation_id (int): The ID of the item to delete.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.

        """
        try:
            db_session.execute(
                text(
                    "DELETE FROM person_relationships \
                    WHERE left_id = :person_id AND right_id = :relation_id",
                ),
                {"person_id": person_id, "relation_id": relation_id},
            )
            db_session.commit()
            return jsonify({"message": "success"}), 201
        except SQLAlchemyError:
            current_app.logger.exception("Database error")
            db_session.rollback()
            return jsonify({"message": "error"}), 200


view_func = RelationView.as_view("relation")
bp.add_url_rule(
    "/relations/<int:person_id>",
    view_func=view_func,
    methods=["GET", "POST"],
)
bp.add_url_rule(
    "/relations/<int:person_id>/<int:relation_id>",
    view_func=view_func,
    methods=["DELETE"],
)


class ItemsView(MethodView):
    """Items view."""

    @jwt_required()
    def get(self, item: str, item_id: int) -> Response:
        """Retrieve an item from the database based on the provided item ID.

        Args:
            item (str): The type of item to retrieve.
            item_id (int): The ID of the item to retrieve.

        Returns:
            Tuple[Response, int]: A tuple containing the JSON response containing
            the retrieved item(s) and an HTTP status code of 200.

        """
        table = Base.metadata.tables.get(item)
        stmt = table.select().filter(table.c.person_id == item_id)
        query = db_session.execute(stmt.order_by(desc(table.c.id)))
        return jsonify([row._asdict() for row in query])

    @validate()
    @roles_required(Roles.user.value)
    def post(self, item: str, item_id: int, json_data: Model) -> Response:
        """Insert or replaces a record in the specified table with the given item ID.

        Args:
            item (str): The type of item to insert or replace.
            item_id (int): The ID of the record to insert or replace.
            json_data (Address): The data to insert or replace.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.

        """
        table = Base.metadata.tables.get(item)
        json_dict = json_data.dict() | {
            "person_id": item_id,
            "user_id": current_user.id,
        }
        table_id = json_dict.pop("id", None)
        try:
            stmt = (
                table.update().where(table.c.id == table_id).values(json_dict)
                if table_id
                else table.insert().values(json_dict)
            )
            db_session.execute(stmt)
            db_session.commit()
            return jsonify({"message": "success"}), 201
        except SQLAlchemyError:
            current_app.logger.exception("Database error")
            db_session.rollback()
            return jsonify({"message": "error"}), 200

    @roles_required(Roles.user.value)
    def delete(self, item: str, item_id: int) -> Response:
        """Delete an item from the database based on the provided item name and item ID.

        Args:
            item (str): The type of item to delete.
            item_id (int): The ID of the item to delete.

        Returns:
            Tuple[str, int]: A tuple containing an empty string and an HTTP status
            code of 201.

        """
        try:
            table = Base.metadata.tables.get(item)
            db_session.execute(table.delete().where(table.c.id == item_id))
            db_session.commit()
            return jsonify({"message": "success"}), 201
        except SQLAlchemyError:
            current_app.logger.exception("Database error")
            db_session.rollback()
            return jsonify({"message": "error"}), 200


bp.add_url_rule("/<item>/<int:item_id>", view_func=ItemsView.as_view("item"))
