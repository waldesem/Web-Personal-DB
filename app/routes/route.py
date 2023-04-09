import os
from datetime import datetime

import requests
from sqlalchemy import func, extract
from flask import render_template, request, jsonify
from flask_login import current_user, login_required

from . import bp
from ..extensions.extension import ExcelFile, resume_data, BASE_PATH, URL_CHECK
from ..models.model import Candidate, Staff, Document, Address, Contact, Workplace, RelationShip, \
    Check, Registry, Poligraf, Investigation, Inquiry, db, decerial_resume, resume_schema, \
        investigation_schema, inquiry_schema, poligraf_schema, relation_schema, staff_schema, \
            document_schema, address_schema, contact_schema, work_schema, check_schema, \
                registry_schema, Status, TODAY

PAGINATION = 2


@bp.route('/', methods=['GET', 'POST'])  # стартовый шаблон
def start():
    return render_template('index.html')


@bp.route('/index/<int:page>', methods=['GET', 'POST'])  # главная страница
@login_required
def index(page):
    results = db.session.query(Candidate.id, Candidate.region, Candidate.fullname, Candidate.birthday,
                            Candidate.status, Candidate.deadline).order_by(Candidate.id.desc()). \
                            offset(page * PAGINATION).limit(PAGINATION+1).all()
    count_results = len(results)
    if count_results < PAGINATION:
        datas = resume_schema.dump(results, many=True)
        pager = 0
    else:
        datas = resume_schema.dump(results[:-1], many=True)
        pager = 1
    items = db.session.query(func.count(Candidate.status)).filter_by(status=Status.NEWFAG.value).scalar()
    return jsonify(data=[datas]+[{'items': items}]+[{'pager': pager}])


@bp.route('/officer/<int:page>', methods=['GET', 'POST'])  # главная страница
#@login_required
def officer(page=0):
    PAGINATION = 2
    results = db.session.query(Candidate).filter(Candidate.status != Status.FINISH.value,
                                                 Candidate.status != Status.CANCEL.value).join(Check, isouter=True). \
        filter_by(officer=current_user.username).order_by(Candidate.id.asc()).offset(page * PAGINATION).limit(
        PAGINATION).all()
    count_results = len(results)
    if count_results < PAGINATION:
        datas = resume_schema.dump(results, many=True)
        pager = 0
    else:
        datas = resume_schema.dump(results[:-1], many=True)
        pager = 1
    return jsonify(data=[datas]+[{'items': count_results}]+[{'pager': pager}])


@bp.route('/fastsearch/<int:page>', methods=['GET', 'POST'])  # главная страница
@login_required
def fastsearch(page=0):
    user_form = request.form.to_dict()
    search_by = user_form['fullname']
    results = db.session.query(Candidate).filter(Candidate.fullname.ilike(f'%{search_by}%')). \
        offset(page * PAGINATION).limit(PAGINATION+1).all()
    count_results = len(results)
    if count_results < PAGINATION:
        datas = resume_schema.dump(results, many=True)
        pager = 0
    else:
        datas = resume_schema.dump(results[:-1], many=True)
        pager = 1
    return jsonify(data=[datas]+[{'items': count_results}]+[{'pager': pager}])


@bp.route('/extsearch/<int:page>', methods=['GET', 'POST'])  # главная страница
@login_required
def extsearch(page=0):
    search_by = request.form.to_dict()
    form_dict = {k: v for k, v in search_by.items()}
    print(form_dict)
    results = db.session.query(Candidate).filter(Candidate.region.ilike(f'%{form_dict["region"]}%'
            if form_dict["region"] != '' else '%'), Candidate.fullname.ilike(f'%{form_dict["fullname"]}%'
            if form_dict["fullname"] != '' else '%'), Candidate.birthday.ilike(f'%{form_dict["birthday"]}%'
            if form_dict["birthday"] is not None else '%')). \
        join(Document, isouter=True).filter(Document.number.ilike(f'%{form_dict["number"]}%'
                                                                    if form_dict["number"] != '' else '%')). \
        join(Contact, isouter=True).filter(Contact.contact.ilike(f'%{form_dict["contact"]}%'
                                                                    if form_dict["contact"] != '' else '%')). \
        offset(page * PAGINATION).limit(PAGINATION+1).all()
    count_results = len(results)
    if count_results < PAGINATION:
        datas = resume_schema.dump(results, many=True)
        pager = 0
    else:
        datas = resume_schema.dump(results[:-1], many=True)
        pager = 1
    return jsonify(data=[datas]+[{'items': count_results}]+[{'pager': pager}])


