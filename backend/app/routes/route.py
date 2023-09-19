from datetime import datetime
import json
import os
import shutil
import requests

from flask import request, current_app, send_from_directory
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import func
from werkzeug.utils import secure_filename

from . import bp
from .. import db
from . login import roles_required, group_required
from ..utils.excel import ExcelFile
from ..utils.actions import resume_data, add_resume, create_folders
from ..models.model import User, Person, Staff, Document, Address, Contact, Workplace, \
    Check, Registry, Poligraf, Investigation, Inquiry, Relation, Status, Report
from ..models.schema import RelationSchema, StaffSchema, AddressSchema, \
        PersonSchema, ProfileSchema, ContactSchema, DocumentSchema, CheckSchema, InquirySchema, \
            InvestigationSchema, PoligrafSchema, RegistrySchema, WorkplaceSchema, AnketaSchema
from ..models.classes import Category, Roles, Groups, Status

bp.static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))


@bp.get('/', defaults={'path': ''})
@bp.get('/<path:path>')
@bp.get('/index/profile/<path:path>')
@bp.doc(hide=True)
def main(path=''):
    """
    Get the file from the specified path in the static folder and return it, or return the index.html file if the path is not found.
    """
    if path and os.path.exists(os.path.join(bp.static_folder, path)):
        return send_from_directory(bp.static_folder, path)
    else:
        return bp.send_static_file('index.html')


@bp.route('/index/<flag>/<int:page>', methods=['GET', 'POST'])
@group_required(Groups.staffsec.name)
@bp.doc(hide=True)
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
                query = db.session.query(Person).filter(Person.fullname.ilike('%{}%'.format(search['fullname']))).\
                    order_by(Person.id.asc()).paginate(page=page, per_page=pagination, error_out=False)
            else:
                query = db.session.query(Person).filter(Person.fullname.ilike('%{}%'.format(search['fullname'])), 
                                                        Person.region_id == location_id).order_by(Person.id.asc()).\
                    paginate(page=page, per_page=pagination, error_out=False)
    
    resume_schema = PersonSchema()
    datas = resume_schema.dump(query, many=True)
    has_next, has_prev = int(query.has_next), int(query.has_prev)
    
    return [datas, {'has_next': has_next, "has_prev": has_prev}]


@bp.get('/profile/<int:person_id>')
@group_required(Groups.staffsec.name)
@bp.doc(hide=True)
@bp.output(ProfileSchema)
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


@bp.post('/file/<action>/<int:item_id>')
@group_required(Groups.staffsec.name)
@roles_required(Roles.user.name)
@bp.doc(hide=True)
def upload_file(action, item_id=0):
    """
    Handles the POST request to upload a file.
    Parameters:
        action (str): The action to perform on the file.
        item_id (int): The ID of the file to upload.
    Returns:
        dict: A dictionary containing the action performed and the item ID.
    """
    if request.files['file'].filename == '':
        return {'result': False, 'item_id': item_id}
    
    if action == 'anketa':
        file = request.files['file']
        
        filename = secure_filename(file.filename)
        temp_path = os.path.join(current_app.config["BASE_PATH"], f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}-{filename}')
        file.save(temp_path)
        
        excel = ExcelFile(temp_path)
        location_id = db.session.query(User.region_id).filter_by(username=current_user.username).scalar()

        person_id, result = add_resume(excel.resume, location_id, 'create')
        resume_data(person_id, excel.passport, excel.addresses, excel.contacts, excel.workplaces, excel.staff)
        excel.close()

        person = Person.query.get(person_id)
        if person and person.path:
            if not os.path.isdir(person.path):
                os.mkdir(os.path.join(person.path))
            new_path = person.path
        else:
            new_path = os.path.join(current_app.config["BASE_PATH"], f'{person_id}-{person["fullname"]}')
            if not os.path.isdir(new_path):
                os.mkdir(new_path)
            person.path = new_path
            db.session.commit()

        action_folder = os.path.join(new_path, action)
        if not os.path.isdir(action_folder):
            os.mkdir(action_folder)

        save_path = os.path.join(action_folder, filename)
        if not os.path.isfile(save_path):
            shutil.move(temp_path, save_path)
        return {'result': bool(result), 'person_id': person_id}

    else:
        model_mapping = {
            'check': Check,
            'investigation': Investigation,
            'poligraf': Poligraf,
            'inquiry': Inquiry
        }
        files = request.files.getlist('file')
        model = model_mapping.get(action)
        item = db.session.query(model).filter_by(id=item_id).scalar()
        folder = item.path
        if not folder:
            person  = Person.query.get(item.person_id)
            folder = create_folders(person.id, person.fullname, action)
            item.path = folder
            db.session.commit()
        for file in files:
            filename = secure_filename(file.filename)
            for file in files:
                file.save(os.path.join(folder, filename))
        
        return {'result': bool(result), 'person_id': person_id}


@bp.post('/resume/<action>')
@group_required(Groups.staffsec.name)
@roles_required(Roles.user.name)
@bp.input(PersonSchema)
@bp.doc(hide=True)
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


