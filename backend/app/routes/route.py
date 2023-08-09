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
    if path and os.path.exists(os.path.join(bp.static_folder, path)):
        return send_from_directory(bp.static_folder, path)
    else:
        return bp.send_static_file('index.html')


@bp.get('/locations')
@bp.doc(hide=True)
def get_locations():
    return {rgn[0]: rgn[1] for rgn in db.session.query(Region.id, Region.region).all()}
    
    
@bp.get('/classify')
@bp.doc(hide=True)
def get_classify():
    return [{i.name: i.value for i in Status}, 
            {i.name: i.value for i in Role}, 
            {i.name: i.value for i in Conclusions}, 
            {i.name: i.value for i in Decisions}, 
            {i.name: i.value for i in Category}]


@bp.route('/index/<flag>/<int:page>', methods=['GET', 'POST'])
@bp.doc(hide=True)
@jwt_required()
def index(flag, page):
    pagination = 12
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


@bp.get('/messages/<string:flag>')
@bp.doc(hide=True)
@bp.output(MessagesSchema)
@jwt_required()
def get_messages(flag):
    messages = db.session.query(Report).filter(Report.status == Status.new.value,
                                                Report.user_id == current_user.id).limit(12).all()
    if flag == 'reply':
        db.session.delete(messages)
        db.session.commit()
        messages = []
    return messages


@bp.get('/profile/<int:person_id>')
@bp.doc(hide=True)
@bp.output(ProfileSchema)
@jwt_required()
def get_profile(person_id):
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
    location_id = db.session.query(User.region_id).filter_by(username=current_user.username).scalar()
    person_id, result = add_resume(response, location_id)
    return {'person_id': person_id, 'result': result}


@bp.post('/resume/upload')
@bp.doc(hide=True)
@jwt_required()
def upload_file():
    file = request.files['file']
    excel = ExcelFile(file)
    location_id = db.session.query(User.region_id).filter_by(username=current_user.username).scalar()

    person_id, result = add_resume(excel.resume, location_id)
    resume_data(person_id, excel.passport, excel.addresses, excel.contacts, excel.workplaces, excel.staff)

    return {'result': bool(result), 'person_id': person_id}


def add_resume(resume: dict, location_id):
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


@bp.post('/photo/<int:person_id>')
@bp.doc(hide=True)
@jwt_required()
def upload_photo(person_id):
    if 'file' not in request.files:
        return {'result': False}
    
    person = Person.query.get(person_id)
    if person.path:
        if not os.path.isdir(person.path):
            os.mkdir(person.path)
        else:
            for index, file in enumerate(os.listdir(person.path)):
                if file.startswith('photo'):
                    lst_file = file.rsplit('.', 1)
                    os.rename(os.path.join(person.path, file), 
                              os.path.join(person.path, f'{lst_file[0]}-{index+1}.{lst_file[1]}'))
        new_path = person.path
    else:
        new_path = os.path.join(f'{person_id}-{person["fullname"]}')
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
        setattr(person, 'path', new_path)
        db.session.commit()

    file = request.files['file']
    im = Image.open(file)
    rgb_im = im.convert('RGB')
    photo_path = os.path.join(new_path,'photo.jpg')
    rgb_im.save(photo_path)
    
    return {'result': True}


@bp.get('/images/<path:path>') 
@bp.doc(hide=True)
def send_photos(path):
    return send_from_directory(path, 'photo.jpeg', mimetype='image/jpeg')


