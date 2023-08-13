import json
import os
from datetime import datetime
import requests

from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import func, or_
from flask import request, send_from_directory
from werkzeug.exceptions import BadRequest
from PIL import Image

from . import bp
from ..utils.excel import ExcelFile, resume_data
from ..models.model import User, db, Person, Staff, Document, Address, Contact, Workplace, \
    Check, Registry, Poligraf, Investigation, Inquiry, Relation, Status, Report, Region
from ..models.schema import MessagesSchema, RelationSchema, StaffSchema, AddressSchema, \
        PersonSchema, ProfileSchema, ContactSchema, DocumentSchema, CheckSchema, InquirySchema, \
            InvestigationSchema, PoligrafSchema, RegistrySchema, WorkplaceSchema, AnketaSchema, LocationSchema
from ..models.classify import Category, Conclusions, Decisions, Role, Status

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'persons'))

bp.static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))


@bp.get('/', defaults={'path': ''})
@bp.get('/<string:path>')
@bp.get('/<path:path>')
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


@bp.get('/images/<path:path>') 
@bp.doc(hide=True)
def send_photos(path):
    """
    Send photos from the specified path.
    Parameters:
        path (str): The path to the directory containing the photos.
    Returns:
        Response: The response containing the requested photo.
    """
    return send_from_directory(os.path.join(path, 'photos'), 'photo.jpeg', mimetype='image/jpeg')


@bp.get('/locations')
@bp.doc(hide=True)
def get_locations():
    """
    Retrieves all locations from the database.
    Returns:
        dict: A dictionary containing the locations, where the keys are the region IDs and the values are the corresponding region names.
    """
    return {rgn[0]: rgn[1] for rgn in db.session.query(Region.id, Region.region).all()}
    
    
@bp.get('/classify')
@bp.doc(hide=True)
def get_classify():
    """
    Get the classification data.
    This function retrieves the classification data for the API. It returns a dictionary 
    containing the values of the different status options, role options, conclusions,
    decisions, and categories.
    """
    return [{i.name: i.value for i in Status}, 
            {i.name: i.value for i in Role}, 
            {i.name: i.value for i in Conclusions}, 
            {i.name: i.value for i in Decisions}, 
            {i.name: i.value for i in Category}]


@bp.get('/messages/<string:flag>')
@bp.doc(hide=True)
@bp.output(MessagesSchema)
@jwt_required()
def get_messages(flag):
    """
    Retrieves messages based on a flag.
    Args:
        flag (str): The flag to determine the type of messages to retrieve.
    Returns:
        list: A list of messages retrieved based on the flag.
    """
    messages = db.session.query(Report).filter(Report.status == Status.new.value,
                                                Report.user_id == current_user.id).limit(12).all()
    if flag == 'reply':
        db.session.delete(messages)
        db.session.commit()
        messages = []
    return messages


