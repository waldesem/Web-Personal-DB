import json
import os
from datetime import datetime

import requests
from sqlalchemy import func
from flask import render_template, request
from flask_login import current_user, login_required

from . import bp
from ..extensions.extension import ExcelFile, resume_data, BASE_PATH, URL_CHECK
from ..models.model import Candidate, Staff, Document, Address, Contact, Workplace, RelationShip, \
    Check, Registry, Poligraf, Investigation, Inquiry, TODAY, db, serial_resume, resume_schema, \
    staff_schema, document_schema, address_schema, contact_schema, work_schema, relation_schema, \
    check_schema, poligraf_schema, registry_schema, investigation_schema, inquiry_schema
from ..forms.form import LoginForm, ResumeForm, StaffForm, DocumentForm, AddressForm, WorkplaceForm, SearchForm, \
    RelationshipForm, ContactForm, CheckForm, RegistryForm, FileForm, PoligrafForm, InvestigationForm, InquiryForm, \
    InfoForm, Status


@bp.errorhandler(404)
def page_not_found():
    return "Страница не найдена", 404


@bp.get('/')  # стартовый шаблон
def main():
    return render_template("index.html", form_login=LoginForm(), form_search=SearchForm(), form_file=FileForm(),
                           form_resume=ResumeForm(), form_check=CheckForm(), form_investigation=InvestigationForm(),
                           form_inquiry=InquiryForm(), form_poligraf=PoligrafForm(), form_staff=StaffForm(),
                           form_document=DocumentForm(), form_address=AddressForm(), form_work=WorkplaceForm(),
                           form_relation=RelationshipForm(), form_contact=ContactForm(), form_registry=RegistryForm(),
                           form_info=InfoForm())


@bp.route('/index/<flag>/<int:page>', methods=['GET', 'POST'])  # загрузка информации на главную страницу
@bp.doc(hide=True)
@login_required
def index(flag, page):
    pagination = 11
    results = None
    title = None
    items = db.session.query(func.count(Candidate.status)).filter_by(status=Status.NEWFAG.value).scalar()
    if request.method == 'GET':
        match flag:
            case 'main':
                title = "Главная страница"
                results = db.session.query(Candidate.id, Candidate.region, Candidate.fullname, Candidate.birthday,
                                           Candidate.status, Candidate.deadline).order_by(Candidate.id.desc()). \
                    offset(page * pagination).limit(pagination + 1).all()
            case 'new':
                title = "Новые анкеты"
                results = db.session.query(Candidate.id, Candidate.region, Candidate.fullname, Candidate.birthday,
                                           Candidate.status, Candidate.deadline). \
                    filter(Candidate.status == Status.NEWFAG.value).order_by(Candidate.id.desc()). \
                    offset(page * pagination).limit(pagination + 1).all()
            case 'officer':
                title = "Страница пользователя"
                results = db.session.query(Candidate.id, Candidate.region, Candidate.fullname, Candidate.birthday,
                                           Candidate.status, Candidate.deadline). \
                    filter(Candidate.status != Status.FINISH.value and Candidate.status != Status.CANCEL.value). \
                    join(Check, isouter=True).filter_by(officer=current_user.username). \
                    order_by(Candidate.id.asc()).offset(page * pagination).limit(pagination + 1).all()
    else:
        title = "Страница поиска"
        search_by: dict = request.form.to_dict()
        results = db.session.query(Candidate.id, Candidate.region, Candidate.fullname, Candidate.birthday,
                                   Candidate.status, Candidate.deadline).filter(
            Candidate.region.ilike(f'%{search_by["region"]}%' if search_by["region"] != '' else '%'),
            Candidate.fullname.ilike(f'%{search_by["fullname"]}%' if search_by["fullname"] != '' else '%'),
            Candidate.birthday.ilike(f'%{search_by["birthday"]}%' if search_by["birthday"] is not None else '%'),
            Candidate.status.ilike(f'%{search_by["status"]}%' if search_by["status"] != '' else '%')). \
            order_by(Candidate.id.asc()).offset(page * pagination).limit(pagination + 1).all()
    count_results = len(results)
    if count_results <= pagination:
        datas = resume_schema.dump(results, many=True)
        pager = 0
    else:
        datas = resume_schema.dump(results[:-1], many=True)
        pager = 1
    return [datas, {'pager': pager, 'items': items, 'title': title}]


