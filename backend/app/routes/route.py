import json
import os
from datetime import datetime
import shutil
import requests

from flask import request, send_from_directory
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import func, or_
from PIL import Image
from werkzeug.exceptions import BadRequest

from . import bp
from . login import roles_required, group_required
from ..utils.excel import ExcelFile, resume_data
from ..models.model import User, db, Person, Staff, Document, Address, Contact, Workplace, \
    Check, Registry, Poligraf, Investigation, Inquiry, Relation, Status, Report, Region
from ..models.schema import MessagesListSchema, RelationSchema, StaffSchema, AddressSchema, \
        PersonSchema, ProfileSchema, ContactSchema, DocumentSchema, CheckSchema, InquirySchema, \
            InvestigationSchema, PoligrafSchema, RegistrySchema, WorkplaceSchema, AnketaSchema, FileSchema
from ..models.classes import Category, Conclusions, Decisions, Roles, Groups, Status

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'persons'))

bp.static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))


@bp.get('/', defaults={'path': ''})
@bp.get('/<path:path>')
@bp.get('/index/profile/<path:path>')
@bp.doc(hide=True)
def main(path=''):
    """
    Get the file from the specified path in the static folder and return it, or return the index.html file if the path is not found.
    Parameters:
        path (str): The path of the file to retrieve from the static folder. Defaults to an empty string if no path is provided.
    Returns:
        Response: The file from the specified path in the static folder, or the index.html file if the path is not found.
    """
    if path and os.path.exists(os.path.join(bp.static_folder, path)):
        return send_from_directory(bp.static_folder, path)
    else:
        return bp.send_static_file('index.html')
    
    
@bp.get('/classify')
@bp.doc(hide=True)
def get_classes():
    """
    Get the classification data.
    This function retrieves the classification data for the API. It returns a dictionary 
    containing the values of the different status options, role options, conclusions,
    decisions, categories, groups and roles 
    """
    return [{i.name: i.value for i in Status}, 
            {rgn[0]: rgn[1] for rgn in db.session.query(Region.id, Region.region).all()}, 
            {i.name: i.value for i in Conclusions}, 
            {i.name: i.value for i in Decisions}, 
            {i.name: i.value for i in Category},
            {i.name: i.value for i in Groups},
            {i.name: i.value for i in Roles}]


@bp.get('/messages/<string:flag>')
@bp.doc(hide=True)
@bp.output(MessagesListSchema)
@jwt_required()
def get_messages(flag):
    """
    Retrieves messages based on a flag.
    Args:
        flag (str): The flag to determine the type of messages to retrieve.
    Returns:
        list: A list of messages retrieved based on the flag.
    """
    def update_messages():
        updates = db.session.query(Report).filter(Report.status == Status.new.value, 
                                                  Report.user_id == current_user.id).limit(12).all()
        return updates
    
    messages = update_messages()
    
    if flag == 'reply':
        for message in messages:
             db.session.delete(message)
        db.session.commit()
        messages = update_messages()

    return messages