@bp.route('/resume', methods=['GET', 'POST'])  # добавляем новую анкету
@login_required
def resume():
    resume_dict = request.form.to_dict()
    resume_dict['birthday'] = datetime.strptime(resume_dict['birthday'], "%Y-%m-%d")
    result = db.session.query(Candidate).filter(Candidate.fullname == resume_dict['fullname'],
                                                Candidate.birthday == resume_dict['birthday']).first()
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
    return jsonify(data=[{'cand_id': cand_id}, {'message': message}])


@bp.route('/upload', methods=['GET', 'POST'])  # загрузка анкеты из файла Excel
@login_required
def upload():
    file = request.files['file']  # получаем файл
    excel = ExcelFile(file)  # создаем экземпляр класса ExcelFile для разборки файла,
    result = db.session.query(Candidate).filter(Candidate.fullname.ilike(excel.resume['fullname']),
                                                Candidate.birthday == (excel.resume['birthday'])).first()
    if result:  # проверяем, есть анкета с таким именем; если есть, то обновляем основные данные
        resum = excel.resume | {'status': Status.UPDATE.value, 'deadline': TODAY}
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
    return jsonify(data=[{'cand_id': cand_id}, {'message': message}])


@bp.route('/profile/<int:cand_id>', methods=['GET', 'POST'])  # загрузка профиля кандидата
@login_required
def profile(cand_id):  # полный профиль кандидата/сотрудника
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
    check = db.session.query(Check).filter_by(cand_id=cand_id).order_by(Check.id.asc()).all()
    checks = check_schema.dump(check, many=True)
    reg = [db.session.query(Registry).filter(Registry.check_id == i.id).first() for i in check]
    registries = registry_schema.dump(reg, many=True)
    pfo = db.session.query(Poligraf).filter_by(cand_id=cand_id).order_by(Poligraf.id.asc()).all()
    pfos = poligraf_schema.dump(pfo, many=True)
    inv = db.session.query(Investigation).filter_by(cand_id=cand_id).order_by(Investigation.id.asc()).all()
    invs = investigation_schema.dump(inv, many=True)
    inq = db.session.query(Inquiry).filter_by(cand_id=cand_id).order_by(Inquiry.id.asc()).all()
    inquiries = inquiry_schema.dump(inq, many=True)
    return jsonify(data=[candidate, staffs, documents, address, relations, workplaces, 
                         contacts, checks, registries, inquiries, pfos, invs, {i.name: i.value for i in Status}])


@bp.route('/resume/update/<int:cand_id>', methods=['GET', 'POST'])  # update ststus
@login_required
def update_resume(cand_id):
    result = db.session.query(Candidate).filter_by(id=cand_id).first()
    if result.status not in [Status.RESULT.value, Status.POLIGRAF.value]:
        result.status = Status.UPDATE.value
        result.deadline = TODAY
        db.session.commit()
        result = db.session.query(Candidate).filter_by(id=cand_id).first()
        datas = resume_schema.dump(result, many=True)
        return jsonify(data=[datas, {"message": "Статус обновлен"}, {i.name: i.value for i in Status}])
    else:
        return jsonify(data=[datas, {"message": "Текущий статус обновить нельзя"}, {i.name: i.value for i in Status}])


