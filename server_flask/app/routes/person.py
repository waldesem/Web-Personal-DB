"""Person routes."""

from flask import Blueprint, current_app
from sqlalchemy.exc import SQLAlchemyError

from app import caching, db
from app.classes.classes import Roles
from app.decorators.depend import auth_required
from app.decorators.validize import pydantify
from app.models.models import PersonIn, PersonOut, ResumeModel
from app.tables.tables import Persons
from app.utils.utilities import upload_resume

bp = Blueprint("persons", __name__)


@bp.get("/persons/<int:person_id>")
@pydantify(PersonOut, orm=True)
@auth_required()
def get_person(person_id: int) -> tuple[Persons, int]:
    """Retrieve an item from the database based on the provided item ID."""
    if caching_data := caching.get_data(person_id):
        return caching_data
    person = db.session.get(Persons, person_id), 200
    caching.set_data(person_id, person)
    return person


@bp.post("/persons")
@pydantify(ResumeModel)
@auth_required(Roles.user.value)
def post_person(json_data: PersonIn) -> tuple[dict, int]:
    """Replace a record in persons table."""
    # Загружаем резюме, получаем id кандидата, а также был ли он ранее загружен
    cand_id, existed = upload_resume(json_data)
    caching.set_data(cand_id)
    return {"person_id": cand_id, "exists": existed}, 201


@bp.delete("/persons/<int:person_id>")
@pydantify(ResumeModel)
@auth_required(Roles.user.value)
def delete_person(person_id: int) -> tuple[str, int]:
    """Delete an item from the database based on the provided item name and item ID."""
    try:
        person = db.session.get(Persons, person_id)
        db.session.delete(person)
        db.session.commit()
    except SQLAlchemyError:
        current_app.logger.exception("Database error")
        db.session.rollback()
        return {"message": "error"}, 400
    else:
        caching.delete_data(person_id)
        return {"message": "success"}, 201