@bp.route('/index/<flag>/<int:page>', methods=['GET', 'POST'])
@bp.doc(hide=True)
@jwt_required()
def index(flag, page):
    """
    This function handles the index route of the API. It takes in two parameters:
    - flag: a string representing the flag indicating the type of query to perform
    - page: an integer representing the page number for pagination
    The function returns a list containing the serialized datas and a dictionary with the has_next and has_prev values.
    """
    pagination = 16
    location_id = db.session.query(User.region_id).filter_by(username=current_user.username).scalar()
    match flag:
        case 'main':
            if location_id == 1:
                query = db.session.query(Person).order_by(Person.id.desc()). \
                    paginate(page=page, per_page=pagination, error_out=False)
            else:
                query = db.session.query(Person).filter_by(region_id=location_id).order_by(Person.id.desc()). \
                    paginate(page=page, per_page=pagination, error_out=False)
        
        case 'new':
            if location_id == 1:
                query = db.session.query(Person).filter(Person.status.in_([Status.new.value, Status.update.value, Status.repeat.value]), 
                                                    Person.region_id == location_id, Person.category == Category.candidate.value).\
                    order_by(Person.id.desc()).paginate(page=page, per_page=pagination, error_out=False)
            else:
                query = db.session.query(Person).filter(Person.status.in_([Status.new.value, Status.update.value, Status.repeat.value]), 
                                                    Person.region_id == location_id, Person.category == Category.candidate.value).\
                    order_by(Person.id.desc()).paginate(page=page, per_page=pagination, error_out=False)
        
        case 'officer': 
            query = db.session.query(Person).filter(Person.status.notin_(
                [Status.finish.value, Status.result.value, Status.cancel.value])). \
                    join(Check, isouter=True).filter_by(officer=current_user.username).order_by(Person.id.asc()). \
                        paginate(page=page, per_page=pagination, error_out=False)
        
        case 'search':
            search = request.get_json()
            if location_id == 1:
                query = db.session.query(Person).filter(
                    or_(Person.fullname.ilike('%{}%'.format(search['fullname'])), search['fullname'] == ''),
                    or_(Person.birthday == search['birthday'] if search['birthday'] else True),
                    ).order_by(Person.id.asc()).\
                        paginate(page=page, per_page=pagination, error_out=False)
            else:
                query = db.session.query(Person).filter(
                or_(Person.fullname.ilike('%{}%'.format(search['fullname'])), search['fullname'] == ''),
                or_(Person.birthday == search['birthday']),
                Person.region_id == location_id).order_by(Person.id.asc()).\
                    paginate(page=page, per_page=pagination, error_out=False)
    
    resume_schema = PersonSchema()
    datas = resume_schema.dump(query, many=True)
    has_next, has_prev = int(query.has_next), int(query.has_prev)
    
    return [datas, {'has_next': has_next, "has_prev": has_prev}]


@bp.get('/profile/<int:person_id>')
@bp.doc(hide=True)
@bp.output(ProfileSchema)
@jwt_required()
def get_profile(person_id):
    """
    Retrieves the profile information for a specific person.
    Parameters:
        person_id (int): The ID of the person.
    Returns:
        dict: A dictionary containing the profile information of the person.
    """
    resume = db.session.query(Person).filter_by(id=person_id).one_or_none()
    
    documents = db.session.query(Document).filter_by(person_id=person_id).order_by(Document.person_id.asc()).all()
    
    addresses = db.session.query(Address).filter_by(person_id=person_id).order_by(Address.id.asc()).all()
    
    contacts = db.session.query(Contact).filter_by(person_id=person_id).order_by(Contact.id.asc()).all()
    
    workplaces = db.session.query(Workplace).filter_by(person_id=person_id).order_by(Workplace.id.asc()).all()
    
    relations = db.session.query(Relation).filter_by(person_id=person_id).order_by(Relation.id.asc()).all()
    
    staffs = db.session.query(Staff).filter_by(person_id=person_id).order_by(Staff.id.asc()).all()
    
    checks = db.session.query(Check).filter_by(person_id=person_id).order_by(Check.id.desc()).all()

    registries = [db.session.query(Registry).filter_by(check_id=check.id).first() for check in checks]
    
    pfos = db.session.query(Poligraf).filter_by(person_id=person_id).order_by(Poligraf.id.desc()).all()
    
    invs = db.session.query(Investigation).filter_by(person_id=person_id).order_by(Investigation.id.desc()).all()
    
    inquiries = db.session.query(Inquiry).filter_by(person_id=person_id).order_by(Inquiry.id.desc()).all()  

    return {'resume': resume, 'documents': documents, 'addresses': addresses, 'contacts': contacts, 
            'workplaces': workplaces, 'staffs': staffs, 'relations': relations, 'checks': checks, 
            'registries': registries, 'pfos': pfos, 'invs': invs, 'inquiries': inquiries}


@bp.post('/anketa/upload')
@bp.doc(hide=True)
@jwt_required()
@bp.input(FileSchema, location='files')
def upload_file(files_data):
    """
    Uploads a file and adds the resume data to the database.
    Returns:
        A dictionary containing the result of the upload and the person ID.
    """
    file = files_data['file']
    excel = ExcelFile(file)
    location_id = db.session.query(User.region_id).filter_by(username=current_user.username).scalar()

    person_id, result = add_resume(excel.resume, location_id, 'create')
    resume_data(person_id, excel.passport, excel.addresses, excel.contacts, excel.workplaces, excel.staff)

    return {'result': bool(result), 'person_id': person_id}