@bp.route('/resume/edit/<int:cand_id>', methods=['GET', 'POST'])  # edit resume
@login_required
def edit_resume(cand_id):
    result = db.session.query(Candidate).filter_by(id=cand_id).first()
    decerial = resume_schema.dump(result, many=True)
    return jsonify(data=decerial)        


@bp.route('/add/<flag>/<int:cand_id>', methods=['GET', 'POST'])
#@login_required
def add(flag, cand_id):  # добавление данных через модальные окна
    match flag:
        case "formInvestigation":
            form_investigation = request.form("formInvestigation")  # получаем данные из формы
            if form_investigation.validate_on_submit():
                db.session.add(Investigation(**{k: v for k, v in form_investigation.data.items()} | {'cand_id': cand_id}))
                db.session.commit()  # передаем в БД
                result = db.session.query(Investigation).filter_by(cand_id=cand_id).all()
                decerial = investigation_schema.dump(result, many=True)
                return jsonify(data=decerial+[{"message": "Запись успешно добавлена"}])
        case "formInquiry":
            form_inquiry = request.form("formInquiry")
            if form_inquiry.validate_on_submit():
                db.session.add(Inquiry(**{k: v for k, v in form_inquiry.data.items()}| {'cand_id': cand_id}))
                db.session.commit()
                result = db.session.query(Inquiry).filter_by(cand_id=cand_id).all()
                decerial = inquiry_schema.dump(result, many=True)
                return jsonify(data=decerial+[{"message": "Запись успешно добавлена"}])
        case "formPoligraf":
            form_poligraf = request.form("formPoligraf")
            if form_poligraf.validate_on_submit():
                db.session.add(Poligraf(**{k: v for k, v in form_poligraf.data.items()} | {'cand_id': cand_id} |
                                            {'officer': current_user.username}))
                db.session.commit()
                candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
                if candidate.status == Status.POLIGRAF.value:  # проверяем статус, если указано ПФО, завершаем
                    candidate.status = Status.RESULT.value
                    db.session.commit()
                result = db.session.query(Poligraf).filter_by(cand_id=cand_id).all()
                decerial = poligraf_schema.dump(result, many=True)
                return jsonify(data=decerial+[{"message": "Запись успешно добавлена"}])
        case "formStaff":
            form_staff = request.form("formStaff")
            if form_staff.validate_on_submit():
                db.session.add(Staff(**{k: v for k, v in form_staff.data.items()} | {'cand_id': cand_id}))
                db.session.commit()
                result = db.session.query(Staff).filter_by(cand_id=cand_id).all()
                decerial = staff_schema.dump(result, many=True)
                return jsonify(data=decerial+[{"message": "Запись успешно добавлена"}])
        case "formDocument":
            form_document = request.form("formDocument")
            if form_document.validate_on_submit():
                db.session.add(Document(**{k: v for k, v in form_document.data.items()} | {'cand_id': cand_id}))
                db.session.commit()
                result = db.session.query(Document).filter_by(cand_id=cand_id).all()
                decerial = document_schema.dump(result, many=True)
                return jsonify(data=decerial+[{"message": "Запись успешно добавлена"}])
        case "formAddress":
            form_address = request.form("formAddress")
            if form_address.validate_on_submit():
                db.session.add(Address(**{k: v for k, v in form_address.data.items()} | {'cand_id': cand_id}))
                db.session.commit()
                result = db.session.query(Address).filter_by(cand_id=cand_id).all()
                decerial = address_schema.dump(result, many=True)
                return jsonify(data=decerial+[{"message": "Запись успешно добавлена"}])
        case "formContact":
            form_contact = request.form("formContact")
            if form_contact.validate_on_submit():
                db.session.add(Contact(**{k: v for k, v in form_contact.data.items()} | {'cand_id': cand_id}))
                db.session.commit()
                result = db.session.query(Contact).filter_by(cand_id=cand_id).all()
                decerial = contact_schema.dump(result, many=True)
                return jsonify(data=decerial+[{"message": "Запись успешно добавлена"}])
        case "formWorkplace":
            form_work = request.form("formWorkplace")
            if form_work.validate_on_submit():
                db.session.add(Workplace(**{k: v for k, v in form_work.data.items()} | {'cand_id': cand_id}))
                db.session.commit()
                result = db.session.query(Workplace).filter_by(cand_id=cand_id).all()
                decerial = work_schema.dump(result, many=True)
                return jsonify(data=decerial+[{"message": "Запись успешно добавлена"}])
        case "formRelation":
            form_relation = request.form("formRelation")
            if form_relation.validate_on_submit():
                db.session.add(RelationShip(**{k: v for k, v in form_relation.data.items()} | {'cand_id': cand_id}))
                db.session.commit()
                result = db.session.query(RelationShip).filter_by(cand_id=cand_id).all()
                decerial = relation_schema.dump(result, many=True)
                return jsonify(data=decerial+[{"message": "Запись успешно добавлена"}])
        case _:
            return jsonify(data=[]+[{"message": "Error"}])


