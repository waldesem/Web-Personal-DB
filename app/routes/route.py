import os
import json

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
    form_dict = {k: v for k, v in search_by.items() if k not in ['submit', 'csrf_token']}
    results = db.session.query(Candidate).filter(Candidate.region.ilike(f'%{form_dict["region"]}%'
            if form_dict["region"] != '' else '%'), Candidate.fullname.ilike(f'%{form_dict["fullname"]}%'
            if form_dict["fullname"] != '' else '%'), Candidate.birthday.ilike(f'%{form_dict["birthday"]}%'
            if form_dict["birthday"] is not None else '%')). \
        join(Staff, isouter=True).filter(Staff.position.ilike(f'%{form_dict["position"]}%' 
                                                                if form_dict["position"] != '' else '%')). \
        join(Document, isouter=True).filter(Document.number.ilike(f'%{form_dict["number"]}%'
                                                                    if form_dict["number"] != '' else '%')). \
        join(Address, isouter=True).filter(Address.address.ilike(f'%{form_dict["address"]}%'
                                                                    if form_dict["address"] != '' else '%')). \
        join(Workplace, isouter=True).filter(Workplace.workplace.ilike(f'%{form_dict["workplace"]}%'
                                                                        if form_dict["workplace"] != '' else '%')). \
        join(Contact, isouter=True).filter(Contact.contact.ilike(f'%{form_dict["contact"]}%'
                                                                    if form_dict["contact"] != '' else '%')). \
        offset(page * PAGINATION).limit(PAGINATION+1)
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
    candidate = request.form('formMultiform')
    resume_dict = {k: v for k, v in candidate.data.items() if k not in ['submit', 'csrf_token']}
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
    return jsonify(data=cand_id, message=message)


@bp.route('/upload', methods=['GET', 'POST'])  # загрузка анкеты из файла Excel
#@login_required
def upload():
    file = request.files['file']  # получаем файл
    excel = ExcelFile(file)  # создаем экземпляр класса ExcelFile для разборки файла,
    result = db.session.query(Candidate).filter(Candidate.fullname.ilike(excel.resume['fullname']),
                                                Candidate.birthday == (excel.resume['birthday'])).first()
    if result:  # проверяем, есть анкета с таким именем; если есть, то обновляем основные данные
        for k, v in excel.resume.items() | {'status': Status.UPDATE.value, 'deadline': TODAY}:
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
    return jsonify(data=cand_id, message=message)


@bp.route('/profile/<int:cand_id>', methods=['GET', 'POST'])  # загрузка профиля кандидата
#@login_required
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


# @bp.route('/actions/<action>/<int:cand_id>', methods=['GET', 'POST'])  # редактируем/обновляем анкету
# @login_required
# def actions(action, cand_id):
#     result = db.session.query(Candidate).filter_by(id=cand_id).first()
#     if action == 'update':
#         if result.status not in [Status.RESULT.value, Status.POLIGRAF.value]:
#             result.status = Status.UPDATE.value
#             result.deadline = TODAY
#             db.session.commit()
#             result = db.session.query(Candidate).filter_by(id=cand_id).first()
#             data = resume_schema.dump(result, many=True)
#             return jsonify(data=data+[{'message': "Статус обновлен"}])
#         else:
#             return jsonify([{'message': "Статус обновлен"}]+[{'state': 'warning'}])  
    
#     if request.method == 'POST' and action == 'edit':  # получаем данные из формы
#         resume_dict = {k: v for k, v in candidate.data.items() if k not in ['submit', 'csrf_token']}
#         for k, v in resume_dict.items():
#             setattr(result, k, v)
#             db.session.commit()
#         flash(Markup('Данные обновлены'), 'info')
#         result = db.session.query(Candidate).filter_by(id=cand_id).all()
#         decerial = resume_schema.dump(result, many=True)
#         return jsonify(data=decerial+[{'flag': 'resume'}])


