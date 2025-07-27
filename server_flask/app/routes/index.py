"""Route routes."""

from flask import Blueprint, current_app
from sqlalchemy import desc, func, select
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.decorators.depend import auth_required
from app.decorators.validize import pydantify
from app.models.models import Candidates, Index
from app.tables.tables import Persons, Users

bp = Blueprint("route", __name__)


@bp.get("/index")
@pydantify(Candidates, orm=True, many=True)
@auth_required()
def get_index(json_query: Index) -> tuple[list[Persons], int]:
    """Retrieve a paginated list of persons from the database."""
    try:
        stmt = select(
            Persons.id,
            # Получение полного имени кандидата
            (
                Persons.surname
                + " "
                + Persons.firstname
                + " "
                + func.coalesce(Persons.patronymic, "")
            ).label("fullname"),
            Persons.birthday,
            Persons.editable,
            Persons.created,
            Users.fullname.label("username"),
            func.count().over().label("total"),
        ).filter(
            Users.id == Persons.user_id,
        )
        if json_query.search:
            search = json_query.search.upper().split(maxsplit=3)[:3]
            stmt = stmt.where(
                Persons.surname == search[0],
                Persons.firstname == search[1] if len(search) > 1 else True,
                Persons.patronymic == search[2] if len(search) > 2 else True,
            )
        # Пагинация списка кандидатов
        result = db.session.execute(
            stmt.order_by(desc(Persons.id)).slice(
                (json_query.page - 1) * json_query.per_page,
                json_query.per_page * json_query.page,
            ),
        ).all()

    except SQLAlchemyError:
        current_app.logger.exception("SQL Error")
        return [], 400
    else:
        return result, 200