@bp.post('/update/staff/<person_id>')
@bp.input(StaffSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def update_staff(person_id, response):
    db.session.add(Staff(**response | {'person_id': person_id}))
    db.session.commit()
    return ''


@bp.post('//update/document/<person_id>')
@bp.input(DocumentSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def update_document(person_id, resonse):
    db.session.add(Document(**resonse | {'person_id': person_id}))
    db.session.commit()
    return ''


@bp.post('/update/contact/<person_id>')
@bp.input(ContactSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def update_contact(person_id, response):
    db.session.add(Contact(**response | {'person_id': person_id}))
    db.session.commit()
    return ''


@bp.post('/update/workplace/<person_id>')
@bp.input(WorkplaceSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def update_workplace(person_id, response):
    db.session.add(Workplace(**response | {'person_id': person_id}))
    db.session.commit()
    return ''


@bp.post('/update/address/<person_id>')
@bp.input(AddressSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def update_address(person_id, response):
    db.session.add(Address(**response | {'person_id': person_id}))
    db.session.commit()
    return ''


@bp.post('/update/relation/<person_id>')
@bp.input(RelationSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def create_relation(person_id, response):
    db.session.add(Relation(**response | {'person_id': person_id}))
    db.session.add(Relation(relation = response['relation'], 
                            relation_id = person_id, 
                            person_id = response['relation_id']))
    db.session.commit()
    return ''


@bp.post('/update/location/<person_id>')
@bp.doc(hide=True)
@jwt_required()
def add_region(person_id):
    location = request.form['region']
    person = Person.query.get(person_id)
    setattr(person, 'region_id', location)
    users = db.session.query(User).filter(User.role.in_(['superuser', 'user']), 
                                          User.region_id == location).all()
    for user in users:
        db.session.add(Report(report=f'Делегирована анкета {person.fullname} от \
                               {current_user.username}', user_id=user.id))
    db.session.commit()
    return ''


@bp.delete('/delete/<item>/<int:item_id>')
@bp.doc(hide=True)
@jwt_required()
def delete_item(item, item_id):
    item_model_map = {
        'staff': Staff,
        'relation': Relation,
        'document': Document,
        'workplace': Workplace,
        'address': Address,
        'contact': Contact
    }
    item_model = item_model_map.get(item)
    if item_model:
        item_instance = item_model.query.get(item_id)
        if item_instance:
            db.session.delete(item_instance)
            db.session.commit()
    return ''



@bp.get('/anketa/status/<int:person_id>/')
@bp.doc(hide=True)
@jwt_required()
def patch_status(person_id: int):
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
    resume = db.session.query(Person).get(person_id)
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


@bp.get('/anketa/probe/<int:person_id>/')
@bp.doc(hide=True)
@jwt_required()
def send_check(flag, person_id):
    person = Person.query.get(person_id)
    if person.has_status([Status.new.value, Status.update.value]):
        folder_check(person_id, person["fullname"])
        person.status = Status.robot.value
        db.session.add(Check(officer=current_user.username, person_id = person_id))
        db.session.commit()
        return {'message': Status.robot.name}
        
    return {'message': Status.error.name}


@bp.get('/check/add/<int:person_id>')
@bp.doc(hide=True)
@jwt_required()
def add_check(person_id):
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


def folder_check(person_id, fullname):
    url = os.path.join(BASE_PATH, f'{person_id}-{fullname}')
    if not os.path.isdir(url):
        os.mkdir(url)
    check_path = os.path.join(url, datetime.now().strftime("%Y-%m-%d"))
    os.mkdir(check_path)
    return check_path
                             

@bp.post('/check/create/<int:person_id>')
@bp.input(CheckSchema)
@bp.doc(hide=True)
@jwt_required()
def post_check(person_id: int, response: dict):
    person = db.session.query(Person).get(person_id)
    latest_check = db.session.query(Check).filter_by(person_id=person_id).order_by(Check.id.desc()).first()
    
    response['pfo'] = bool(response.pop('pfo')) if 'pfo' in response else False
    response.update({"officer": current_user.username})
    
    for k, v in response.items():
        setattr(latest_check, k, v)
    
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


@bp.get('/check/delete/<int:person_id>')
@bp.doc(hide=True)
@jwt_required()
def delete_check(person_id):
    person = db.session.query(Person).get(person_id)
    if not person.has_status([Status.result.value, Status.finish.value]):
        latest_check = db.session.query(Check).filter_by(person_id=person_id).order_by(Check.id.desc()).first()
        if latest_check is not None:
            db.session.delete(latest_check)
            db.session.commit()
            return {'message': Status.reply.name}
    return {'message': Status.error.name}


@bp.post('/registry/<int:person_id>')
@bp.input(RegistrySchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def post_registry(person_id, resp):
    user = db.session.query(User).filter_by(username=current_user.username).one_or_none()
    if user.has_role(Role.superuser.value):
        check_id = db.session.query(Check.id).filter_by(person_id=person_id).order_by(Check.id.desc()).one_or_none()
        reg = {'check_id': check_id, 'supervisor': current_user.username} | resp
        person = Person.query.get(person_id)
        if person.request_id:
            try:
                response = requests.post(url='https://httpbin.org/post', 
                                        json=json.dumps({"id": person.request_id,
                                                        "deadline": datetime.now().strftime("%Y-%m-d%"),
                                                        "supervisor": current_user.username} | resp), timeout=5)
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


@bp.post('/poligraf/<int:person_id>')
@bp.input(PoligrafSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def post_poligraf(person_id, response):
    poligraf = Poligraf(**response, person_id=person_id, officer=current_user.username)
    db.session.add(poligraf)
    person = Person.query.get(person_id)
    if person.has_status(Status.poligraf.value):
        person.status = Status.result.value
    db.session.commit()
    return {'message': person_id}


@bp.post('/investigation/<int:person_id>')
@bp.input(InvestigationSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def post_investigation(person_id, response):
    db.session.add(Investigation(**response | {'person_id': person_id, 'officer': current_user.username}))
    db.session.commit()
    return {'message': person_id}


@bp.post('/inquiry/<int:person_id>')
@bp.input(InquirySchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def post_inquiry(person_id, response):
    db.session.add(Inquiry(**response | {'person_id': person_id, 'officer': current_user.username}))
    db.session.commit()
    return {'message': person_id}


@bp.post('/information')
@bp.doc(hide=True)
@jwt_required()
def post_information():
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
    return 'bad request!', 400