@bp.post('/profile/<table>/<action>/<int:id>')
@roles_required(Roles.user.value)
@bp.doc(hide=True)
def post_staff(table, action, id):
    """
    Handles the POST request to update staff profile information.
    Parameters:
        table (str): The table name for the profile information.
        action (str): The action to perform on the profile information.
        id (int): The ID of the staff member.
    Returns:
        dict: A dictionary containing the updated table name, action, and ID.
    """
    response = request.get_json()
    mapping = {
        'staff': [StaffSchema, Staff],
        'document': [DocumentSchema, Document],
        'address': [AddressSchema, Address],
        'contact': [ContactSchema, Contact],
        'workplace': [WorkplaceSchema, Workplace],
        'relation': [RelationSchema, Relation],
        'location': [PersonSchema, Person]
        }
    schema = mapping[table][0]  
    data = schema.dump(response)

    if action == 'create':
        db.session.add(mapping[table][1](**data | {'person_id': id}))
    else:
        for k, v in data.items():
            setattr(db.session.query(mapping[table][1]).get(id), k, v)
    
    if table == 'relation':
        db.session.add(Relation(relation = data['relation'], 
                                relation_id = id,
                                person_id = data['relation_id']))
    if table == 'location':
        users = db.session.query(User).filter_by(region_id=data['region_id']).all()
        for user in users:
            db.session.add(Report(report=f'Делегирована анкета ID #{id} от {current_user.username}', user_id=user.id))
    
    db.session.commit()
    return {'table': table, 'actions': action, 'id': id}


@bp.get('/anketa/status/<int:person_id>')
@group_required(Groups.staffsec.name)
@roles_required(Roles.user.name)
@bp.doc(hide=True)
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
@group_required(Groups.staffsec.name)
@roles_required(Roles.user.name)
@bp.doc(hide=True)
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
                db.session.add(Check(officer=current_user.fullname, 
                                     path=check_path,
                                     person_id = person_id))
                db.session.commit()
                return {'message': Status.robot.name}
            return {'message': Status.error.name}
        except requests.exceptions.RequestException as e:
            print(e)
            return {'message': Status.error.name}
    return {'message': Status.error.name}


@bp.get('/check/add/<int:person_id>')
@group_required(Groups.staffsec.name)
@roles_required(Roles.user.name)
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
        db.session.add(Check(officer=current_user.fullname, 
                                path = check_path,
                                person_id = person_id))
        db.session.commit()
        return {'message': Status.manual.name}
        
    return {'message': Status.error.name}


@bp.post('/profile/check/<action>/<int:id>')
@group_required(Groups.staffsec.name)
@roles_required(Roles.user.name)
@bp.doc(hide=True)
@bp.input(CheckSchema)
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
        db.session.add(Check(**json_data | {'person_id': id, 'officer': current_user.fullname}))

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
@group_required(Groups.staffsec.name)
@roles_required(Roles.superuser.value)
@bp.input(RegistrySchema)
@bp.doc(hide=True)
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
    reg = {'supervisor': current_user.fullname} | json_data
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
@group_required(Groups.staffsec.name)
@roles_required(Roles.user.name)
@bp.doc(hide=True)
@bp.input(PoligrafSchema)
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
        db.session.add(Poligraf(**json_data | {'person_id': id, 'officer': current_user.fullname}))
    else:
        for k, v in json_data.items():
            setattr(db.session.query(Poligraf).get(id), k, v)
    db.session.commit()
    return {'table': 'poligraf', 'actions': action, 'id': id}


@bp.post('/profile/investigation/<action>/<int:id>')
@group_required(Groups.staffsec.name)
@roles_required(Roles.user.name)
@bp.doc(hide=True)
@bp.input(InvestigationSchema)
def post_investigation(action, id, json_data):
    """
    Endpoint for creating or updating an investigation profile for a person.
    Args:
        action (str): The action to perform. 'create' to create a new investigation profile, or any other value to update an existing profile.
        person_id (int): The ID of the person for whom the investigation profile is being created or updated.
    Returns:
        dict: A dictionary containing the action performed and the person ID.
    """
    if action == 'create':
        db.session.add(Investigation(**json_data | {'person_id': id, 'officer': current_user.fullname}))
    else:
        for k, v in json_data.items():
            setattr(db.session.query(Investigation).get(id), k, v)
    db.session.commit()
    return {'table': 'investigation', 'actions': action, 'id': id}


@bp.post('/profile/inquiry/<action>/<id>')
@group_required(Groups.staffsec.name)
@roles_required(Roles.user.name)
@bp.doc(hide=True)
@bp.input(InquirySchema)
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
        db.session.add(Inquiry(**json_data | {'person_id': id, 'officer': current_user.fullname}))
    else:
        for k, v in json_data.items():
            setattr(db.session.query(Inquiry).get(id), k, v)
    db.session.commit()
    return {'table': 'inquiry', 'actions': action, 'id': id}
 

@bp.delete('/profile/<item>/delete/<int:item_id>')
@group_required(Groups.staffsec.name)
@roles_required(Roles.user.name)
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
@group_required(Groups.staffsec.name)
@roles_required(Roles.superuser.name, Roles.user.name)
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

