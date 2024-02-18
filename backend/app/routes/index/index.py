from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy_searchable import search
from sqlalchemy import select, func

from . import bp_index
from ... import db
from ..login.login import group_required
from ...models.classes import Categories, Groups, Statuses
from ..resume.resume import ResumeView
from ..anketa.anketa import (
    StaffView,
    DocumentView,
    ContactView,
    AddressView,
    WorkplaceView,
    AffilationView,
    RelationView,
)
from ..checks.checks import(
    CheckView,
    RobotView,
    PoligrafView,
    InvestigationView,
    InquiryView,
)
from ...models.model import (
    Category,
    Person,
    Check,
    Status,
)
from ...models.schema import (
    InfoSchema,
    PersonSchema,
    SearchSchema,
)


class IndexView(MethodView):

    decorators = [
        group_required(Groups.staffsec.value),
        bp_index.doc(hide=True),
    ]

    @bp_index.input(SearchSchema, location="query")
    def get(self, flag, page, query_data):
        search_data = query_data.get("search")
        query = select(Person).order_by(Person.id.desc())
        if flag != "search":
            match flag:
                case "new":
                    query = query.filter(
                        Person.status_id.in_(
                            [
                                Status().get_id(Statuses.new.value),
                                Status().get_id(Statuses.update.value),
                                Status().get_id(Statuses.repeat.value),
                            ]
                        ),
                        Person.category_id
                        == Category().get_id(Categories.candidate.value),
                    )
                case "officer":
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
                query = search(query,"%{}%".format(search_data))

        result = db.paginate(query, page=page, per_page=16, error_out=False)
        return [
            PersonSchema().dump(result, many=True),
            {"has_next": bool(result.has_next), "has_prev": bool(result.has_prev)},
        ]


bp_index.add_url_rule("/index/<flag>/<int:page>", view_func=IndexView.as_view("index"))


class InfoView(MethodView):

    @group_required(Groups.staffsec.value)
    @bp_index.input(InfoSchema, location="query")
    @bp_index.doc(hide=True)
    def get(self, json_data):
        candidates = db.session.execute(
            select(Check.conclusion_id, func.count(Check.id))
            .join(Person)
            .group_by(Check.conclusion_id)
            .filter(Person.region_id == json_data["region_id"])
            .filter(Check.deadline.between(json_data["start"], json_data["end"]))
        ).all()
        return {"candidates": dict(map(lambda x: (x[1], x[0]), candidates))}, 200


bp_index.add_url_rule("/information", view_func=InfoView.as_view("information"))