@bp.route('/resume/send/<int:cand_id>', methods=['GET'])  # отправка анкеты на проверку
def send_resume(cand_id):
    resum = db.session.query(Candidate).filter_by(id=cand_id).first()
    if resum.status == Status.NEWFAG.value or resum.status == Status.UPDATE.value:
        decer = decerial_resume.decer_res(cand_id, officer=current_user.username)  # десериализация анкетных данных
        response = requests.post(url=URL_CHECK, json=decer, timeout=5)
        response.raise_for_status()
        if response.status_code == 200:  # проверка статуса отправки
            resum.status = Status.ROBOT.value  # устанавливаем статус Робот
            db.session.commit()
            jsonify(data={'message': "Анкета успешно отправлена"})
        else:
            jsonify(data={'message': "Отправка не удалась. Попробуйте позднее"})
    else:
        jsonify(data={'message': "Анкета не может быть отправлена. Проверка уже начата"})


@bp.route('/check/<int:cand_id>', methods=['GET', 'POST'])  # добавить проверку
@login_required  # форма проверки кандидата
def check(cand_id):
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    if candidate.status not in [Status.NEWFAG.value, Status.UPDATE.value]:
        return jsonify(data={'message': "Анкета взята в работу и еще не закончена"})
    else: 
        path = os.path.join(BASE_PATH, candidate.fullname[0], f"{str(candidate.id)}-{candidate.fullname}",
                            TODAY.strftime("%Y-%m-%d"))
        # os.makedirs(path)  #  создаем папку для материалов проверки
        # os.startfile(path)  # открываем папку с проверкой
        check_form = request.form('checkForm')
        check_dict = {k: v for k, v in check_form.data.items()} | {'officer': current_user.username}
        check_dict.update({'path': path, "cand_id": cand_id})
        db.session.add(Check(**check_dict))
        db.session.commit()
        if check_dict['conclusion'] == Status.SAVE.value:
            candidate.status = Status.SAVE.value  # меняем статус анкеты сохранен
            db.session.commit()
            message = "Проверка успешно сохранена"
        elif check_dict['conclusion'] == Status.CANCEL.value:
            candidate.status = Status.CANCEL.value
            db.session.commit()
            message = "Проверка отменена"
        else:
            if check_dict['pfo']:  # если поставлена отметка ПФО меняем статус
                candidate.status = Status.POLIGRAF.value
                db.session.commit()
                message = "Проверка завершена. Назначено проведение ПФО"
            else:
                candidate.status = Status.RESULT.value
                db.session.commit()
                message = "Проверка завершена"
        return jsonify(data={'message': message})


