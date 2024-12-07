from flask import Blueprint, current_app, jsonify, request
from pydantic import ValidationError
from sqlalchemy import desc

from ...depends.depend import (
    current_user,
    jwt_required,
    roles_required,
)
from ...model.classes import Roles
from ...model.models import Model
from ...model.tables import (
    Persons,
    association_table,
    db_session,
    tables,
)

bp = Blueprint("items", __name__, url_prefix="/items")


@bp.get("/<item>/<int:item_id>")
@jwt_required()
def get_item_id(item, item_id):
    """
    Retrieves an item from the database based on the provided item name and item ID.

    Parameters:
        item (str): The name of the table to retrieve the item from.
        item_id (int): The ID of the item to retrieve.

    Returns:
        Tuple[Response, int]: A tuple containing the JSON response containing
        the retrieved item(s) and an HTTP status code of 200.
    """
    if item == "persons":
        person = db_session.get(Persons, item_id)
        if not person:
            return "", 404
        return jsonify(person.to_dict()), 200
    else:
        table = tables.get(item)
        stmt = table.select().filter(table.c.person_id == item_id)
        query = db_session.execute(stmt.order_by(desc(table.c.id)))
        return jsonify([row._asdict() for row in query])


@bp.post("/<item>/<int:item_id>")
@roles_required(Roles.user.value)
def post_item_id(item, item_id):
    """
    Inserts or replaces a record in the specified table with the given item ID.

    Parameters:
        item (str): The name of the table to insert or replace the record in.
        item_id (int): The ID of the record to insert or replace.

    Returns:
        Tuple[str, int]: A tuple containing an empty string and an HTTP status
        code of 201.
    """
    json_data = request.get_json()
    models = {
        cls.__modelname__: cls
        for cls in Model.__subclasses__()
        if hasattr(cls, "__modelname__")
    }
    table, model = tables.get(item), models.get(item)
    try:
        json_data = model(**json_data).dict()
    except ValidationError as e:
        current_app.logger.exception(e)
        return jsonify({"message": "error"}), 200
    if item != "persons":
        json_data["person_id"] = item_id
    json_data["user_id"] = current_user.get("id")
    table_id = json_data.pop("id", None)
    stmt = (
        table.update().where(table.c.id == table_id).values(json_data)
        if table_id
        else table.insert().values(json_data)
    )
    db_session.execute(stmt)
    db_session.commit()
    return jsonify({"message": "success"}), 201


@bp.delete("/<item>/<int:item_id>")
@roles_required(Roles.user.value)
def delete_item(item, item_id):
    """
    Deletes an item from the database based on the provided item name and item ID.

    Parameters:
        item (str): The name of the table to delete the item from.
        item_id (int): The ID of the item to delete.

    Returns:
        Tuple[str, int]: A tuple containing an empty string and an HTTP status
        code of 204.
    """
    table = tables.get(item)
    if item == "persons":
        for model, tbl in tables.items():
            if model not in ["users", "persons", "person_relationships"]:
                db_session.execute(tbl.delete().where(tbl.c.person_id == item_id))
        db_session.execute(
            association_table.delete().where(association_table.c.left_id == item_id)
        )
        db_session.execute(
            association_table.delete().where(association_table.c.right_id == item_id)
        )
    db_session.execute(table.delete().where(table.c.id == item_id))
    db_session.commit()
    return jsonify({"message": "success"}), 201
