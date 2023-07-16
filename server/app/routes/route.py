import json
import os
from datetime import datetime
import requests
from flask_jwt_extended import current_user, jwt_required

from sqlalchemy import func, or_
from flask import request, send_from_directory, render_template
from werkzeug.exceptions import BadRequest

from . import bp

from ..utils.excel import ExcelFile, resume_data, BASE_PATH
from ..models.model import User, db, Candidate, Staff, Document, Address, Contact, Workplace, \
    Check, Registry, Poligraf, Investigation, Inquiry, Status, Message
from ..models.schema import MessagesSchema, StaffSchema, AddressSchema, \
        CandidateSchema, ProfileSchema, ContactSchema, DocumentSchema, CheckSchema, InquirySchema, \
            InvestigationSchema, PoligrafSchema, RegistrySchema, WorkplaceSchema, AnketaSchema

bp.static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dist'))


@bp.route('/redoc')
def my_redoc():
    return render_template('/redoc.html')


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
    pagination = 16
    match flag:
        case 'main':
            query = db.session.query(Candidate).order_by(Candidate.id.desc()). \
                paginate(page=page, per_page=pagination, error_out=False)
        case 'new':
            query = db.session.query(Candidate).filter(Candidate.status.in_([Status.new.value,
                                                                             Status.update.value]))\
                .order_by(Candidate.id.desc()).paginate(page=page, per_page=pagination, error_out=False)
        case 'officer': 
            query = db.session.query(Candidate).filter(Candidate.status.notin_(
                [Status.finish.value, Status.result.value, Status.cancel.value])). \
                    join(Check, isouter=True).filter_by(officer=current_user.username).order_by(Candidate.id.asc()). \
                        paginate(page=page, per_page=pagination, error_out=False)
        case 'search':
            search = request.get_json()
            query = db.session.query(Candidate).filter(
                or_(Candidate.fullname.ilike('%{}%'.format(search['fullname'])), search['fullname'] == ''),
                or_(Candidate.birthday.ilike('%{}%'.format(search['birthday'])), search['birthday'] == '')
                ).order_by(Candidate.id.asc()).paginate(page=page, per_page=pagination, error_out=False)
    resume_schema = CandidateSchema()
    datas = resume_schema.dump(query, many=True)
    has_next, has_prev = int(query.has_next), int(query.has_prev)
    return [datas, {'has_next': has_next, "has_prev": has_prev}], 200


@bp.get('/candidates/new')
@bp.doc(hide=True)
@jwt_required()
def get_counts():
    news = db.session.query(func.count(Candidate.id)).filter(Candidate.status.in_
                                                             ([Status.new.value, Status.update.value])).scalar()
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


@bp.get('/profile/<int:cand_id>')
@bp.doc(hide=True)
@bp.output(ProfileSchema)
@jwt_required()
def get_profile(cand_id):
    checks_list = db.session.query(Check).filter_by(cand_id=cand_id).order_by(Check.id.asc()).all()
    return dict(
        resume = db.session.query(Candidate).filter_by(id=cand_id).all(),
        documents = db.session.query(Document).filter_by(cand_id=cand_id).order_by(Document.cand_id.asc()).all(),
        addresses = db.session.query(Address).filter_by(cand_id=cand_id).order_by(Address.id.asc()).all(),
        contacts = db.session.query(Contact).filter_by(cand_id=cand_id).order_by(Contact.id.asc()).all(),
        workplaces = db.session.query(Workplace).filter_by(cand_id=cand_id).order_by(Workplace.id.asc()).all(),
        staffs = db.session.query(Staff).filter_by(cand_id=cand_id).order_by(Staff.id.asc()).all(),
        checks = checks_list,
        registries = [db.session.query(Registry).filter_by(check_id=check.id).first() for check in checks_list],
        pfos = db.session.query(Poligraf).filter_by(cand_id=cand_id).order_by(Poligraf.id.asc()).all(),
        invs = db.session.query(Investigation).filter_by(cand_id=cand_id).order_by(Investigation.id.asc()).all(),
        inquiries = db.session.query(Inquiry).filter_by(cand_id=cand_id).order_by(Inquiry.id.asc()).all()
    )