@bp.route('/check/edit/<int:cand_id>', methods=['GET', 'POST'])  # редактировать проверку
@login_required  # форма проверки кандидата
def check_edit(cand_id):
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    result = db.session.query(Check).filter_by(check_id=candidate.id).desc().first()  # запрашиваем данные проверки
    if candidate.status in [Status.SAVE.value, Status.REPLY.value]:
        candidate.status = Status.MANUAL.value  # меняем статус анкеты
        db.session.commit()
        return jsonify(data={'message': "Проверку с текущим статусом нельзя отредактировать"})
    else:
        decer = check_schema.dump(result, many=True)
        return jsonify(data={decer})


@bp.route('/check/delete/<int:cand_id>', methods=['GET', 'POST'])  # удалить проверку
@login_required  # форма проверки кандидата
def delete(cand_id):
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    result = db.session.query(Check).filter_by(check_id=candidate.id).desc().first()  # запрашиваем данные проверки
    Check.query.filter_by(id=result.id).delete()
    db.session.commit()
    return jsonify(data={'message': "Проверка успешно удалена"})


@bp.route('/registr/<int:cand_id>/<int:check_id>', methods=('GET', 'POST'))  # отправка решения по кандидату
#@login_required
def registry(cand_id, check_id):
    form_registry = request.form("formRegistry")  # загружаем форму согласования
    reg = {k: v for k, v in form_registry.data.items()} | \
            {'check_id': check_id, 'supervisor': current_user.username, 'deadline': TODAY}
    db.session.add(Registry(**reg))  # получаем данные из формы и записываем в базу данных
    db.session.commit()
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    registr = db.session.query(Registry).filter_by(cand=cand_id).all()
    decerial = registry_schema.dumps(registr, many=True)
    response = requests.post(url=URL_CHECK, json=jsonify(
        {
            "id": candidate.request_id,
            "comments": reg['comments'],
            "decision": reg['decision'],
            "deadline": TODAY,
            "supervisor": reg['supervisor']
        },
        default=str), timeout=5)
    response.raise_for_status()
    if response.status_code == 200:  # проверка статуса отправки
        if reg['decision'] == Status.CANCEL.value:
            candidate.status = Status.CANCEL.value  # меняем статус в таблице на "Отмена"
            db.session.commit()
        else:
            candidate.status = Status.FINISH.value  # меняем статус в таблице на "Решение "
            db.session.commit()
        #flash(Markup("Решение успешно отправлено"), 'success')
    else:
        #flash(Markup("Отправка анкеты не удалась попробуйте еще раз позднее"), 'warning')
        return jsonify(data=decerial+[{'flag': 'resume'}])


@bp.route('/info', methods=('GET', 'POST'))  # create statistic info
@login_required
def info():
    if request.method == 'GET':
        candidates = db.session.query(Registry.decision, func.count(Registry.id)). \
            group_by(Registry.decision).filter(extract('year', Registry.deadline) == TODAY.year).all()
        poligraf = db.session.query(Poligraf.theme, func.count(Poligraf.id)). \
            group_by(Poligraf.theme).filter(extract('year', Poligraf.deadline) == TODAY.year).all()
        # return ('info.html', form=statinfo, candidates=candidates, poligraf=poligraf,
        #                    title=f'Статистика за {TODAY.year} год')
    
    if request.method == 'POST':
        statinfo = request.form("InfoForm")
        candidates = db.session.query(Registry.decision, func.count(Registry.id)). \
            group_by(Registry.decision).filter(Registry.deadline.between(statinfo.start.data, statinfo.end.data)).all()
        poligraf = db.session.query(Poligraf.theme, func.count(Poligraf.id)). \
            group_by(Poligraf.theme).filter(Poligraf.deadline.between(statinfo.start.data, statinfo.end.data)).all()
        # return ('info.html', form=statinfo, candidates=candidates, poligraf=poligraf,
        #                        title=f'Cтатистика за период c {statinfo.start.data.strftime("%d.%m.%Y")} по '
        #                              f'{statinfo.end.data.strftime("%d.%m.%Y")}')"