@bp.post('/resume/<action>')
@bp.input(PersonSchema)
@bp.doc(hide=True)
@jwt_required()
def post_resume(action, json_data):
    """
    Creates a new resume for a person.
    Parameters:
        - response: The input data for creating the resume. (PersonSchema)
    Returns:
        - A dictionary containing the person_id and the result of the resume creation. (dict)
    """
    location_id = db.session.query(User.region_id).filter_by(username=current_user.username).scalar()
    person_id, result = add_resume(json_data, location_id, action)
    return {'person_id': person_id, 'result': result}


def add_resume(resume: dict, location_id, action):
    """
    Adds a resume to the database.
    Args:
        resume (dict): A dictionary containing the resume information.
        location_id: The ID of the location where the resume is being added.
    Returns:
        list: A list containing the person ID and a boolean indicating if the person already exists in the database.
    """
    result = db.session.query(Person).filter(Person.fullname.ilike(resume['fullname']),
                                             Person.birthday==resume['birthday']).one_or_none()
    if result:
        if action == "create" or action == 'api':
            resume.update({'status': Status.repeat.value, 'region_id': location_id})
        else:
            resume.update({'status': Status.update.value, 'region_id': location_id})
        for k, v in resume.items():
            setattr(result, k, v)
        person_id = result.id
        
        if result.path and not os.path.isdir(result.path):
            os.mkdir(result.path)
        elif not result.path:
            new_path = os.path.join(BASE_PATH, f'{person_id}-{resume["fullname"]}')
            if not os.path.isdir(new_path):
                os.mkdir(new_path)
            result.path = new_path
    else:
        person = Person(**resume | {'region_id': location_id})
        db.session.add(person)
        db.session.flush()
        person_id = person.id
        
        path = os.path.join(BASE_PATH, f'{person_id}-{resume["fullname"]}')
        person.path = path
        if not os.path.isdir(path):
            os.mkdir(path)
        
    db.session.commit()
    return [person_id, bool(result)]


@bp.post('/profile/staff/<action>/<int:id>')
@bp.doc(hide=True)
@bp.input(StaffSchema)
@jwt_required()
def post_staff(action, id, json_data):
    """
    Create or update a staff profile.
    Parameters:
        action (str): The action to perform. Possible values are 'create' or 'update'.
        id (int): The ID of the staff member.
        response (dict): The response data containing the staff profile information.
    Returns:
        dict: A dictionary containing the action performed and the ID of the staff member.
    """
    if action == 'create':
        db.session.add(Staff(**json_data | {'person_id': id}))
    else:
        for k, v in json_data.items():
            setattr(db.session.query(Staff).get(id), k, v)
    db.session.commit()
    return {'table': 'staff', 'actions': action, 'id': id}


@bp.post('/profile/document/<action>/<int:id>')
@bp.doc(hide=True)
@bp.input(DocumentSchema)
@jwt_required()
def post_document(action, id, json_data):
    """
    Create or update a document based on the specified action and ID.
    Args:
        action (str): The action to perform. Valid values are 'create' and 'update'.
        id (int): The ID of the document.
        response (dict): The response data containing the document attributes.
    Returns:
        dict: A dictionary containing the table name, action performed, and ID of the document.
    """
    if action == 'create':
        db.session.add(Document(**json_data | {'person_id': id}))
    else:
        for k, v in json_data.items():
            setattr(db.session.query(Document).get(id), k, v)
    db.session.commit()
    return {'table': 'document', 'actions': action, 'id': id}


@bp.post('/profile/address/<action>/<int:id>')
@bp.doc(hide=True)
@bp.input(AddressSchema)
@jwt_required()
def post_address(action, id, json_data):
    """
    Create or update an address for a profile.
    Parameters:
        action (str): The action to perform. Can be 'create' or 'update'.
        id (int): The ID of the profile.
        response (dict): The address information to create or update.
    Returns:
        dict: A dictionary with the table name, action performed, and profile ID.
    """
    if action == 'create':
        db.session.add(Address(**json_data | {'person_id': id}))
    else:
        for k, v in json_data.items():
            setattr(db.session.query(Address).get(id), k, v)
    db.session.commit()
    return {'table': 'address', 'actions': action, 'id': id}


