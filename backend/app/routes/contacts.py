from flask import request
from flask_jwt_extended import jwt_required

from . import bp
from ..models.model import db, Group, Connect
from ..models.schema import ConnectSchema


@bp.route('/contacts/<group>/<flag>/<int:page>', methods=['GET', 'POST'])
@jwt_required()
@bp.doc(hide=True)
def get_contacts(group, flag, page):
    """
    Get contacts based on the specified group, flag, and page.
    """
    pagination = 16
    group_id = db.session.query(Group.id).filter_by(group=group).scalar()
    match flag:
        case 'list':
            query = db.session.query(Connect).filter_by(group_id=group_id). \
                order_by(Connect.id.desc()).paginate(page=page, per_page=pagination, error_out=False)
        case 'search':
            search = request.get_json()
            query = db.session.query(Connect).filter(Connect.company.ilike('%{}%'.format(search['company'])))\
                .filter_by(group_id=group_id).order_by(Connect.id.desc()).\
                    paginate(page=page, per_page=pagination, error_out=False)
    resume_schema = ConnectSchema()
    datas = resume_schema.dump(query, many=True)
    datalist = db.session.query(Connect.company, Connect. city).all()

    return [datas, {'has_next': int(query.has_next)}, {"has_prev": int(query.has_prev)}, 
            {'companies': [company[0] for company in datalist]},  {'cities': [city[1] for city in datalist]}]


@bp.route('/contact/<group>/<action>/<int:item_id>', methods=['DELETE', 'POST'])
@jwt_required()
@bp.doc(hide=True)
def update_contact(group, action, item_id):
    if action == 'delete':
        resp = db.session.query(Connect).filter_by(id=item_id).first()
        db.session.delete(resp)
    else:
        data = request.get_json()
        schema = ConnectSchema()
        json_dumped = schema.dump(data)
        if action == 'create':
            group_id = db.session.query(Group.id).filter_by(group=group).scalar()
            connect = Connect(**json_dumped | {"group_id": group_id})
            db.session.add(connect)
            db.session.flush()
            item_id = connect.id
        else:
            resp = db.session.query(Connect).filter_by(id=item_id).first()
            for k, v in json_dumped.items():
                setattr(resp, k, v)
    db.session.commit()

    return {'action': action, 'item_id': item_id}