# @bp.route('/add/<flag>/<int:cand_id>', methods=['GET', 'POST'])
# #@login_required
# def add(flag, cand_id):  # добавление данных через модальные окна
#     if request.method == 'POST':
#         match flag:
#             case "form_investigation":
#                 form_investigation = InvestigationForm(request.form)  # получаем данные из формы
#                 if form_investigation.validate_on_submit():
#                     db.session.add(Investigation(**{k: v for k, v in form_investigation.data.items() if
#                                                     k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
#                     db.session.commit()  # передаем в БД
#                     flash(Markup(f"Запись успешно добавлена"), 'success')
#                     result = db.session.query(Investigation).filter_by(cand_id=cand_id).all()
#                     decerial = investigation_schema.dump(result, many=True)
#                     return jsonify(data=decerial+[{'flag': 'investigation'}])
#             case "form_inquiry":
#                 form_inquiry = InquiryForm(request.form)
#                 if form_inquiry.validate_on_submit():
#                     db.session.add(Inquiry(**{k: v for k, v in form_inquiry.data.items() if
#                                               k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
#                     db.session.commit()
#                     flash(Markup(f"Запись успешно добавлена"), 'success')
#                     result = db.session.query(Inquiry).filter_by(cand_id=cand_id).all()
#                     decerial = inquiry_schema.dump(result, many=True)
#                     return jsonify(data=decerial+[{'flag': 'inquiry'}])
#             case "form_poligraf":
#                 form_poligraf = PoligrafForm(request.form)
#                 if form_poligraf.validate_on_submit():
#                     db.session.add(Poligraf(**{k: v for k, v in form_poligraf.data.items() if
#                                                k not in ['submit', 'csrf_token']} | {'cand_id': cand_id} |
#                                               {'officer': current_user.username}))
#                     db.session.commit()
#                     candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
#                     if candidate.status == Status.POLIGRAF.value:  # проверяем статус, если указано ПФО, завершаем
#                         candidate.status = Status.RESULT.value
#                         db.session.commit()
#                     flash(Markup(f"Запись успешно добавлена"), 'success')
#                     result = db.session.query(Poligraf).filter_by(cand_id=cand_id).all()
#                     decerial = poligraf_schema.dump(result, many=True)
#                     return jsonify(data=decerial+[{'flag': 'poligraf'}])
#             case "form_staff":
#                 form_staff = StaffForm(request.form)
#                 if form_staff.validate_on_submit():
#                     db.session.add(Staff(**{k: v for k, v in form_staff.data.items() if
#                                             k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
#                     db.session.commit()
#                     result = db.session.query(Staff).filter_by(cand_id=cand_id).all()
#                     decerial = staff_schema.dump(result, many=True)
#                     return jsonify(data=decerial+[{'flag': 'staff'}])
#             case "form_document":
#                 form_document = DocumentForm(request.form)
#                 if form_document.validate_on_submit():
#                     db.session.add(Document(**{k: v for k, v in form_document.data.items() if
#                                                k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
#                     db.session.commit()
#                     result = db.session.query(Document).filter_by(cand_id=cand_id).all()
#                     decerial = document_schema.dump(result, many=True)
#                     return jsonify(data=decerial+[{'flag': 'document'}])
#             case "form_address":
#                 form_address = AddressForm(request.form)
#                 if form_address.validate_on_submit():
#                     db.session.add(Address(**{k: v for k, v in form_address.data.items() if
#                                               k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
#                     db.session.commit()
#                     result = db.session.query(Address).filter_by(cand_id=cand_id).all()
#                     decerial = address_schema.dump(result, many=True)
#                     return jsonify(data=decerial+[{'flag': 'address'}])
#             case "form_contact":
#                 form_contact = ContactForm(request.form)
#                 if form_contact.validate_on_submit():
#                     db.session.add(Contact(**{k: v for k, v in form_contact.data.items() if
#                                               k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
#                     db.session.commit()
#                     result = db.session.query(Contact).filter_by(cand_id=cand_id).all()
#                     decerial = contact_schema.dump(result, many=True)
#                     return jsonify(data=decerial+[{'flag': 'contact'}])
#             case "form_work":
#                 form_work = WorkplaceForm(request.form)
#                 if form_work.validate_on_submit():
#                     db.session.add(Workplace(**{k: v for k, v in form_work.data.items() if
#                                                 k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
#                     db.session.commit()
#                     result = db.session.query(Workplace).filter_by(cand_id=cand_id).all()
#                     decerial = work_schema.dump(result, many=True)
#                     return jsonify(data=decerial+[{'flag': 'work'}])
#             case "form_relation":
#                 form_relation = RelationshipForm(request.form)
#                 if form_relation.validate_on_submit():
#                     db.session.add(RelationShip(**{k: v for k, v in form_relation.data.items() if
#                                                    k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
#                     db.session.commit()
#                     result = db.session.query(RelationShip).filter_by(cand_id=cand_id).all()
#                     decerial = relation_schema.dump(result, many=True)
#                     return jsonify(data=decerial+[{'flag': 'relation'}])
#             case _:
#                 flash(Markup(f"Ошибка добавления записи. Неизвестный флаг {flag}"), 'warning')