@bp.route('/index/<flag>/<int:page>', methods=['GET', 'POST'])
@bp.doc(hide=True)
@jwt_required()
def index(flag, page):
    """
    This function handles the index route of the API. It takes in two parameters:
    - flag: a string representing the flag indicating the type of query to perform
    - page: an integer representing the page number for pagination
    
    The function performs different queries based on the value of the flag parameter:
    - If flag is 'main', the function checks the location_id and performs a query to retrieve a paginated list of Person objects ordered by id in descending order. If the location_id is not 1, the query is filtered by region_id.
    - If flag is 'new', the function performs a query to retrieve a paginated list of Person objects with status values of 'new' or 'update' and category value of 'candidate', filtered by region_id and ordered by id in descending order.
    - If flag is 'officer', the function performs a query to retrieve a paginated list of Person objects with status values not equal to 'finish', 'result', or 'cancel', joined with the Check table on the officer field. The query is filtered by the current user's username and ordered by id in ascending order.
    - If flag is 'search', the function retrieves a JSON payload from the request and performs a query to retrieve a paginated list of Person objects filtered by fullname and birthday fields. The query is filtered by region_id if the location_id is not 1, and ordered by id in ascending order.
    
    The function uses a pagination value of 12 and the PersonSchema to serialize the query results into a list of datas. It also determines the has_next and has_prev values based on the pagination query object.
    
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
            query = db.session.query(Person).filter(Person.status.in_([Status.new.value, Status.update.value]), 
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
                    or_(Person.birthday.ilike('%{}%'.format(search['birthday'])), search['birthday'] == ''),
                    ).order_by(Person.id.asc()).\
                        paginate(page=page, per_page=pagination, error_out=False)
            else:
                query = db.session.query(Person).filter(
                or_(Person.fullname.ilike('%{}%'.format(search['fullname'])), search['fullname'] == ''),
                or_(Person.birthday.ilike('%{}%'.format(search['birthday'])), search['birthday'] == ''),
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
        dict: A dictionary containing the profile information of the person. The dictionary has the following keys:
            - 'resume' (Person): The resume information of the person.
            - 'documents' (list[Document]): The list of documents associated with the person.
            - 'addresses' (list[Address]): The list of addresses associated with the person.
            - 'contacts' (list[Contact]): The list of contacts associated with the person.
            - 'workplaces' (list[Workplace]): The list of workplaces associated with the person.
            - 'staffs' (list[Staff]): The list of staff members associated with the person.
            - 'relations' (list[Relation]): The list of relations associated with the person.
            - 'checks' (list[Check]): The list of checks associated with the person.
            - 'registries' (list[Registry]): The list of registries associated with the person.
            - 'pfos' (list[Poligraf]): The list of poligrafs associated with the person.
            - 'invs' (list[Investigation]): The list of investigations associated with the person.
            - 'inquiries' (list[Inquiry]): The list of inquiries associated with the person.
    """
    resume = db.session.query(Person).filter_by(id=person_id).one_or_none()
    
    documents = db.session.query(Document).filter_by(person_id=person_id).order_by(Document.person_id.asc()).all()
    
    addresses = db.session.query(Address).filter_by(person_id=person_id).order_by(Address.id.asc()).all()
    
    contacts = db.session.query(Contact).filter_by(person_id=person_id).order_by(Contact.id.asc()).all()
    
    workplaces = db.session.query(Workplace).filter_by(person_id=person_id).order_by(Workplace.id.asc()).all()
    
    relations = db.session.query(Relation).filter_by(person_id=person_id).order_by(Relation.id.asc()).all()
    
    staffs = db.session.query(Staff).filter_by(person_id=person_id).order_by(Staff.id.asc()).all()
    
    checks = db.session.query(Check).filter_by(person_id=person_id).order_by(Check.id.asc()).all()

    registries = [db.session.query(Registry).filter_by(check_id=check.id).first() for check in checks]
    
    pfos = db.session.query(Poligraf).filter_by(person_id=person_id).order_by(Poligraf.id.asc()).all()
    
    invs = db.session.query(Investigation).filter_by(person_id=person_id).order_by(Investigation.id.asc()).all()
    
    inquiries = db.session.query(Inquiry).filter_by(person_id=person_id).order_by(Inquiry.id.asc()).all()

    return {'resume': resume, 'documents': documents, 'addresses': addresses, 'contacts': contacts, 
            'workplaces': workplaces, 'staffs': staffs, 'relations': relations, 'checks': checks, 
            'registries': registries, 'pfos': pfos, 'invs': invs, 'inquiries': inquiries}


@bp.post('/resume/create')
@bp.input(PersonSchema)
@bp.doc(hide=True)
@jwt_required()
def post_resume(response):
    """
    Creates a new resume for a person.
    Parameters:
        - response: The input data for creating the resume. (PersonSchema)
    Returns:
        - A dictionary containing the person_id and the result of the resume creation. (dict)
    """
    location_id = db.session.query(User.region_id).filter_by(username=current_user.username).scalar()
    person_id, result = add_resume(response, location_id)
    return {'person_id': person_id, 'result': result}


@bp.post('/resume/upload')
@bp.doc(hide=True)
@jwt_required()
def upload_file():
    """
    Uploads a file and adds the resume data to the database.
    Returns:
        A dictionary containing the result of the upload and the person ID.
    """
    file = request.files['file']
    excel = ExcelFile(file)
    location_id = db.session.query(User.region_id).filter_by(username=current_user.username).scalar()

    person_id, result = add_resume(excel.resume, location_id)
    resume_data(person_id, excel.passport, excel.addresses, excel.contacts, excel.workplaces, excel.staff)

    return {'result': bool(result), 'person_id': person_id}


