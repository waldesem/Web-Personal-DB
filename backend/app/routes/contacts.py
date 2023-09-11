from flask import request
from flask_jwt_extended import jwt_required

from . import bp
from ..models.model import db, cache, Organization, Location, Contact, Connect,  Group
from ..models.schema import ConnectSchema, ContacsBookSchema, ContactSchema, LocationSchema, OrganizationSchema


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
@cache.cached(timeout=60)
@bp.doc(hide=True)
@bp.output(ContacsBookSchema)
def view_contact(contact_id):
    """
    Retrieves a contact from the database by its ID and returns the contact information along with its associated organization, locations, and connections.
    Parameters:
        contact_id (int): The ID of the contact to retrieve.
    Returns:
        dict: A dictionary containing the contact information, the associated organization, a list of locations, and a list of connections.
    Raises:
        None
    """
    org = db.session.query(Organization).filter_by(id=contact_id).first()
    location = db.session.query(Location).filter_by(id=org.id).all()
    connect = [db.session.query(Connect).filter_by(id=loc.id).all() for loc in location]
    contact = [db.session.query(Contact).filter_by(id=conn.id).all() for conn in connect]

    return {'org': org, 'locations': location, 'connect': connect, 'contacts': contact}


@bp.post('/contact/<action>/<item>/<int:item_id>')
@jwt_required()
@bp.doc(hide=True)
def edit_contact(action, item, item_id):
    """
    Edit a contact in the contacts book.
    Parameters:
        - action (str): The action to perform on the contact.
        - item (str): The type of item to edit (organization, location, contact, connect).
        - item_id (int): The ID of the item to edit.
        - json_data (dict): The data to update the contact with.
    Returns:
        dict: A dictionary containing the action, item, and item_id of the edited contact.
    """
    mapped = {
        'organization': [Organization, OrganizationSchema],
        'location': [Location, LocationSchema],
        'contact': [Contact, ContactSchema],
        'connect': [Connect, ConnectSchema]
    }
    data = request.get_json()
    model = mapped[item][0]
    schema = mapped[item][1]
    verified = schema.dump(data)
    resp = db.session.query(model).filter_by(id=item_id).first()
    if action == 'create' and not resp:
       db.session.add(model(**verified))
    elif action == 'delete':
        db.session.delete(resp)
    else:
        for k, v in verified.items():
            setattr(resp, k, v)
    db.session.commit()

    return {'action': action, 'item': item, 'item_id': item_id}