@bp.post('/resume/create')
@bp.input(CandidateSchema)
@bp.doc(hide=True)
@jwt_required()
def post_resume(response):
    cand_id, result = add_resume(response)
    return {'cand_id': cand_id, 'result': result}


@bp.post('/resume/upload')
@bp.doc(hide=True)
@jwt_required()
def upload_file():
    file = request.files['file']
    excel = ExcelFile(file)
    cand_id, result = add_resume(excel.resume)
    resume_data(cand_id, excel.passport, excel.addresses, excel.contacts, excel.workplaces, excel.staff)
    return {'cand_id': cand_id, 'result': bool(result)}


def add_resume(resume):
    result = db.session.query(Candidate).filter(Candidate.fullname.ilike(resume['fullname']),
                                                Candidate.birthday==resume['birthday']).one_or_none()
    if result:
        resume.update({'status': Status.update.value, 'update': datetime.now()})
        for k, v in resume.items():
            setattr(result, k, v)
        cand_id = result.id
    else:
        value = Candidate(**resume)
        db.session.add(value)
        db.session.flush()
        cand_id = value.id
    db.session.commit()
    return [cand_id, bool(result)]


@bp.post('/update/staff/<cand_id>')
@bp.input(StaffSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def update_staff(cand_id, response):
    db.session.add(Staff(**response | {'cand_id': cand_id}))
    db.session.commit()
    return ''

@bp.post('/update/document/<cand_id>')
@bp.input(DocumentSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def update_document(cand_id, resonse):
    db.session.add(Document(**resonse | {'cand_id': cand_id}))
    db.session.commit()
    return ''


@bp.post('/update/contact/<cand_id>')
@bp.input(ContactSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def update_contact(cand_id, response):
    db.session.add(Contact(**response | {'cand_id': cand_id}))
    db.session.commit()
    return ''


@bp.post('/update/workplace/<cand_id>')
@bp.input(WorkplaceSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def update_workplace(cand_id, response):
    db.session.add(Workplace(**response | {'cand_id': cand_id}))
    db.session.commit()
    return ''


@bp.post('/update/address/<cand_id>')
@bp.input(AddressSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def update_address(cand_id, response):
    db.session.add(Address(**response | {'cand_id': cand_id}))
    db.session.commit()
    return ''


@bp.get('/resume/send/<int:cand_id>')
@bp.doc(hide=True)
@jwt_required()
def send_resume(cand_id):
    resume = db.session.query(Candidate).get(cand_id)
    if resume.status in [Status.new.value, Status.update.value]:
        anketa_schema = AnketaSchema()
        serial = anketa_schema.dump(dict(
            resume = resume, 
            document = db.session.query(Document).filter_by(cand_id=cand_id).order_by(Document.id.desc()).first(), 
            address = db.session.query(Address).filter_by(cand_id=cand_id).filter(Address.view.ilike("%регистрац%")).\
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
                                     cand_id=cand_id))
                db.session.commit()
                return {'message': Status.robot.name}
            return {'message': Status.error.name}
        except requests.exceptions.RequestException as e:
            print(e)
            return {'message': Status.error.name}
    return {'message': Status.cancel.name}


@bp.get('/resume/status/<int:cand_id>')
@bp.doc(hide=True)
@jwt_required()
def patch_status(cand_id: int):
    result = db.session.query(Candidate).filter_by(id=cand_id).one_or_none()
    if result and result.status not in [Status.result.value, Status.poligraf.value]:
        result.status = Status.update.value
        db.session.commit()
        return {"message": Status.update.name}
    else:
        return {"message": Status.error.name}


@bp.get('/check/status/<int:cand_id>')
@bp.doc(hide=True)
@jwt_required()
def status_check(cand_id):
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    if candidate.status == Status.new.value or candidate.status == Status.update.value:
        candidate.status = Status.manual.value
        db.session.commit()
        return {'message': Status.manual.name}
    return {'message': Status.error.name}


@bp.post('/check/<flag>/<int:cand_id>')
@bp.input(CheckSchema)
@bp.doc(hide=True)
@jwt_required()
def post_check(flag: str, cand_id: int, response):
    candidate = db.session.query(Candidate).get(cand_id)
    response['pfo'] = bool(response.pop('pfo')) if 'pfo' in response else False
    if flag == 'new':
        path = os.path.join(BASE_PATH, candidate.fullname[0], f"{str(candidate.id)}-{candidate.fullname}",
                            datetime.now().strftime("%Y-%m-%d"))
        response.update({'path': path, "cand_id": cand_id, "officer": current_user.username})
        db.session.add(Check(**response))
    else:
        response.update({"cand_id": cand_id, "officer": current_user.username})
        latest_check = db.session.query(Check).filter_by(cand_id=cand_id).order_by(Check.id.desc()).first()
        for k, v in response.items():
            setattr(latest_check, k, v)
    db.session.commit()
    if response['conclusion'] == 'Сохранено':
        candidate.status = Status.save.value
        db.session.commit()
        return {'message': Status.save.name}
    elif response['conclusion'] == "Отмена":
        candidate.status = Status.cancel.value
        db.session.commit()
        return {'message': Status.cancel.name}
    else:
        candidate.status = Status.poligraf.value if response['pfo'] else Status.result.value
        db.session.commit()
        return {'message': Status.poligraf.name if response['pfo'] else Status.result.name}


@bp.get('/check/delete/<int:cand_id>')
@bp.doc(hide=True)
@jwt_required()
def delete_check(cand_id):
    candidate = db.session.query(Candidate).get(cand_id)
    if candidate.status not in [Status.result.value, Status.finish.value]:
        latest_check = db.session.query(Check).filter_by(cand_id=cand_id).order_by(Check.id.desc()).first()
        if latest_check is not None:
            db.session.delete(latest_check)
            db.session.commit()
            return {'message': Status.reply.name}
    return {'message': Status.error.name}


@bp.post('/registry/<int:cand_id>')
@bp.input(RegistrySchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def post_registry(cand_id, resp):
    user = db.session.query(User.role).filter_by(username=current_user.username).one_or_none()
    if user.has_role('superuser'):
        check_id = db.session.query(Check.id).filter_by(cand_id=cand_id).order_by(Check.id.desc()).one_or_none()
        reg = {'check_id': check_id, 'supervisor': current_user.username} | resp
        candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
        try:
            response = requests.post(url='https://httpbin.org/post', 
                                     json=json.dumps({"id": candidate.request_id,
                                                      "deadline": datetime.now().strftime("%Y-%m-d%"),
                                                      "supervisor": current_user.username} | resp), timeout=5)
            response.raise_for_status()
            if response.status_code == 200:
                db.session.add(Registry(**reg))
                candidate.status = Status.cancel.value if reg['decision'] == Status.cancel.value else Status.finish.value
                db.session.commit()
                return {'message': Status.result.name}
            else:
                return {'message': Status.cancel.name}
        except Exception as e:
            print(e)
            return {"message": Status.error.name}
    return {'message': Status.error.name}


@bp.post('/poligraf/<int:cand_id>')
@bp.input(PoligrafSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def post_poligraf(cand_id, response):
    poligraf = Poligraf(**response, cand_id=cand_id, officer=current_user.username)
    db.session.add(poligraf)
    candidate = Candidate.query.get(cand_id)
    if candidate.status == Status.poligraf.value:
        candidate.status = Status.result.value
    db.session.commit()
    return {'message': cand_id}


@bp.post('/investigation/<int:cand_id>')
@bp.input(InvestigationSchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def post_investigation(cand_id, response):
    db.session.add(Investigation(**response | {'cand_id': cand_id}))
    db.session.commit()
    return {'message': cand_id}


@bp.post('/inquiry/<int:cand_id>')
@bp.input(InquirySchema, location='form')
@bp.doc(hide=True)
@jwt_required()
def post_inquiry(cand_id, response):
    db.session.add(Inquiry(**response | {'cand_id': cand_id}))
    db.session.commit()
    return {'message': cand_id}


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