def add_resume(resume: dict, location_id):
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
        resume.update({'status': Status.update.value, 'region_id': location_id})
        for k, v in resume.items():
            setattr(result, k, v)
        person_id = result.id
        
        if result.path and not os.path.isdir(result.path):
            os.mkdir(result.path)
        else:
            new_path = os.path.join(BASE_PATH, f'{person_id}-{resume["fullname"]}')
            if not os.path.isdir(new_path):
                os.mkdir(new_path)
                setattr(result, 'path', new_path)
    else:
        value = Person(**resume | {'region_id': location_id})
        db.session.add(value)
        db.session.flush()
        person_id = value.id
        path = os.path.join(BASE_PATH, f'{person_id}-{resume["fullname"]}')
        setattr(value, 'path', path)
        os.mkdir(path)
        
    db.session.commit()
    return [person_id, bool(result)]


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
        setattr(person, 'path', new_path)
        db.session.commit()

    file = request.files['file']
    im = Image.open(file)
    rgb_im = im.convert('RGB')
    if not os.path.isdir(os.path.join(new_path, 'photos')):
        os.mkdir(os.path.join(new_path, 'photos'))
    # сохраняем фото в директорию photos с пометкой времени в формате YYYYMMDDHHMMSS
    rgb_im.save(os.path.join(new_path, 'photos', f'{datetime.now().strftime("%Y%m%d%H%M%S")}.jpg'))
    
    return {'result': True}


@bp.get('/anketa/status/<int:person_id>/')
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
    if person and not person.has_status([Status.result.value]):
        person.status = Status.update.value
        db.session.commit()
        return {"message": Status.update.value}
    return {"message": Status.error.name.value}


@bp.get('/anketa/send/<int:person_id>')
@bp.doc(hide=True)
@jwt_required()
def send_resume(person_id):
    """
    Sends a resume to the check's robot.
    Parameters:
        person_id (int): The ID of the person.
    Returns:
        dict: A dictionary containing the response message.
            Possible values for the 'message' key:
                - 'new': The resume status is set to 'new'.
                - 'update': The resume status is set to 'update'.
                - 'error': An error occurred during the request.
    """
    resume = db.session.query(Person).get(person_id)
    if resume.has_status([Status.new.value, Status.update.value]):
        folder_check(person_id, resume["fullname"])
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
                resume.status = Status.robot.value
                db.session.add(Check(officer=current_user.username, 
                                        path = os.path.join(BASE_PATH, 
                                                            resume.fullname[0], 
                                                            f"{str(resume.id)}-{resume.fullname}",
                                                            datetime.now().strftime("%Y-%m-%d")),
                                                            person_id=person_id))
                db.session.commit()
                return {'message': Status.robot.name}
            return {'message': Status.error.name}
        except requests.exceptions.RequestException as e:
            print(e)
            return {'message': Status.error.name}
    return {'message': Status.error.name}


def folder_check(person_id, fullname):
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
    check_path = os.path.join(url, datetime.now().strftime("%Y-%m-%d"))
    os.mkdir(check_path)
    return check_path


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
    person = Person.query.get(person_id)
    if person.has_status([Status.new.value, Status.update.value]):
        check_path = folder_check(person_id, person.fullname)
        person.status = Status.manual.value
        db.session.add(Check(officer=current_user.username, 
                                path = check_path,
                                person_id = person_id))
        db.session.commit()
        return {'message': Status.manual.name}
        
    return {'message': Status.error.name}

                         
@bp.post('/<item>/<action>/<int:id>')
@bp.doc(hide=True)
@jwt_required()
def post_item(item, action, id):
    """
        Endpoint for posting an item.
        Args:
            item (str): The type of item being posted.
            action (str): The action to be performed on the item.
            id (int): The ID of the item being posted.
        Returns:
            dict: A dictionary containing the message response.
    """
    item_model_map = {
        'staff': [Staff, StaffSchema],
        'relation': [Relation, RelationSchema],
        'document': [Document, DocumentSchema],
        'workplace': [Workplace, WorkplaceSchema],
        'address': [Address, AddressSchema],
        'contact': [Contact, ContactSchema],
        'check': [Check, CheckSchema],
        'registry': [Registry, RegistrySchema],
        'poligraf': [Poligraf, PoligrafSchema],
        'investigation': [Investigation, InvestigationSchema],
        'inquiry': [Inquiry, InquirySchema],
        'location': [Person, LocationSchema]
    }
    schema = item_model_map.get(item)[1]
    response = schema.load(request.get_json())
    
    if item == 'registry':
        post_registry(id, response)

    else:
        model = item_model_map.get(item)[0]
        item_instance = model.query.get(id)
        if action == 'update':
            if item == 'check':
                post_check(id, response, item_instance)
            else:
                for k, v in response.items():
                    setattr(item_instance, k, v)
                if item == 'location':
                    users = db.session.query(User).filter(User.role.in_(['superuser', 'user']), 
                                          User.region_id == response).all()
                    for user in users:
                        db.session.add(Report(report=f'Делегирована анкета {item_instance.fullname} от \
                               {current_user.username}', user_id=user.id))
        else:
            if item in ['staff', 'document', 'workplace', 'address', 'contact', 'relation']:
                db.session.add(model(**response | {'person_id': id}))
                if item == 'relation':
                    db.session.add(Relation(relation = response['relation'], 
                                            relation_id = id, 
                                            person_id = response['relation_id']))
            else:
                db.session.add(model(**response | {'person_id': id, 'officer': current_user.username}))
                if item == 'poligraf' and item_instance.has_status(Status.poligraf.value):
                    item_instance.status = Status.result.value
        db.session.commit()
        return {'message': id}


