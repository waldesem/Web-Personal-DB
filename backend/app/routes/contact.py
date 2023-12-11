from apiflask import EmptySchema
from flask import request
from flask_jwt_extended import jwt_required
from flask.views import MethodView
from sqlalchemy import select

from . import bp
from .. import db
from ..models.model import Connect
from ..models.schema import ConnectSchema


class ContactsView(MethodView):

    decorators = [jwt_required(), bp.doc(hide=True)]

    def post(self, group, item):
        """
        Retrieves a paginated list of Connect objects based on the specified group and item.
        """
        schema = ConnectSchema()
        response = request.get_json()
        datalist = db.session.execute(
            select(Connect.company, Connect.city)
        ).scalars()
        if response['search']:
            query = Connect.query.search('%{}%'.format(response['search']))
        else:
            query = db.session.execute(select(Connect))

        result = query.order_by(Connect.id.desc()).\
                paginate(page=item, per_page=16, error_out=False) 
        return [schema.dump(result, many=True),
                {'has_next': int(result.has_next)},
                {'has_prev': int(result.has_prev)},
                {'companies': list({company[0] for company in datalist})},
                {'cities': list({city[1] for city in datalist})}]

bp.add_url_rule('/connects/<group>/<int:item>', view_func=ContactsView.as_view('connects'))


class ConnnectView(MethodView):

    decorators = [jwt_required(), bp.doc(hide=True)]

    @bp.input(ConnectSchema)
    def post(self, group, json_data):
        """
        Create a new connection.
        """
        connect = Connect(**json_data)
        db.session.add(connect)
        db.session.flush()
        item = connect.id
        db.session.commit()
        return {'item_id': item}
    
    @bp.input(ConnectSchema)
    def patch(self, item, json_data):
        """
        Patch an item in the Connect table.
        """
        resp = db.session.execute(
            select(Connect)
            .filter_by(id=item)
            ).first()
        for k, v in json_data.items():
            setattr(resp, k, v)
        db.session.commit()
        return {'item_id': item}
    
    @bp.output(EmptySchema, status_code=204)
    def delete(self, item):
        """
        Deletes an item from the database.
        """
        resp = db.session.execute(
            select(Connect)
            .filter_by(id=item)
            ).one_or_none()
        db.session.delete(resp)
        db.session.commit()
        return ''
    
contacts_view = ConnnectView.as_view('connect')
bp.add_url_rule('/connect/<group>', view_func=contacts_view, methods=['POST'])
bp.add_url_rule('/connect/<int:item>', view_func=contacts_view, methods=['PATCH', 'DELETE'])