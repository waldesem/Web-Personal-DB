from flask import request
from flask_jwt_extended import jwt_required
from flask.views import MethodView

from . import bp
from ..models.model import db, Group, Connect
from ..models.schema import ConnectSchema


class ContactsView(MethodView):

    decorators = [jwt_required(), bp.doc(hide=True)]
    pagination = 16

    def __init__(self) -> None:
        self.datalist = db.session.query(Connect.company, Connect. city).all()
        self.schema = ConnectSchema()
    
    def get(self, group, item):
        group_id = db.session.query(Group.id).filter_by(group=group).scalar()
        query = db.session.query(Connect).filter_by(group_id=group_id). \
                    order_by(Connect.id.desc()).paginate(page=item, 
                                                         per_page=self.pagination, 
                                                         error_out=False)
        datas = self.schema.dump(query, many=True)
        return [datas, 
                {'has_next': int(query.has_next)}, 
                {"has_prev": int(query.has_prev)}, 
                {'companies': [company[0] for company in self.datalist]},  
                {'cities': [city[1] for city in self.datalist]}]

    def post(self, group, item, json_data):
        group_id = db.session.query(Group.id).filter_by(group=group).scalar()
        query = db.session.query(Connect).\
            filter(Connect.company.ilike('%{}%'.format(json_data['company'])),
                   Connect.group_id==group_id).order_by(Connect.id.desc()).\
            paginate(page=item, per_page=self.pagination, error_out=False)
        datas = self.schema.dump(query, many=True)
        return [datas, 
                {'has_next': int(query.has_next)}, 
                {"has_prev": int(query.has_prev)}, 
                {'companies': [company[0] for company in self.datalist]},  
                {'cities': [city[1] for city in self.datalist]}]
    
bp.add_url_rule('/connects/<group>/<int:item>', view_func=ContactsView.as_view('connects'))


class ConnnectView(MethodView):

    decorators = [jwt_required(), bp.doc(hide=True)]
    
    @bp.input(ConnectSchema)
    def post(self, group, json_data):
        group_id = db.session.query(Group.id).filter_by(group=group).scalar()
        connect = Connect(**json_data | {"group_id": group_id})
        db.session.add(connect)
        db.session.flush()
        item = connect.id
        db.session.commit()
        return {'item_id': item}

    @bp.input(ConnectSchema)
    def patch(self, item, json_data):
        resp = db.session.query(Connect).filter_by(id=item).first()
        for k, v in json_data.items():
            setattr(resp, k, v)
        return {'item_id': item}

    def delete(self, item):
        resp = db.session.query(Connect).filter_by(id=item).first()
        db.session.delete(resp)
        return {'item_id': item}


contacts_view = ConnnectView.as_view('connect')
bp.add_url_rule('/connect/<group>', view_func=contacts_view, methods=['POST'])
bp.add_url_rule('/connect/<int:item>', view_func=contacts_view, methods=['PATCH','DELETE'])

