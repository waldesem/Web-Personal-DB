import json
import os
from datetime import datetime
import requests
from flask_jwt_extended import current_user, jwt_required

from sqlalchemy import func, or_
from flask import request, send_from_directory
from werkzeug.exceptions import BadRequest

from . import bp

from ..utils.excel import ExcelFile, resume_data, BASE_PATH
from ..models.model import Roles, User, db, Person, Staff, Document, Address, Contact, Workplace, \
    Check, Registry, Poligraf, Investigation, Inquiry, Relation, Status, Message, Category
from ..models.schema import MessagesSchema, RelationSchema, StaffSchema, AddressSchema, \
        PersonSchema, ProfileSchema, ContactSchema, DocumentSchema, CheckSchema, InquirySchema, \
            InvestigationSchema, PoligrafSchema, RegistrySchema, WorkplaceSchema, AnketaSchema

bp.static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))


@bp.get('/', defaults={'path': ''})
@bp.get('/<string:path>')
@bp.get('/<path:path>')
@bp.doc(hide=True)
def main(path=''):
    """
    An API endpoint that serves static files from the bp.static_folder directory.

    Parameters:
    - path: A string that represents the file path within the bp.static_folder directory. Defaults to an empty string.

    Returns:
    - If the file path exists, returns the file from the bp.static_folder directory.
    - If the file path does not exist, returns the 'index.html' file from the bp.static_folder directory.
    """
    if path and os.path.exists(os.path.join(bp.static_folder, path)):
        return send_from_directory(bp.static_folder, path)
    else:
        return bp.send_static_file('index.html')


@bp.route('/index/<flag>/<int:page>', methods=['GET', 'POST'])
@bp.doc(hide=True)
@jwt_required()
def index(flag, page):
    pagination = 12
    match flag:
        case 'main':
            query = db.session.query(Person).order_by(Person.id.desc()). \
                paginate(page=page, per_page=pagination, error_out=False)
        case 'new':
            query = db.session.query(Person).filter(Person.status.in_(
                [Status.new.value, Status.update.value]
                ), Person.category == Category.candidate.value).\
                    order_by(Person.id.desc()).paginate(page=page, per_page=pagination, error_out=False)
        case 'officer': 
            query = db.session.query(Person).filter(Person.status.notin_(
                [Status.finish.value, Status.result.value, Status.cancel.value])). \
                    join(Check, isouter=True).filter_by(officer=current_user.username).order_by(Person.id.asc()). \
                        paginate(page=page, per_page=pagination, error_out=False)
        case 'search':
            search = request.get_json()
            query = db.session.query(Person).filter(
                or_(Person.fullname.ilike('%{}%'.format(search['fullname'])), search['fullname'] == ''),
                or_(Person.birthday.ilike('%{}%'.format(search['birthday'])), search['birthday'] == '')
                ).order_by(Person.id.asc()).paginate(page=page, per_page=pagination, error_out=False)
    resume_schema = PersonSchema()
    datas = resume_schema.dump(query, many=True)
    has_next, has_prev = int(query.has_next), int(query.has_prev)
    return [datas, {'has_next': has_next, "has_prev": has_prev}], 200


@bp.get('/persons/new')
@bp.doc(hide=True)
@jwt_required()
def get_counts():
    news = db.session.query(func.count(Person.id)).filter(Person.status.in_(
        [Status.new.value, Status.update.value]
        ), Person.category == Category.candidate.value).scalar()
    return {'news': news if news else 0}


@bp.get('/messages/<string:flag>')
@bp.doc(hide=True)
@bp.output(MessagesSchema)
@jwt_required()
def get_messages(flag):
    messages = db.session.query(Message).filter(Message.status == Status.new.value,
                                                Message.user_id == current_user.id).all()
    if flag == 'reply':
        for resp in messages:
            setattr(resp, 'status', Status.reply.value)
        db.session.commit()
        messages = []
    return dict(messages=messages)


@bp.get('/profile/<int:person_id>')
@bp.doc(hide=True)
@bp.output(ProfileSchema)
@jwt_required()
def get_profile(person_id):
    checks_list = db.session.query(Check).filter_by(person_id=person_id).order_by(Check.id.asc()).all()
    return dict(
        resume = db.session.query(Person).filter_by(id=person_id).all(),
        documents = db.session.query(Document).filter_by(person_id=person_id).order_by(Document.person_id.asc()).all(),
        addresses = db.session.query(Address).filter_by(person_id=person_id).order_by(Address.id.asc()).all(),
        contacts = db.session.query(Contact).filter_by(person_id=person_id).order_by(Contact.id.asc()).all(),
        workplaces = db.session.query(Workplace).filter_by(person_id=person_id).order_by(Workplace.id.asc()).all(),
        staffs = db.session.query(Staff).filter_by(person_id=person_id).order_by(Staff.id.asc()).all(),
        relations = db.session.query(Relation).filter_by(person_id=person_id).order_by(Relation.id.asc()).all(),
        checks = checks_list,
        registries = [db.session.query(Registry).filter_by(check_id=check.id).first() for check in checks_list],
        pfos = db.session.query(Poligraf).filter_by(person_id=person_id).order_by(Poligraf.id.asc()).all(),
        invs = db.session.query(Investigation).filter_by(person_id=person_id).order_by(Investigation.id.asc()).all(),
        inquiries = db.session.query(Inquiry).filter_by(person_id=person_id).order_by(Inquiry.id.asc()).all(),
    )


