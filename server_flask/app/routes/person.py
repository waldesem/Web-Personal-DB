"""Person routes."""

from flask import Blueprint, Response, current_app, g, redirect
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.classes.classes import Roles
from app.decorators.depend import auth_required
from app.decorators.validize import pydantify
from app.models.models import PersonIn, PersonOut, ResumeResponse
from app.tables.tables import Persons
from app.utils.utilities import upload_resume

bp = Blueprint("persons", __name__)


@bp.get("/persons/<int:person_id>")
@pydantify(PersonOut, orm=True)
@auth_required()
def get_person(person_id: int) -> tuple[Persons, int] | Response:
    """Retrieve an item from the database based on the provided item ID."""
    if person := db.session.get(Persons, person_id):
        return person, 200
    return redirect("/", 302)


@bp.post("/persons")
@pydantify(ResumeResponse)
@auth_required(Roles.user.value)
def post_person(json_data: PersonIn) -> tuple[dict, int]:
    """Replace a record in persons table."""
    # Загружаем резюме, получаем id кандидата, а также был ли он ранее загружен
    cand_id, existed = upload_resume(json_data, g.user.id)
    return {"person_id": cand_id, "exists": existed}, 201


@bp.delete("/persons/<int:person_id>")
@pydantify(ResumeResponse)
@auth_required(Roles.user.value)
def delete_person(person_id: int) -> tuple[dict, int]:
    """Delete an item from the database based on the provided item name and item ID."""
    try:
        person = db.session.get(Persons, person_id)
        db.session.delete(person)
        db.session.commit()
    except SQLAlchemyError:
        current_app.logger.exception("Database error")
        db.session.rollback()
        return {"message": "error"}, 200
    else:
        return {"message": "success"}, 201