@bp.post('/profile/contact/<action>/<int:id>')
@bp.doc(hide=True)
@bp.input(ContactSchema)
@jwt_required()
def post_contact(action, id, json_data):
    """
    Endpoint for creating or updating a contact in the profile.
    Parameters:
        action (str): The action to perform, either 'create' or 'update'.
        id (int): The ID of the contact to create or update.
        response (dict): The data for creating or updating the contact.
    Returns:
        dict: A dictionary containing the table name, the action performed, and the ID of the contact.
    """
    if action == 'create':
        db.session.add(Contact(**json_data | {'person_id': id}))
    else:
        for k, v in json_data.items():
            setattr(db.session.query(Contact).get(id), k, v)
    db.session.commit()
    return {'table': 'contact', 'actions': action, 'id': id}


@bp.post('/profile/workplace/<action>/<int:id>')
@bp.input(WorkplaceSchema)
@bp.doc(hide=True)
@jwt_required()
def post_workplace(action, id, json_data):
    """
    POST method for updating workplace information.
    Parameters:
        action (str): The action to perform on the workplace information. Valid values are 'create' or 'update'.
        id (int): The id of the workplace to update.
        response (dict): The updated workplace information.
    Returns:
        dict: A dictionary containing the table name, the action performed, and the id of the updated workplace.
    """
    if action == 'create':
        db.session.add(Workplace(**json_data | {'person_id': id}))
    else:
        for k, v in json_data.items():
            setattr(db.session.query(Workplace).get(id), k, v)
    db.session.commit()
    return {'table': 'workplace', 'actions': action, 'id': id}


@bp.post('/profile/relation/<action>/<int:id>')
@bp.input(RelationSchema)
@bp.doc(hide=True)
@jwt_required()
def post_relation(action, id, json_data):
    """
    Post a relation to the profile.
    :param action: The action to perform on the relation. Possible values are 'create' or any other action.
    :type action: str
    :param id: The ID of the profile relation.
    :type id: int
    :param response: The response containing the relation details.
    :type response: dict
    :return: A dictionary containing the table name, action performed, and the ID of the profile relation.
    :rtype: dict
    """
    if action == 'create':
        db.session.add(Relation(**json_data | {'person_id': id}))
    else:
        for k, v in json_data.items():
            setattr(db.session.query(Relation).get(id), k, v)
    db.session.add(Relation(relation = json_data['relation'], 
                            relation_id = id, 
                            person_id = json_data['relation_id']))
    db.session.commit()
    return {'table': 'relation', 'actions': action, 'id': id}


@bp.post('/profile/location/<action>/<int:id>')
@bp.input(PersonSchema)
@bp.doc(hide=True)
@jwt_required()
def post_location(action, id, json_data):
    """
    Create or update a person's location.
    Parameters:
    - action (str): The action to perform. Can be 'create' or any other string.
    - id (int): The ID of the person.
    - response (dict): The response containing the person's location information.
    Returns:
    - dict: A dictionary containing the table name, action, and ID of the location.
    """
    if action == 'create':
        db.session.add(Person(**json_data | {'region_id': id}))
    else:
        for k, v in json_data.items():
            setattr(db.session.query(Person).get(id), k, v)
        users = db.session.query(User).filter(User.role.in_(['superuser', 'user']), 
                                            User.region_id == json_data['region_id']).all()
        for user in users:
            db.session.add(Report(report=f'Делегирована анкета ID #{id} от {current_user.username}', user_id=user.id))        
    db.session.commit()
    return {'table': 'location', 'actions': action, 'id': id}


@bp.post('/photo/upload/<int:person_id>')
@bp.doc(hide=True)
@jwt_required()
def upload_photo(person_id):
    """
    Uploads a photo for a given person.
    :param person_id: The ID of the person.
    :type person_id: int
    :return: A dictionary indicating the result of the upload.
    :rtype: dict
    """
    if 'file' not in request.files:
        return {'result': False}
    
    person = Person.query.get(person_id)
    if person.path:
        if not os.path.isdir(person.path):  # если директория не существует
            os.mkdir(os.path.join(person.path))
        new_path = person.path
    else:
        new_path = os.path.join(BASE_PATH, f'{person_id}-{person["fullname"]}')
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
        person.path = new_path
        db.session.commit()

    file = request.files['file']
    im = Image.open(file)
    rgb_im = im.convert('RGB')
    images = os.path.join(new_path, 'images')
    if not os.path.isdir(images):
        os.mkdir(images)
    rgb_im.save(os.path.join(images, 'person.jpg'))
    
    return {'result': True}


