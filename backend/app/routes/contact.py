from flask.views import MethodView
from sqlalchemy_searchable import search
from sqlalchemy import select

from config import Config
from . import bp
from .login import roles_required
from ..models.classes import Roles
from ..models.model import db, Connect
from ..models.schema import ConnectSchema, SearchSchema


class ConnnectView(MethodView):

    decorators = [roles_required(Roles.user.value), bp.doc(hide=True)]

    @bp.input(SearchSchema, location="query")
    def get(self, page, query_data):
        """
        Retrieves a paginated list of Connect objects based on the specified group and item.
        """
        names = db.session.execute(select(Connect.name)).scalars()
        companies = db.session.execute(select(Connect.company)).scalars()
        cities = db.session.execute(select(Connect.city)).scalars()
        search_data = query_data.get("search")
        query = select(Connect).order_by(Connect.id.desc())
        if search_data:
            query = search(query,"%{}%".format(search_data))
        result = db.paginate(
            query, 
            page=page, 
            per_page=Config.PAGINATION, 
            error_out=False
            )
        return [
            ConnectSchema().dump(result, many=True),
            {"has_prev": result.has_prev},
            {"has_next": result.has_next},
            {"names": list({name for name in names})},
            {"companies": list({company for company in companies})},
            {"cities": list({city for city in cities})},
        ], 200

    @bp.input(ConnectSchema)
    def post(self, json_data):
        """
        Create a new connection.
        """
        db.session.add(Connect(**json_data))
        db.session.commit()
        return {"message": "Created"}, 201

    @bp.input(ConnectSchema)
    def patch(self, item_id, json_data):
        """
        Patch an item in the Connect table.
        """
        print(json_data)
        resp = db.session.get(Connect, item_id)
        for k, v in json_data.items():
            setattr(resp, k, v)
        db.session.commit()
        return {"message": "Updated"}, 201

    def delete(self, item_id):
        """
        Deletes an item from the database.
        """
        resp = db.session.get(Connect, item_id)
        db.session.delete(resp)
        db.session.commit()
        return {"message": "Deleted"}, 204


contacts_view = ConnnectView.as_view("connect")
bp.add_url_rule("/connect/<int:page>", view_func=contacts_view, methods=["GET"])
bp.add_url_rule("/connect", view_func=contacts_view, methods=["POST"])
bp.add_url_rule(
    "/connect/<int:item_id>",
    view_func=contacts_view,
    methods=["PATCH", "DELETE"],
)
