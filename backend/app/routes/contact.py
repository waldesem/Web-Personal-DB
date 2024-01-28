from flask_jwt_extended import jwt_required
from flask.views import MethodView
from sqlalchemy import select

from . import bp
from .. import db
from ..models.model import Connect
from ..models.schema import ConnectSchema, SearchSchema


class ContactsView(MethodView):
    decorators = [jwt_required(), bp.doc(hide=True)]

    @bp.input(SearchSchema)
    def post(self, page, json_data):
        """
        Retrieves a paginated list of Connect objects based on the specified group and item.
        """
        schema = ConnectSchema()
        companies = db.session.execute(select(Connect.company)).scalars()
        cities = db.session.execute(select(Connect.city)).scalars()
        if json_data["search"]:
            query = Connect.query.search("%{}%".format(json_data["search"]))
        else:
            query = select(Connect)
        result = query.order_by(Connect.id.desc())
        result = db.paginate(query, page=page, per_page=16, error_out=False)
        return [
            schema.dump(result, many=True),
            {"has_next": result.has_next},
            {"has_prev": result.has_prev},
            {"companies": list({company for company in companies})},
            {"cities": list({city for city in cities})},
        ], 200


bp.add_url_rule("/connects/<int:page>", view_func=ContactsView.as_view("connects"))


class ConnnectView(MethodView):
    decorators = [jwt_required(), bp.doc(hide=True)]

    @bp.input(ConnectSchema)
    def post(self, json_data):
        """
        Create a new connection.
        """
        connect = Connect(**json_data)
        db.session.add(connect)
        db.session.commit()
        return {"message": "Created"}, 201

    @bp.input(ConnectSchema)
    def patch(self, item_id, page, json_data):
        """
        Patch an item in the Connect table.
        """
        resp = db.session.get(Connect, item_id)
        for k, v in json_data.items():
            setattr(resp, k, v)
        db.session.commit()
        return {"message": "Updated"}, 201

    def delete(self, page, item_id):
        """
        Deletes an item from the database.
        """
        resp = db.session.get(Connect, item_id)
        db.session.delete(resp)
        db.session.commit()
        return {"message": "Deleted"}, 204


contacts_view = ConnnectView.as_view("connect")
bp.add_url_rule("/connect", view_func=contacts_view, methods=["POST"])
bp.add_url_rule(
    "/connect/<int:page>/<int:item_id>",
    view_func=contacts_view,
    methods=["PATCH", "DELETE"],
)