@bp.get('/anketa/status/<int:person_id>')
@bp.doc(hide=True)
@jwt_required()
def patch_status(person_id: int):
    """
    Update the status of a person in the database.
    Parameters:
        person_id (int): The ID of the person whose status needs to be updated.
    Returns:
        dict: A dictionary containing the message of the status update.
    """
    person = Person.query.get(person_id)
    if person:
        person.status = Status.update.value
        db.session.commit()
        return {"message": Status.update.value}
    return {"message": Status.error.name}


@bp.get('/anketa/send/<int:person_id>')
@bp.doc(hide=True)
@jwt_required()
def send_resume(person_id):
    """
    Sends a resume to the check's robot.
    Parameters:
        person_id (int): The ID of the person.
    Returns:
        dict: A dictionary containing the response message
    """
    resume = db.session.query(Person).get(person_id)
    if resume.has_status([Status.new.value, Status.update.value, Status.repeat.value]):
        anketa_schema = AnketaSchema()
        serial = anketa_schema.dump(dict(
            resume = resume, 
            document = db.session.query(Document).filter_by(person_id=person_id).order_by(Document.id.desc()).first(), 
            address = db.session.query(Address).filter_by(person_id=person_id).filter(Address.view.ilike("%регистрац%")).\
                order_by(Address.id.desc()).first()))
        try:
            response = requests.post(url='https://httpbin.org/post', json=serial, timeout=5)
            response.raise_for_status()
            if response.status_code == 200:
                check_path = create_folders(person_id, resume.fullname, 'Проверки')
                resume.status = Status.robot.value
                db.session.add(Check(officer=current_user.username, 
                                     path=check_path,
                                     person_id = person_id))
                db.session.commit()
                return {'message': Status.robot.name}
            return {'message': Status.error.name}
        except requests.exceptions.RequestException as e:
            print(e)
            return {'message': Status.error.name}
    return {'message': Status.error.name}


def create_folders(person_id, fullname, folder_name):
    """
        Check if a folder exists for a given person and create it if it does not exist.

        :param person_id: The ID of the person.
        :type person_id: int
        :param fullname: The full name of the person.
        :type fullname: str
        :return: The path of the created folder.
        :rtype: str
    """
    url = os.path.join(BASE_PATH, f'{person_id}-{fullname}')
    if not os.path.isdir(url):
        os.mkdir(url)
    folder = os.path.join(url, folder_name)
    if not os.path.isdir(folder):
        os.mkdir(folder)
    subfolder = os.path.join(folder, datetime.now().strftime("%Y-%m-%d"))
    if not os.path.isdir(subfolder):
        os.mkdir(subfolder)
    return subfolder


@bp.get('/check/add/<int:person_id>')
@bp.doc(hide=True)
@jwt_required()
def add_check(person_id):
    """
    Add a check for a person with the given ID.
    Parameters:
        person_id (int): The ID of the person.
    Returns:
        dict: A dictionary containing the message indicating the status of the check.
    """
    person = db.session.query(Person).get(person_id)
    if person.has_status([Status.new.value, Status.update.value, Status.repeat.value]):
        check_path = create_folders(person_id, person.fullname, 'Проверки')
        person.status = Status.manual.value
        db.session.add(Check(officer=current_user.username, 
                                path = check_path,
                                person_id = person_id))
        db.session.commit()
        return {'message': Status.manual.name}
        
    return {'message': Status.error.name}


