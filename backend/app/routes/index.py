import os

from flask import send_file
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy_searchable import search
from sqlalchemy import func, select

from config import Config
from . import bp
from .login import roles_required
from ..models.classes import Roles, Statuses
from ..models.model import (
    db,
    Person,
    Check,
    Status,
)
from ..models.schema import (
    InfoSchema,
    PersonSchema,
    SearchSortSchema,
)


class IndexView(MethodView):

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    @bp.input(SearchSortSchema, location="query")
    def get(self, flag, page, query_data):
        query = select(Person)
        search_data = query_data.get("search")
        sort = query_data.get("sort")
        order = query_data.get("order")
        if order == "asc":
            query = query.order_by(Person[sort].asc())
        else:
            query = query.order_by(Person[sort].desc())
        if flag == "officer":
            query = query.filter(
                Person.status_id.notin_(
                    [
                        Status().get_id(Statuses.finish.value),
                        Status().get_id(Statuses.cancel.value),
                    ]
                ),
                Person.user_id == current_user.id,
            )
        else:
            if search_data:
                query = search(query, "%{}%".format(search_data))

        result = db.paginate(query, page=page, per_page=16, error_out=False)
        return [
            PersonSchema().dump(result, many=True),
            {"has_next": bool(result.has_next), "has_prev": bool(result.has_prev)},
        ]


index_view = IndexView.as_view("index")
bp.add_url_rule("/index/<flag>/<int:page>", view_func=index_view)


@roles_required(Roles.user.value)
@bp.doc(hide=True)
@bp.route("/image/<int:item_id>")
def get_image(item_id):
    """
    Retrieves a file from the server and sends it as a response.
    """
    person = db.session.get(Person, item_id)
    if person.path:
        file_path = os.path.join(Config.BASE_PATH, person.path, "image", "image.jpg")
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True, mimetype="image/jpg")
    return send_file(Config.NO_PHOTO, as_attachment=True, mimetype="image/jpg")


@roles_required(Roles.user.value)
@bp.get("/information")
@bp.input(InfoSchema, location="query")
def get_information(query_data):
    candidates = db.session.execute(
        select(Check.conclusion_id, func.count(Check.id))
        .join(Person)
        .group_by(Check.conclusion_id)
        .filter(Person.region_id == query_data["region_id"])
        .filter(Check.deadline.between(query_data["start"], query_data["end"]))
    ).all()
    return dict(map(lambda x: (x[1], x[0]), candidates)), 200