# @bp.route('/send_resume/<int:cand_id>', methods=['GET'])  # отправка анкеты на проверку
# def send_resume(cand_id):
#     resum = db.session.query(Candidate).filter_by(id=cand_id).first()
#     decerial = resume_schema.dumps(resum, many=True)
#     if resum.status == Status.NEWFAG.value or resum.status == Status.UPDATE.value:
#         decer = decerial_resume.decer_res(cand_id, officer=current_user.username)  # десериализация анкетных данных
#         response = requests.post(url=URL_CHECK, json=decer, timeout=5)
#         response.raise_for_status()
#         decerial = resume_schema.dumps(resum, many=True)
#         if response.status_code == 200:  # проверка статуса отправки
#             resum.status = Status.ROBOT.value  # устанавливаем статус Робот
#             db.session.commit()
#             resum = db.session.query(Candidate).filter_by(id=cand_id).first()
#             decerial = resume_schema.dumps(resum, many=True)
#             flash(Markup("Анкета успешно отправлена"), 'success')
#             return jsonify(data=decerial+[{'flag': 'resume'}])
#         else:
#             flash(Markup("Отправка не удалась. Попробуйте позднее"), 'warning')
#             return jsonify(data=decerial+[{'flag': 'resume'}])
#     else:
#         flash(Markup("Анкета не может быть отправлена. Проверка уже начата"), 'warning')
#         return jsonify(data=decerial+[{'flag': 'resume'}])


# @bp.route('/check/<int:cand_id>', methods=['GET', 'POST'])  # добавить проверку
# @bp.route('/check/<int:cand_id>/<int:check_id>', methods=['GET', 'POST'])  # редактировать проверку
# #@login_required  # форма проверки кандидата
# def check(cand_id, check_id=0):
#     check_form = CheckForm()
#     candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
#     path = os.path.join(BASE_PATH, candidate.fullname[0], f"{str(candidate.id)}-{candidate.fullname}",
#                         TODAY.strftime("%Y-%m-%d"))
#     result = db.session.query(Check).filter_by(
#         id=check_id).first()  # запрашиваем данные проверки, если есть
#     if request.method == 'GET':
#         if check_id:
#             if candidate.status in [Status.SAVE.value, Status.REPLY.value]:
#                 check_form = CheckForm(request.form, obj=result)  # загружаем  предварительные (старые данные)
#             else:
#                 flash(Markup("Проверку с текущим статусом нельзя отредактировать"), 'warning')
#                 return redirect(url_for('route.index')), jsonify(data={"status": "error"})
#         else:
#             if candidate.status in [Status.NEWFAG.value, Status.UPDATE.value]:
#                 pass
#                 # os.makedirs(path)  #  создаем папку для материалов проверки
#                 # os.startfile(path)  # открываем папку с проверкой
#             else:
#                 flash(Markup("Анкета взята в работу и еще не закончена"), 'warning')
#                 return redirect(url_for('route.index')), jsonify(
#                     data={"status": "error"})  # проверка на одновременную работу с анкетой
#         candidate.status = Status.MANUAL.value  # меняем статус анкеты
#         db.session.commit()
#     if check_form.validate_on_submit() and request.method == 'POST':
#         check_form = CheckForm(request.form)
#         check_dict = {k: v for k, v in check_form.data.items() if k not in ['submit', 'csrf_token']} | \
#                      {'officer': current_user.username}
#         if check_id:  # если редактируется проверка то перезаписываем данные
#             for k, v in check_dict.items():
#                 setattr(result, k, v)
#                 db.session.commit()
#         else:  # если новая проверка, то добавляем его в базу даннных
#             check_dict.update({'path': path, "cand_id": cand_id})
#             db.session.add(Check(**check_dict))
#             db.session.commit()
#         if check_dict['conclusion'] == Status.SAVE.value:
#             candidate.status = Status.SAVE.value  # меняем статус анкеты сохранен
#             db.session.commit()
#             flash(Markup("Проверка успешно сохранена"), 'success')
#         elif check_dict['conclusion'] == Status.CANCEL.value:
#             candidate.status = Status.CANCEL.value
#             db.session.commit()
#             flash(Markup("Проверка отменена"), 'info')
#         else:
#             if check_dict['pfo']:  # если поставлена отметка ПФО меняем статус
#                 candidate.status = Status.POLIGRAF.value
#                 db.session.commit()
#                 flash(Markup("Проверка завершена. Назначено проведение ПФО"), 'primary')
#             else:
#                 candidate.status = Status.RESULT.value
#                 db.session.commit()
#                 flash(Markup("Проверка завершена"), 'success')
#         # checks = db.session.query(Check).filter_by(cand_id=cand_id).first()
#         # resp_checks = check_schema.dumps(checks, many=True)
#         return redirect(url_for('route.index'))
#     return render_template('check.html', form=check_form, title="Проверка кандидата")


