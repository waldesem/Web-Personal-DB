"""Person routes."""

from pathlib import Path

from flask import Blueprint, Response, g, jsonify

from app import db
from app.classes.classes import Roles
from app.decorators.depend import auth_required
from app.decorators.pydantify import validize
from app.models.models import PersonIn, PersonOut
from app.tables.tables import Persons
from app.utils.utilities import create_destination, upload_resume

bp = Blueprint("persons", __name__)


@bp.get("/persons/<int:person_id>")
@validize()
@auth_required()
def get_person(person_id: int) -> Response:
    """Retrieve an item from the database based on the provided item ID."""
    person = db.session.get(Persons, person_id)
    if not person.destination or not Path(person.destination).exists():
        person.destination = create_destination(person)
        db.session.commit()
    return jsonify(PersonOut.model_validate(person).model_dump()), 200


@bp.post("/persons")
@validize()
@auth_required(Roles.user.value)
def post_person(json_data: PersonIn) -> Response:
    """Replace a record in persons table."""
    # Загружаем резюме, получаем id кандидата, а также был ли он ранее загружен
    cand_id, existed = upload_resume(json_data, g.user.id)
    return jsonify({"person_id": cand_id, "exists": existed}), 201


@bp.delete("/persons/<int:person_id>")
@validize()
@auth_required(Roles.user.value)
def delete_person(person_id: int) -> Response:
    """Delete an item from the database based on the provided item name and item ID."""
    person = db.session.get(Persons, person_id)
    db.session.delete(person)
    db.session.commit()
    return jsonify({"message": "success"}), 201
