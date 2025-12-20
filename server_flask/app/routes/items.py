"""Items routes."""

from flask import Blueprint, Response, jsonify

from app import db
from app.classes.classes import Roles
from app.decorators.depend import auth_required
from app.decorators.pydantify import validize
from app.models.models import Items, Model, models

bp = Blueprint("items", __name__, url_prefix="/items")


def select_item(item: Items, person_id: int) -> list:
    """Retrieve an item from the database based on the provided item."""
    stmt = (
        db.metatables[item]
        .select()
        .filter(db.metatables[item].c.person_id == person_id)
        .order_by(db.metatables[item].c.id.desc())
    )
    items = db.session.execute(stmt).all()
    return [models[item].model_validate(table).model_dump() for table in items]


@bp.get("/<int:person_id>")
@auth_required()
def get_items(person_id: int) -> Response:
    """Retrieve an all items from the database."""
    return jsonify({item: select_item(item, person_id) for item in models}), 200


@bp.get("/<item>/<int:person_id>")
@validize()
@auth_required()
def get_item(item: Items, person_id: int) -> Response:
    """Get an item based on the provided item."""
    return jsonify(select_item(item, person_id)), 200


@bp.post("/<item>/<int:person_id>")
@validize()
@auth_required(Roles.user.value)
def post_item(item: Items, person_id: int, json_data: Model) -> Response:
    """Insert or replaces a record in the specified table with the given item ID."""
    json_dict = json_data.dict(exclude_none=True, exclude={"created"})
    json_dict["person_id"] = person_id
    # Проверяем, есть ли ключ "id" в словаре json_dict
    if item_id := json_dict.pop("id", None):
        # Если есть, создаем запрос на обновление записи с указанным id
        stmt = (
            db.metatables[item]
            .update()
            .where(db.metatables[item].c.id == item_id)
            .values(json_dict)
        )
    else:
        # Если нет, создаем запрос на вставку новой записи
        stmt = db.metatables[item].insert().values(json_dict)
    db.session.execute(stmt)
    db.session.commit()
    return jsonify({"message": "success"}), 201


@bp.delete("/<item>/<int:item_id>")
@validize()
@auth_required(Roles.user.value)
def delete_item(item: Items, item_id: int) -> Response:
    """Delete an item from the database based on the provided item name and item ID."""
    db.session.execute(
        db.metatables[item].delete().where(db.metatables[item].c.id == item_id),
    )
    db.session.commit()
    return jsonify({"message": "success"}), 201
