from flask import request
from flask_jwt_extended import jwt_required


from . import bp
from ..models.model import db, cache, Organization, Location, Contact, Connection,  Group
from ..models.schema import ContacsBookSchema, OrganizationSchema
from ..models.classes import Groups


@bp.route('/contacts/<group>/<flag>/<int:page>', methods=['GET', 'POST'])
@jwt_required()
@cache.cached(timeout=50)
@bp.doc(hide=True)
def get_contact(group, flag, page):
    pagination = 16
    group_id = db.session.query(Group.id).filter_by(group=group).first()
    match flag:
        case 'main':
            query = db.session.query(Organization).filter_by(group_id=group_id). \
                paginate(page=page, per_page=pagination, error_out=False)
        case 'search':
            search = request.get_json()
            query = db.session.query(Organization.id, Organization.name).filter_by(name=search).\
                    paginate(page=page, per_page=pagination, error_out=False)
    
    resume_schema = OrganizationSchema()
    datas = resume_schema.dump(query, many=True)
    has_next, has_prev = int(query.has_next), int(query.has_prev)
    
    return [datas, {'has_next': has_next, "has_prev": has_prev}]


@bp.get('/contact/<int:contact_id>')
@jwt_required()
@cache.cached(timeout=50)
@bp.doc(hide=True)
@bp.output(ContacsBookSchema)
def get_profile(contact_id):
   
    query = db.session.query(Organization).filter_by(id=contact_id).\
                    join(Location).join(Contact).join(Connection).first()

    return query