@bp.post('/profile/check/<action>/<int:id>')
@bp.doc(hide=True)
@bp.input(CheckSchema)
@jwt_required()
def post_check(action, id, json_data):
    """
    Endpoint for performing a check on a profile.
    Args:
        action (str): The action to perform on the profile check.
        id (int): The ID of the profile to perform the check on.
        response (dict): The response containing the check details.
    Returns:
        dict: A dictionary containing information about the performed check.
    """
    json_data['pfo'] = bool(json_data.pop('pfo')) if 'pfo' in json_data else False
    if action == 'create':
        person = db.session.query(Person).get(id)        
        db.session.add(Check(**json_data | {'person_id': id, 'officer': current_user.username}))

    else:
        check = db.session.query(Check).get(id)
        person = db.session.query(Person).get(check.person_id)
        for k, v in json_data.items():
            setattr(check, k, v)
    db.session.commit()    

    if json_data['conclusion'] == (Status.save.value).upper():
        person.status = Status.save.value
        db.session.commit()
        return {'table': 'check', 
                'action': action, 
                'id': id, 
                'message': Status.save.name}
    
    elif json_data['conclusion'] == (Status.cancel.name).upper():
        person.status = Status.result.value
        db.session.commit()
        return {'table': 'check', 
                'action': action, 
                'id': id, 
                'message': Status.cancel.name}
    
    else:
        person.status = Status.poligraf.value if json_data['pfo'] else Status.result.value
        db.session.commit()
    
    return {'table': 'check', 
            'action': action, 
            'id': id, 
            'message': Status.poligraf.name if json_data['pfo'] else Status.result.name}


@bp.post('/profile/registry/<action>/<int:id>')
@roles_required(Roles.superuser.value)
@bp.input(RegistrySchema)
@bp.doc(hide=True)
@jwt_required()
def post_registry(action, id, json_data):
    """
    Post a registry entry for a given ID and response.
        :param id: The ID of the person.
        :type id: int
        :param response: The response to the registry entry.
        :type response: dict
        :return: A dictionary with a message indicating the result of the registry entry.
        :rtype: dict
    """
    check_id = db.session.query(Check.id).filter_by(person_id=id).order_by(Check.id.desc()).scalar()
    reg = {'supervisor': current_user.username} | json_data
    person = db.session.query(Person).get(id)
    # отправка ответа о результатах проверки если анкета поступила через API
    if person.request_id or person.request_id != 'NULL':  
        try:
            response = requests.post(url='https://httpbin.org/post', 
                                    json=json.dumps({"id": person.request_id}
                                                    | reg), timeout=5)
            response.raise_for_status()
            if response.status_code == 200:
                db.session.add(Registry(**reg | {'check_id': check_id}))
                person.status = Status.cancel.value \
                    if reg['decision'] == Status.cancel.value else Status.finish.value
                db.session.commit()
                return {'table': 'registry', 
                        'action': action, 
                        'id': id, 
                        'message': Status.finish.name}
            else:
                return {'table': 'registry', 
                        'action': action, 
                        'id': id, 
                        'message': response.text}
        except Exception as e:
            return {'table': 'registry', 
                    'action': action, 
                    'id': id, 
                    "message": e}
    db.session.add(Registry(**reg | {'check_id': check_id}))
    person.status = Status.cancel.value \
        if reg['decision'] == Status.cancel.value else Status.finish.value
    db.session.commit()
    return {'table': 'registry', 
            'action': action, 
            'id': id, 
            'message': Status.finish.name}


@bp.post('/profile/poligraf/<action>/<int:id>')
@bp.doc(hide=True)
@bp.input(PoligrafSchema)
@jwt_required()
def post_poligraf(action, id, json_data):
    """
    Endpoint for creating or updating a poligraf profile.
    Args:
        action (str): The action to perform. Can be 'create' or any other value for updating.
        id (int): The ID of the poligraf profile.
        response (dict): The data to be stored in the poligraf profile.
    Returns:
        dict: A dictionary containing the action performed and the ID of the poligraf profile.
    """
    if action == 'create':
        person = db.session.query(Person).get(id)
        if person.has_status(Status.poligraf.value):
            person.status = Status.result.value
        db.session.add(Poligraf(**json_data | {'person_id': id, 'officer': current_user.username}))
    else:
        for k, v in json_data.items():
            setattr(db.session.query(Poligraf).get(id), k, v)
    db.session.commit()
    return {'table': 'poligraf', 'actions': action, 'id': id}


