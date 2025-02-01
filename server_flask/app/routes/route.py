"""Route routes."""

from flask import Blueprint, Response, jsonify, request
from sqlalchemy import desc, func, select

from app.depends.depend import current_user, jwt_required, roles_required, validate
from app.model.classes import Regions, Roles
from app.model.models import Info
from app.model.tables import Checks, Persons, Users, db_session

bp = Blueprint("route", __name__)


@bp.get("/index/<int:page>")
@jwt_required()
def get_index(page: int) -> Response:
    """Retrieve a paginated list of persons from the database.

    Arguments:
        page (int): The page number of the results.

    Returns:
        tuple: A tuple containing the list of persons, a boolean indicating if
        there are more results, and a 200 status code.

    """
    pagination = 11
    search = request.args.get("search")
    stmt = select(Persons, Users.fullname).filter(
        Persons.user_id == Users.id,
        Persons.region == current_user.region
        if current_user.region != Regions.main.value
        else True,
    )
    if search:
        search = search.upper().split(maxsplit=2)[:3]
        stmt = stmt.filter(
            Persons.surname == search[0],
            Persons.firstname == search[1] if len(search) > 1 else True,
            Persons.patronymic == search[2] if len(search) > 2 else True,  # noqa: PLR2004
        )
    query = db_session.execute(
        stmt.order_by(desc(Persons.id))
        .offset((page - 1) * pagination)
        .limit(pagination + 1),
    ).all()
    result = [row[0].to_dict() | {"username": row[1]} for row in query]
    has_next = len(result) > pagination
    return jsonify(
        [result[:pagination] if has_next else result, has_next],
    ), 200


@bp.get("/info")
@validate()
@roles_required(Roles.admin.value)
def get_information(query_data: Info) -> Response:
    """Retrieve the number of conclusion for a given region and period of time.

    Arguments:
        query_data (Info): The query data containing the start and end dates,
        the region, and the user's role.

    Returns:
        list: A list of dictionaries, each containing a conclusion and the number
        of persons with that conclusion.

    """
    results = db_session.execute(
        select(Checks.conclusion, func.count(Checks.id))
        .where(
            Checks.person_id == Persons.id,
            Checks.created.between(query_data.start, query_data.end),
            Persons.region == query_data.region
            if query_data.region
            else current_user.region,
        )
        .group_by(Checks.conclusion),
    ).all()
    return jsonify(
        [{"conclusion": result[0], "count": result[1]} for result in results],
    )