def post_check(int, response: dict, item_instance):
    """
    Updates the person with the given ID using the provided response data.
    Parameters:
        int: The ID of the person to update.
        response (dict): A dictionary containing the response data.
        item_instance: The instance of the item to update.
    Returns:
        dict: A dictionary with a message indicating the status of the update.
    """
    person = db.session.query(Person).get(int)

    response['pfo'] = bool(response.pop('pfo')) if 'pfo' in response else False
    response.update({"officer": current_user.username})
    
    for k, v in response.items():
        setattr(item_instance, k, v)
    
    if response['conclusion'] == 'Сохранено':
        person.status = Status.save.value
        db.session.commit()
        return {'message': Status.save.name}
    
    elif response['conclusion'] == "Отмена":
        person.status = Status.finish.value
        db.session.commit()
        return {'message': Status.cancel.name}
    
    else:
        person.status = Status.poligraf.value if response['pfo'] else Status.result.value
        db.session.commit()
        return {'message': Status.poligraf.name if response['pfo'] else Status.result.name}


def post_registry(id, response):
    """
    Post a registry entry for a given ID and response.
        :param id: The ID of the person.
        :type id: int
        :param response: The response to the registry entry.
        :type response: dict
        :return: A dictionary with a message indicating the result of the registry entry.
        :rtype: dict
    """
    user = db.session.query(User).filter_by(username=current_user.username).one_or_none()
    if user.has_role(Role.superuser.value):
        check_id = db.session.query(Check.id).filter_by(person_id=id).order_by(Check.id.desc()).one_or_none()
        reg = {'check_id': check_id, 'supervisor': current_user.username} | response
        person = Person.query.get(id)
        if person.request_id:  # отправка ответа о результатах проверки если анкета поступила через API
            try:
                response = requests.post(url='https://httpbin.org/post', 
                                        json=json.dumps({"id": person.request_id,
                                                        "deadline": datetime.now().strftime("%Y-%m-d%"),
                                                        "supervisor": current_user.username} | response), timeout=5)
                response.raise_for_status()
                if response.status_code == 200:
                    db.session.add(Registry(**reg))
                    person.status = Status.cancel.value if reg['decision'] == Status.cancel.value else Status.finish.value
                    db.session.commit()
                    return {'message': Status.result.name}
                else:
                    return {'message': Status.cancel.name}
            except Exception as e:
                print(e)
                return {"message": Status.error.name}
        else:
            db.session.add(Registry(**reg))
            person.status = Status.cancel.value if reg['decision'] == Status.cancel.value else Status.finish.value
            db.session.commit()
            return {'message': Status.result.name}
    return {'message': Status.error.name}


@bp.delete('/<item>/delete/<int:item_id>')
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
    if item == 'check':
        person = db.session.query(Person).get(db.session.query(Check.person_id).filter_by(id=item_id).scalar())
        if person.has_status([Status.result.value, Status.finish.value]) \
            or db.session.query(Registry).filter_by(check_id=item_id).one_or_none():
            return {'message': Status.error.name}  # нельзя удалить оконченную проверку
        
    os.rmdir(item_instance.path) if os.path.isdir(item_instance.path) else None  # удаление директории с файлами
    db.session.delete(item_instance)
    db.session.commit()
    return ''


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
                           Person.region_id == response['region']).all()
    
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