# @bp.route('/delete/<int:cand_id>/<int:check_id>', methods=['GET', 'POST'])  # редактировать проверку
# #@login_required  # форма проверки кандидата
# def delete(cand_id, check_id):
#     candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
#     candidate.status = Status.MANUAL.value  # меняем статус анкеты сохранен
#     db.session.commit()
#     Check.query.filter_by(id=check_id).delete()
#     db.session.commit()
#     checks = db.session.query(Check).filter_by(check_id=cand_id)
#     decerial = check_schema.dumps(checks, many=True)
#     flash(Markup("Проверка успешно удалена"), 'success')
#     return jsonify(data=decerial+[{'flag': 'check'}])


# @bp.route('/registr/<int:cand_id>/<int:check_id>', methods=('GET', 'POST'))  # отправка решения по кандидату
# #@login_required
# def registry(cand_id, check_id):
#     form_registry = RegistryForm(request.form)  # загружаем форму согласования
#     if form_registry.validate_on_submit() and request.method == 'POST':
#         reg = {k: v for k, v in form_registry.data.items() if k not in ['submit', 'csrf_token']} | \
#               {'check_id': check_id, 'supervisor': current_user.username, 'deadline': TODAY}
#         db.session.add(Registry(**reg))  # получаем данные из формы и записываем в базу данных
#         db.session.commit()
#         candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
#         registr = db.session.query(Registry).filter_by(cand=cand_id).all()
#         decerial = registry_schema.dumps(registr, many=True)
#         response = requests.post(url=URL_CHECK, json=json.dumps(
#             {
#                 "id": candidate.request_id,
#                 "comments": reg['comments'],
#                 "decision": reg['decision'],
#                 "deadline": TODAY,
#                 "supervisor": reg['supervisor']
#             },
#             default=str), timeout=5)
#         response.raise_for_status()
#         if response.status_code == 200:  # проверка статуса отправки
#             if reg['decision'] == Status.CANCEL.value:
#                 candidate.status = Status.CANCEL.value  # меняем статус в таблице на "Отмена"
#                 db.session.commit()
#             else:
#                 candidate.status = Status.FINISH.value  # меняем статус в таблице на "Решение "
#                 db.session.commit()
#             flash(Markup("Решение успешно отправлено"), 'success')
#         else:
#             flash(Markup("Отправка анкеты не удалась попробуйте еще раз позднее"), 'warning')
#         return jsonify(data=decerial+[{'flag': 'resume'}])


# @bp.route('/info', methods=('GET', 'POST'))  # create statistic info
# #@login_required
# def info():
#     statinfo = InfoForm()
#     candidates = db.session.query(Registry.decision, func.count(Registry.id)). \
#         group_by(Registry.decision).filter(extract('year', Registry.deadline) == TODAY.year).all()
#     poligraf = db.session.query(Poligraf.theme, func.count(Poligraf.id)). \
#         group_by(Poligraf.theme).filter(extract('year', Poligraf.deadline) == TODAY.year).all()
#     if request.method == 'POST':
#         statinfo = InfoForm(request.form)
#         candidates = db.session.query(Registry.decision, func.count(Registry.id)). \
#             group_by(Registry.decision).filter(Registry.deadline.between(statinfo.start.data, statinfo.end.data)).all()
#         poligraf = db.session.query(Poligraf.theme, func.count(Poligraf.id)). \
#             group_by(Poligraf.theme).filter(Poligraf.deadline.between(statinfo.start.data, statinfo.end.data)).all()
#         return render_template('info.html', form=statinfo, candidates=candidates, poligraf=poligraf,
#                                title=f'Cтатистика за период c {statinfo.start.data.strftime("%d.%m.%Y")} по '
#                                      f'{statinfo.end.data.strftime("%d.%m.%Y")}')
#     return render_template('info.html', form=statinfo, candidates=candidates, poligraf=poligraf,
#                            title=f'Статистика за {TODAY.year} год')
