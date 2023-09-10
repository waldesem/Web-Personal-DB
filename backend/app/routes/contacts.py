from flask import request
from flask_jwt_extended import jwt_required


from . import bp
from ..models.model import db, cache, Organization, Location, Contact, Connect,  Group
from ..models.schema import ContacsBookSchema, OrganizationSchema


@bp.route('/contacts/<group>/<flag>/<int:page>', methods=['GET', 'POST'])
@jwt_required()
@cache.cached(timeout=50)
@bp.doc(hide=True)
def get_contacts(group, flag, page):
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
def view_contact(contact_id):
   
    org = db.session.query(Organization).filter_by(id=contact_id).first()
    locations = db.session.query(Location).filter_by(id=org.id).all()
    contacts = [db.session.query(Contact).filter_by(id=location.id).all() for location in locations]
    connect = [db.session.query(Connect).filter_by(id=contact.id).all() for contact in contacts]

    return {'org': org, 'locations': locations, 'contacts': contacts, 'connect': connect}


@bp.post('/contact/<action>/<item>/<int:item_id>')
@jwt_required()
@bp.doc(hide=True)
@bp.output(ContacsBookSchema)
def edit_contact(action, item, item_id, json_data):
    mapped = {
        'organization': Organization,
        'location': Location,
        'contact': Contact,
        'connect': Connect
    }
    model = mapped.get(item)
    resp = db.session.query(model).filter_by(id=item_id).first()
    if action == 'create' and not resp:
       db.session.add(model(**json_data))
    else:
        for k, v in json_data.items():
            setattr(resp, k, v)
    db.session.commit()

    return {'action': action, 'item': item, 'item_id': item_id}