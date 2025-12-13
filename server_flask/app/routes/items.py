"""Items routes."""

from flask import Blueprint, Response, abort, current_app, jsonify
from pydantic import ValidationError

from app import db
from app.classes.classes import Roles
from app.decorators.depend import auth_required
from app.decorators.pydantify import validize
from app.models.models import ItemModel, Items, Model, models

bp = Blueprint("items", __name__, url_prefix="/items")


def validate_item(item: str) -> Items:
    """Create model."""
    try:
        return ItemModel(item=item).item
    except ValidationError:
        current_app.logger.exception("Error validating data")
        return abort(400)


@bp.get("/<item>/<int:person_id>")
@validize()
@auth_required()
def get_items(item: Items, person_id: int) -> Response:
    """Retrieve an item from the database based on the provided item."""
    table = validate_item(item)
    model = models.get(table)
    stmt = (
        db.metatables[table]
        .select()
        .filter(db.metatables[table].c.person_id == person_id)
        .order_by(db.metatables[table].c.id.desc())
    )
    items = db.session.execute(stmt).all()
    return jsonify([model.model_validate(table).model_dump() for table in items]), 200


@bp.post("/<item>/<int:person_id>")
@validize()
@auth_required(Roles.user.value)
def post_items(item: Items, person_id: int, json_data: Model) -> Response:
    """Insert or replaces a record in the specified table with the given item ID."""
    json_dict = json_data.dict(exclude_none=True, exclude={"created"})
    json_dict["person_id"] = person_id
    table = validate_item(item)
    # Проверяем, есть ли ключ "id" в словаре json_dict
    if item_id := json_dict.pop("id", None):
        # Если есть, создаем запрос на обновление записи с указанным id
        stmt = (
            db.metatables[table]
            .update()
            .where(db.metatables[table].c.id == item_id)
            .values(json_dict)
        )
    else:
        # Если нет, создаем запрос на вставку новой записи
        stmt = db.metatables[table].insert().values(json_dict)
    db.session.execute(stmt)
    db.session.commit()
    return jsonify({"message": "success"}), 201


@bp.delete("/<item>/<int:item_id>")
@validize()
@auth_required(Roles.user.value)
def delete_items(item: Items, item_id: int) -> Response:
    """Delete an item from the database based on the provided item name and item ID."""
    table = validate_item(item)
    db.session.execute(
        db.metatables[table].delete().where(db.metatables[table].c.id == item_id),
    )
    db.session.commit()
    return jsonify({"message": "success"}), 201