@bp.post('/profile/investigation/<action>/<int:id>')
@bp.doc(hide=True)
@bp.input(InvestigationSchema)
@jwt_required()
def post_investigation(action, id, json_data):
    """
    Endpoint for creating or updating an investigation profile for a person.
    Args:
        action (str): The action to perform. 'create' to create a new investigation profile, or any other value to update an existing profile.
        person_id (int): The ID of the person for whom the investigation profile is being created or updated.
    Returns:
        dict: A dictionary containing the action performed and the person ID.
    """
    canddiate = db.session.query(Person).get(id)
    if action == 'create':
        invs_path = create_folders(id, canddiate.fullname, 'Расследования')
        db.session.add(Investigation(**json_data | {'person_id': id, 'path': invs_path, 'officer': current_user.username}))
    else:
        for k, v in json_data.items():
            setattr(db.session.query(Investigation).get(id), k, v)
    db.session.commit()
    return {'table': 'investigation', 'actions': action, 'id': id}


@bp.post('/profile/inquiry/<action>/<id>')
@bp.doc(hide=True)
@bp.input(InquirySchema)
@jwt_required()
def post_inquiry(action, id, json_data):
    """
    Endpoint to post an inquiry for a specific person.
    Parameters:
        - action (str): The action to perform. Can be 'create' or any other string.
        - person_id (int): The ID of the person for whom the inquiry is being posted.
    Returns:
        dict: A dictionary containing the action performed and the person ID.
    """
    if action == 'create':
        db.session.add(Inquiry(**json_data | {'person_id': id, 'officer': current_user.username}))
    else:
        for k, v in json_data.items():
            setattr(db.session.query(Inquiry).get(id), k, v)
    db.session.commit()
    return {'table': 'inquiry', 'actions': action, 'id': id}
 

@bp.delete('/profile/<item>/delete/<int:item_id>')
@bp.doc(hide=True)
@jwt_required()
def delete_item(item, item_id):
    """
    Deletes an item of a specified type from the database.
    Args:
        item (str): The type of item to delete.
        item_id (int): The ID of the item to delete.
    Returns:
        str: An empty string if the item is successfully deleted.
    """
    item_model_map = {
        'person': Person,
        'staff': Staff,
        'relation': Relation,
        'document': Document,
        'workplace': Workplace,
        'address': Address,
        'contact': Contact,
        'check': Check,
        'poligraf': Poligraf,
        'investigation': Investigation,
        'inquiry': Inquiry
    }
    item_model = item_model_map.get(item)
    item_instance = item_model.query.get(item_id)
    if item in ['person', 'check', 'investigation']:
        try:
            shutil.rmtree(item_instance.path)
        except Exception as e:
            print(e)
        if item == 'check':
            person = db.session.query(Person).get(db.session.query(Check.person_id).filter_by(id=item_id).scalar())
            setattr(person, 'status', Status.update.value)
    db.session.delete(item_instance)
    db.session.commit()
    return {'message': item}
    

@bp.post('/information')
@bp.doc(hide=True)
@jwt_required()
def post_information():
    """
    Returns:
        dict: A dictionary containing the candidates and poligraf information.
            - candidates (dict): A dictionary mapping the decision to the count of candidates.
            - poligraf (dict): A dictionary mapping the theme to the count of poligraf entries.
    """
    response = request.get_json()
    candidates = db.session.query(Registry.decision, func.count(Registry.id)).\
        join(Check, Check.id == Registry.check_id). \
            join(Person, Person.id == Check.person_id).\
                group_by(Registry.decision).\
                    filter(Registry.deadline.between(response['start'], response['end']), 
                            Person.region_id == int(response['region'])).all()

    pfo = db.session.query(Poligraf.theme, func.count(Poligraf.id)).group_by(Poligraf.theme). \
        filter(Poligraf.deadline.between(response['start'], response['end'])).all()
    
    return {"candidates": dict(map(lambda x: (x[1], x[0]), candidates)),
            "poligraf": dict(map(lambda x: (x[1], x[0]), pfo))}


@bp.errorhandler(BadRequest)
def handle_bad_request(e):
    """
    A decorator function that handles the BadRequest error.
    Parameters:
    - e (BadRequest): The BadRequest error object.
    Returns:
    - str: The error message 'bad request!'.
    - int: The HTTP status code 400.
    """
    return 'bad request!', 400
