from flask import request
from flask_jwt_extended import jwt_required

from . import bp
from ..models.model import db, cache, Connect, Group
from ..models.schema import ConnectSchema


@bp.route('/contacts/<group>/<flag>/<int:page>', methods=['GET', 'POST'])
@jwt_required()
@cache.cached(timeout=60)
@bp.doc(hide=True)
def get_contacts(group, flag, page):
    """
    Get contacts based on the specified group, flag, and page.

    Parameters:
        group (str): The group parameter.
        flag (str): The flag parameter.
        page (int): The page parameter.

    Returns:
        list: A list containing the contacts data and pagination information.
            The contacts data is a list of dictionaries representing the organizations.
            Each dictionary contains the organization's ID and name.
            The pagination information includes the following keys:
                - has_next (int): 1 if there is a next page, 0 otherwise.
                - has_prev (int): 1 if there is a previous page, 0 otherwise.
    """
    pagination = 16
    group_id = db.session.query(Group.id).filter_by(group=group).first()
    match flag:
        case 'list':
            query = db.session.query(Connect).filter_by(group_id=group_id). \
                paginate(page=page, per_page=pagination, error_out=False)
        case 'search':
            search = request.get_json()
            query = db.session.query(Connect).filter_by(company=search).filter_by(group_id=group_id).\
                paginate(page=page, per_page=pagination, error_out=False)
    
    resume_schema = ConnectSchema()
    datas = resume_schema.dump(query, many=True)
    
    return [datas, {'has_next': int(query.has_next), "has_prev": int(query.has_prev)}]


@bp.route('/contact/<action>/<int:item_id>')
@jwt_required()
@bp.doc(hide=True)
def update_contact(action, item_id):
    resp = db.session.query(Connect).filter_by(id=item_id).first()
    if action == 'delete':
        db.session.delete(resp)
    else:
        data = request.get_json()
        schema = ConnectSchema
        json_data = schema.dump(data)
        
        if action == 'create' and not resp:
            connect = Connect(**json_data)
            db.session.add(connect)
            db.session.flush()
            item_id = connect.id
        else:    
            for k, v in json_data.items():
                setattr(resp, k, v)
    db.session.commit()

    return {'action': action, 'item_id': item_id}