@bp.post('/resume/create')
@bp.doc(hide=True)
@login_required
def post_resume():
    resume_dict: dict = request.form.to_dict()
    result = db.session.query(Candidate).filter(Candidate.fullname == resume_dict['fullname'],
                                                Candidate.birthday == resume_dict['birthday']).first()
    resume_dict['birthday'] = datetime.strptime(resume_dict.pop('birthday'), "%Y-%m-%d")
    if result:  # проверка существования такой же анкеты, если есть анкета с таким именем, обновляем данные
        resume_dict.update({'status': Status.UPDATE.value})
        for k, v in resume_dict.items():
            setattr(result, k, v)
            db.session.commit()
        cand_id = result.id
        message = 'Запись уже существует. Данные обновлены'
    else:  # если нет таких анкет, добавляем новую запись
        resume_dict.update({'status': Status.NEWFAG.value, 'deadline': TODAY})
        value = Candidate(**resume_dict)
        db.session.add(value)
        db.session.flush()
        cand_id = value.id
        db.session.commit()
        message = 'Создана новая запись'
    return {'cand_id': cand_id, 'message': message}


@bp.get('/profile/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def get_profile(cand_id):  # полный профиль кандидата/сотрудника
    cand = db.session.query(Candidate).filter_by(id=cand_id).all()
    candidate = resume_schema.dump(cand, many=True)
    doc = db.session.query(Document).filter_by(cand_id=cand_id).order_by(Document.cand_id.asc()).all()
    documents = document_schema.dump(doc, many=True)
    addr = db.session.query(Address).filter_by(cand_id=cand_id).order_by(Address.id.asc()).all()
    address = address_schema.dump(addr, many=True)
    cont = db.session.query(Contact).filter_by(cand_id=cand_id).order_by(Contact.id.asc()).all()
    contacts = contact_schema.dump(cont, many=True)
    work = db.session.query(Workplace).filter_by(cand_id=cand_id).order_by(Workplace.id.asc()).all()
    workplaces = work_schema.dump(work, many=True)
    rel = db.session.query(RelationShip).filter_by(cand_id=cand_id).order_by(RelationShip.id.asc()).all()
    relations = relation_schema.dump(rel, many=True)
    staf = db.session.query(Staff).filter_by(cand_id=cand_id).order_by(Staff.id.asc()).all()
    staffs = staff_schema.dump(staf, many=True)
    checkin = db.session.query(Check).filter_by(cand_id=cand_id).order_by(Check.id.asc()).all()
    checks = check_schema.dump(checkin, many=True)
    reg = [db.session.query(Registry).filter(Registry.check_id == i.id).first() for i in checkin]
    registries = registry_schema.dump(reg, many=True)
    pfo = db.session.query(Poligraf).filter_by(cand_id=cand_id).order_by(Poligraf.id.asc()).all()
    pfos = poligraf_schema.dump(pfo, many=True)
    inv = db.session.query(Investigation).filter_by(cand_id=cand_id).order_by(Investigation.id.asc()).all()
    invs = investigation_schema.dump(inv, many=True)
    inq = db.session.query(Inquiry).filter_by(cand_id=cand_id).order_by(Inquiry.id.asc()).all()
    inquiries = inquiry_schema.dump(inq, many=True)
    return [[candidate, staffs, documents, address, contacts, workplaces, relations],
            checks, registries, pfos, invs, inquiries, {i.name: i.value for i in Status}]


@bp.post('/upload')
@bp.doc(hide=True)
@login_required
def upload_file():
    file = request.files['file']  # получаем файл
    excel = ExcelFile(file)  # создаем экземпляр класса ExcelFile для разборки файла,
    result = db.session.query(Candidate).filter(Candidate.fullname.ilike(excel.resume['fullname']),
                                                Candidate.birthday == (excel.resume['birthday'])).first()
    if result:  # проверяем, есть анкета с таким именем; если есть, то обновляем основные данные
        resum = excel.resume | {'status': Status.NEWFAG.value, 'deadline': TODAY}
        for k, v in resum.items():
            setattr(result, k, v)
            db.session.commit()
        resume_data(result.id, excel.passport, excel.addresses, excel.contacts,
                    excel.workplaces, excel.staff)  # добавляем новые данные в базу данных
        cand_id = result.id
        message = 'Запись уже существует. Данные обновлены'
    else:  # если нет таких анкет, добавляем новую запись
        result = Candidate(**excel.resume | {'status': Status.NEWFAG.value, 'deadline': TODAY})
        db.session.add(result)
        db.session.flush()  # фиксируем id для последующей записи
        cand_id = result.id
        resume_data(result.id, excel.passport, excel.addresses, excel.contacts,
                    excel.workplaces, excel.staff)  # добавляем новые данные в базу данных
        db.session.commit()  # окончательно сохраняем в базу данных основные данные
        message = 'Создана новая запись'
    return {'cand_id': cand_id, 'message': message}


@bp.post('/update/<flag>/<cand_id>')
@bp.doc(hide=True)
@login_required
def update_profile(flag, cand_id):
    match flag:
        case "staffs":
            form_staff = request.form.to_dict()
            db.session.add(Staff(**form_staff | {'cand_id': cand_id}))
        case "documents":
            form_document: dict = request.form.to_dict()
            form_document['issue'] = datetime.strptime(form_document.pop('issue'), "%Y-%m-%d")
            db.session.add(Document(**form_document | {'cand_id': cand_id}))
        case "addresses":
            form_address = request.form.to_dict()
            db.session.add(Address(**form_address | {'cand_id': cand_id}))
        case "contacts":
            form_contact = request.form.to_dict()
            db.session.add(Contact(**form_contact | {'cand_id': cand_id}))
        case "workplaces":
            form_work = request.form.to_dict()
            db.session.add(Workplace(**form_work | {'cand_id': cand_id}))
        case "relations":
            form_relation: dict = request.form.to_dict()
            form_relation['birthday'] = datetime.strptime(form_relation.pop('birthday'), "%Y-%m-%d")
            db.session.add(RelationShip(**form_relation | {'cand_id': cand_id}))
    db.session.commit()
    return {"message": " Запись {} успешно добавлена".format(flag.upper())}


@bp.get('/resume/send/<int:cand_id>')  # отправка анкеты на проверку
@bp.doc(hide=True)
@login_required
def send_resume(cand_id):
    resume = db.session.query(Candidate).filter_by(id=cand_id).first()
    if resume.status == Status.NEWFAG.value or resume.status == Status.UPDATE.value:
        decer = serial_resume.decer_res(cand_id, officer=current_user.username)
        response = requests.post(url=URL_CHECK, json=decer, timeout=5)
        response.raise_for_status()
        if response.status_code == 200:  # проверка статуса отправки
            resume.status = Status.ROBOT.value  # устанавливаем статус Робот
            db.session.commit()
            return {'message': "Анкета успешно отправлена"}
        else:
            return {'message': "Отправка не удалась. Попробуйте позднее"}
    else:
        return {'message': "Анкета не может быть отправлена. Проверка уже начата"}


@bp.get('/resume/status/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def patch_status(cand_id):
    result = db.session.query(Candidate).filter_by(id=cand_id).first()
    if result.status not in [Status.RESULT.value, Status.POLIGRAF.value]:
        result.status = Status.UPDATE.value
        result.deadline = TODAY
        db.session.commit()
        return {"message": "Статус обновлен"}
    else:
        return {"message": "Текущий статус обновить нельзя"}


@bp.post('/check/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def post_check(cand_id):
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    path = os.path.join(BASE_PATH, candidate.fullname[0], f"{str(candidate.id)}-{candidate.fullname}",
                        TODAY.strftime("%Y-%m-%d"))
    # os.makedirs(path)  #  создаем папку для материалов проверки
    # os.startfile(path)  # открываем папку с проверкой
    check_form: dict = request.form.to_dict()
    check_form['deadline'] = datetime.strptime(check_form.pop('deadline'), "%Y-%m-%d")
    check_form['pfo'] = bool(check_form.pop('pfo'))
    check_form.update({'path': path, "cand_id": cand_id, 'officer': current_user.username})
    db.session.add(Check(**check_form))
    db.session.commit()
    if check_form['conclusion'] == Status.SAVE.value:
        candidate.status = Status.SAVE.value  # меняем статус анкеты сохранен
        db.session.commit()
        message = "Проверка успешно сохранена"
    elif check_form['conclusion'] == Status.CANCEL.value:
        candidate.status = Status.CANCEL.value
        db.session.commit()
        message = "Проверка отменена"
    else:
        if check_form['pfo']:  # если поставлена отметка ПФО меняем статус
            candidate.status = Status.POLIGRAF.value
            db.session.commit()
            message = "Проверка завершена. Назначено проведение ПФО"
        else:
            candidate.status = Status.RESULT.value
            db.session.commit()
            message = "Проверка завершена"
    return {'message': message}


@bp.get('/check/delete/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def delete_check(cand_id):  # запрашиваем данные проверки
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    if candidate.status != Status.FINISH.value:
        result = db.session.query(Check).filter_by(cand_id=cand_id).order_by(Check.id.desc()).first()
        Check.query.filter_by(id=result.id).delete()
        db.session.commit()
        return {'message': "Проверка успешно удалена"}
    else:
        return {'message': "Проверка с текущим статусом не может быть удалена"}


@bp.get('/check/status/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def status_check(cand_id):  # запрашиваем данные проверки
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    if candidate.status == Status.NEWFAG.value or candidate.status == Status.UPDATE.value:
        message = "Анкета взята в работу и еще не закончена"
    else:
        candidate.status = Status.MANUAL.value
        db.session.commit()
        message = "Начата ручная проверка"
    return {'message': message}


@bp.post('/registry/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def post_registry(cand_id):
    form_registry = request.form.to_dict()  # загружаем форму согласования
    result = db.session.query(Check).filter_by(cand_id=cand_id).order_by(Check.id.desc()).first()
    reg = form_registry | {'check_id': result.id, 'supervisor': current_user.username, 'deadline': TODAY}
    db.session.add(Registry(**reg))  # получаем данные из формы и записываем в базу данных
    db.session.commit()
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    response = requests.post(url=URL_CHECK, json=json.dumps(
        {
            "id": candidate.request_id,
            "comments": reg['comments'],
            "decision": reg['decision'],
            "deadline": TODAY.strftime("%Y-%m-d%"),
            "supervisor": reg['supervisor']
        }
    ), timeout=5)
    response.raise_for_status()
    if response.status_code == 200:  # проверка статуса отправки
        if reg['decision'] == Status.CANCEL.value:
            candidate.status = Status.CANCEL.value  # меняем статус в таблице на "Отмена"
            db.session.commit()
        else:
            candidate.status = Status.FINISH.value  # меняем статус в таблице на "Решение "
            db.session.commit()
        return {'message': "Решение успешно отправлено"}
    else:
        return {'message': 'Отправка не удалась попробуйте еще раз позднее'}


@bp.post('/poligraf/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def post_poligraf(cand_id):
    form_poligraf: dict = request.form.to_dict()
    form_poligraf['deadline'] = datetime.strptime(form_poligraf.pop('deadline'), "%Y-%m-%d")
    db.session.add(Poligraf(**form_poligraf | {'cand_id': cand_id} | {'officer': current_user.username}))
    db.session.commit()
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    if candidate.status == Status.POLIGRAF.value:  # проверяем статус, если указано ПФО, завершаем
        candidate.status = Status.RESULT.value
        db.session.commit()
    return {"message": " Запись успешно добавлена"}


@bp.post('/investigation/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def post_investigation(cand_id):
    form_investigation: dict = request.form.to_dict()  # получаем данные из формы
    form_investigation['deadline'] = datetime.strptime(form_investigation.pop('deadline'), "%Y-%m-%d")
    db.session.add(Investigation(**form_investigation | {'cand_id': cand_id}))
    db.session.commit()  # передаем в БД
    return {"message": " Запись успешно добавлена"}


@bp.post('/inquiry/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def post_inquiry(cand_id):
    form_inquiry: dict = request.form.to_dict()
    form_inquiry['deadline'] = datetime.strptime(form_inquiry.pop('deadline'), "%Y-%m-%d")
    db.session.add(Inquiry(**form_inquiry | {'cand_id': cand_id}))
    db.session.commit()
    return {"message": " Запись успешно добавлена"}


@bp.post('/information')
@bp.doc(hide=True)
@login_required
def post_information():
    statistic = request.form.to_dict()
    candidates = db.session.query(Registry.decision, func.count(Registry.id)). \
        group_by(Registry.decision).filter(Registry.deadline.between(statistic['start'], statistic['end'])).all()
    pfo = db.session.query(Poligraf.theme, func.count(Poligraf.id)). \
        group_by(Poligraf.theme).filter(Poligraf.deadline.between(statistic['start'], statistic['end'])).all()
    return {"candidates": [dict([cand]) for cand in candidates], "poligraf": [dict([test]) for test in pfo],
            "title": f'Cтатистика за период c {statistic["start"]} по {statistic["end"]}'}