@bp.post('/resume/create')
@bp.input(PersonSchema)
@bp.doc(hide=True)
@jwt_required()
def post_resume(response):
    person_id, result = add_resume(response)
    return {'person_id': person_id, 'result': result}


@bp.post('/resume/upload')
@bp.doc(hide=True)
@jwt_required()
def upload_file():
    file = request.files['file']
    excel = ExcelFile(file)
    person_id, result = add_resume(excel.resume)
    resume_data(person_id, excel.passport, excel.addresses, excel.contacts, excel.workplaces, excel.staff)
    return {'person_id': person_id, 'result': bool(result)}


def add_resume(resume):
    result = db.session.query(Person).filter(Person.fullname.ilike(resume['fullname']),
                                             Person.birthday==resume['birthday']).one_or_none()
    if result:
        resume.update({'status': Status.update.value})
        for k, v in resume.items():
            setattr(result, k, v)
        person_id = result.id
    else:
        value = Person(**resume)
        db.session.add(value)
        db.session.flush()
        person_id = value.id
    db.session.commit()
    return [person_id, bool(result)]


@bp.post('/update/staff/<person_id>')
@bp.input(StaffSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def update_staff(person_id, response):
    db.session.add(Staff(**response | {'person_id': person_id}))
    db.session.commit()
    return ''


@bp.post('/update/document/<person_id>')
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


@bp.get('/resume/send/<int:person_id>')
@bp.doc(hide=True)
@jwt_required()
def send_resume(person_id):
    resume = db.session.query(Person).get(person_id)
    if resume.status in [Status.new.value, Status.update.value]:
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
    return {'message': Status.cancel.name}


@bp.get('/resume/status/<int:person_id>')
@bp.doc(hide=True)
@jwt_required()
def patch_status(person_id: int):
    person = Person.query.get(person_id)
    if person and person.status not in [Status.result.value, Status.poligraf.value]:
        person.status = Status.update.value
        db.session.commit()
        return {"message": Status.update.name}
    else:
        return {"message": Status.error.name}


@bp.get('/check/status/<int:person_id>')
@bp.doc(hide=True)
@jwt_required()
def status_check(person_id):
    person = Person.query.get(person_id)
    if person.status == Status.new.value or person.status == Status.update.value:
        person.status = Status.manual.value
        db.session.add(Check(officer=current_user.username, person_id = person_id))
        db.session.commit()
        return {'message': Status.manual.name}
    elif person.status == Status.manual.value:
        print(person.status)
        return {'message': Status.error.name}
    return {'message': Status.error.name}


@bp.post('/check/<flag>/<int:person_id>')
@bp.input(CheckSchema)
@bp.doc(hide=True)
@jwt_required()
def post_check(flag: str, person_id: int, response: dict):
    person = db.session.query(Person).get(person_id)
    latest_check = db.session.query(Check).filter_by(person_id=person_id).order_by(Check.id.desc()).first()
    if flag == 'new':
        path = os.path.join(BASE_PATH, person.fullname[0], f"{str(person.id)}-{person.fullname}",
                            datetime.now().strftime("%Y-%m-%d"))
        response.update({'path': path})
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
    if person.status not in [Status.result.value, Status.finish.value]:
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
    if not user.has_role(Roles.superuser.value):
        check_id = db.session.query(Check.id).filter_by(person_id=person_id).order_by(Check.id.desc()).one_or_none()
        reg = {'check_id': check_id, 'supervisor': current_user.username} | resp
        person = Person.query.get(person_id)
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
    return {'message': Status.error.name}


@bp.post('/poligraf/<int:person_id>')
@bp.input(PoligrafSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def post_poligraf(person_id, response):
    poligraf = Poligraf(**response, person_id=person_id, officer=current_user.username)
    db.session.add(poligraf)
    person = Person.query.get(person_id)
    if person.status == Status.poligraf.value:
        person.status = Status.result.value
    db.session.commit()
    return {'message': person_id}


@bp.post('/investigation/<int:person_id>')
@bp.input(InvestigationSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def post_investigation(person_id, response):
    db.session.add(Investigation(**response | {'person_id': person_id}))
    db.session.commit()
    return {'message': person_id}


@bp.post('/inquiry/<int:person_id>')
@bp.input(InquirySchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def post_inquiry(person_id, response):
    db.session.add(Inquiry(**response | {'person_id': person_id}))
    db.session.commit()
    return {'message': person_id}


@bp.post('/information')
@bp.doc(hide=True)
@jwt_required()
def post_information():
    period = request.get_json()
    candidates = db.session.query(Registry.decision, func.count(Registry.id)).group_by(Registry.decision). \
        filter(Registry.deadline.between(period['start'], period['end'])).all()
    pfo = db.session.query(Poligraf.theme, func.count(Poligraf.id)).group_by(Poligraf.theme). \
        filter(Poligraf.deadline.between(period['start'], period['end'])).all()
    return {
        "candidates": dict(map(lambda x: (x[1], x[0]), candidates)),
        "poligraf": dict(map(lambda x: (x[1], x[0]), pfo))
        }


@bp.errorhandler(BadRequest)
def handle_bad_request(e):
    return 'bad request!', 400
