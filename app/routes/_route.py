import os
import json

import requests
from sqlalchemy import func, extract
from flask import Markup, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required

from . import bp
from ..utils.extensions import BASE_PATH, ExcelFile, resume_data, URL_CHECK
from ..models.model import User, db, Candidate, Staff, Document, Address, Contact, Workplace, RelationShip, \
    Check, Registry, Poligraf, Investigation, Inquiry, decerial_resume
from ..forms.form import ResumeForm, StaffForm, DocumentForm, AddressForm, \
    ContactForm, WorkplaceForm, RelationshipForm, RegistryForm, PoligrafForm, InvestigationForm, InquiryForm, \
    FileForm, CheckForm, SearchForm, InfoForm, TODAY, Status


@bp.route('/', methods=['GET', 'POST'])  # главная страница
@login_required
def index():
    form = SearchForm()  # загрузка формы для поиска
    page = request.args.get('page', 1, type=int)  # разбиваем на страницы
    count = db.session.query(func.count(Candidate.status)).filter_by(status=Status.NEWFAG.value).scalar()
    if count:  # отображаем количество новых анкет
        flash(Markup(f'Новых анкет: {count}'), 'info')
    results = db.session.query(Candidate.id, Candidate.region, Candidate.fullname, Candidate.birthday,
                               Candidate.status, Candidate.deadline).order_by(Candidate.id.desc()). \
        paginate(page=page, per_page=16)
    if form.validate_on_submit() and request.method == 'POST':  # получаем данные из формы
        form = SearchForm(request.form)
        form_dict = {k: v for k, v in form.data.items() if k not in ['submit', 'csrf_token']}
        results = db.session.query(Candidate).filter(Candidate.region.ilike(f'%{form_dict["region"]}%'
                                                                            if form_dict["region"] != '' else '%'),
                                                     Candidate.fullname.ilike(f'%{form_dict["fullname"]}%'
                                                                              if form_dict["fullname"] != '' else '%'),
                                                     Candidate.birthday.ilike(f'%{form_dict["birthday"]}%'
                                                                              if form_dict["birthday"] is not None
                                                                              else '%')). \
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
            paginate(page=page, per_page=16)
        data = [{'id': result.id, 'region': result.region, 'fullname': result.fullname,
                 'birthday': result.birthday.strftime("%d.%m.%Y"), 'status': result.status,
                 'deadline': result.deadline.strftime("%d.%m.%Y")} for result in results]
        return jsonify(data=data)
    data = [{'id': result.id, 'region': result.region, 'fullname': result.fullname,
             'birthday': result.birthday.strftime("%d.%m.%Y"), 'status': result.status,
             'deadline': result.deadline.strftime("%d.%m.%Y")} for result in results]
    return render_template('index.html', data=data, form=form)


@bp.route('/search', methods=['GET', 'POST'])  # главная страница
@login_required
def search():
    form = SearchForm()  # загрузка формы для поиска
    page = request.args.get('page', 1, type=int)  # разбиваем на страницы
    if request.args.get('search', None):  # поиск через форму на панели навигации
        search_by = request.form.get('search')
        results = db.session.query(Candidate).filter(Candidate.fullname.ilike(f'%{search_by}%')). \
            paginate(page=page, per_page=16)
        return render_template('index.html', form=form, results=results)


@bp.route('/officer', methods=['GET', 'POST'])  # страница пользователя
@login_required
def officer():
    results = db.session.query(Candidate).filter(Candidate.status != Status.FINISH.value,
                                                 Candidate.status != Status.CANCEL.value).join(Check, isouter=True). \
        filter_by(officer=current_user.username).order_by(Candidate.id.asc()).all()
    username = db.session.query(User.fullname).filter_by(username=current_user.username).first()
    count = db.session.query(func.count(Candidate.status)).filter(Candidate.status == Status.SAVE.value,
                                                                  Candidate.status == Status.REPLY.value). \
        join(Check, isouter=True).filter_by(officer=current_user.username).scalar()
    if count:
        flash(Markup(f'Незавершенных анкет: {count}'), 'info')  # отображаем количество новых анкет
    return render_template('index.html', results=results, user=username)


@bp.route('/resume', methods=['GET', 'POST'])  # добавляем новую анкету
@login_required
def resume():
    file = FileForm()  # форма для добавления файла
    candidate = ResumeForm()  # форма для добавления новой анкеты
    title = "Новая анкета кандидата"
    if candidate.validate_on_submit() and request.method == 'POST':  # получаем данные из формы
        candidate = ResumeForm(request.form)
        resume_dict = {k: v for k, v in candidate.data.items() if k not in ['submit', 'csrf_token']}
        result = db.session.query(Candidate).filter(Candidate.fullname == resume_dict['fullname'],
                                                    Candidate.birthday == resume_dict['birthday']).first()
        if result:  # проверка существования такой же анкеты, если есть анкета с таким именем, обновляем данные
            resume_dict.update({'status': Status.UPDATE.value})
            for k, v in resume_dict.items():
                setattr(result, k, v)
                db.session.commit()
            cand_id = result.id
            flash(Markup('Запись уже существует. Данные обновлены'), 'success')
        else:  # если нет таких анкет, добавляем новую запись
            resume_dict.update({'status': Status.NEWFAG.value, 'deadline': TODAY})
            value = Candidate(**resume_dict)
            db.session.add(value)
            db.session.flush()
            cand_id = value.id
            db.session.commit()
            flash(Markup('Создана новая запись'), 'success')
        return redirect(url_for('route.profile', cand_id=cand_id))
    return render_template('resume.html', file=file, form=candidate, title=title)


@bp.route('/upload', methods=['GET', 'POST'])  # загрузка анкеты из файла Excel
@login_required
def upload():
    file = request.files['file']  # получаем файл
    if request.method == 'POST':
        excel = ExcelFile(file)  # создаем экземпляр класса ExcelFile для разборки файла,
        result = db.session.query(Candidate).filter(Candidate.fullname.ilike(excel.resume['fullname']),
                                                    Candidate.birthday == (excel.resume['birthday'])).first()
        if result:  # проверяем, есть анкета с таким именем; если есть, то обновляем основные данные
            for k, v in excel.resume.items() | {'status': Status.UPDATE.value, 'deadline': TODAY}:
                setattr(result, k, v)
                db.session.commit()
            resume_data(result.id, excel.passport, excel.addresses, excel.contacts,
                        excel.workplaces, excel.staff)  # добавляем новые данные в базу данных
            flash(Markup('Запись уже существует. Данные обновлены'), 'info')
        else:  # если нет таких анкет, добавляем новую запись
            result = Candidate(**excel.resume | {'status': Status.NEWFAG.value, 'deadline': TODAY})
            db.session.add(result)
            db.session.flush()  # фиксируем id для последующей записи
            resume_data(result.id, excel.passport, excel.addresses, excel.contacts,
                        excel.workplaces, excel.staff)  # добавляем новые данные в базу данных
            db.session.commit()  # окончательно сохраняем в базу данных основные данные
            flash(Markup('Создана новая запись'), 'info')
        return redirect(url_for('route.profile', cand_id=result.id))


@bp.route('/actions/<action>/<int:cand_id>', methods=['GET', 'POST'])  # редактируем/обновляем анкету
@login_required
def actions(action, cand_id):
    result = db.session.query(Candidate).filter_by(id=cand_id).first()
    candidate = ResumeForm(request.form)
    if action == 'update':
        if result.status not in [Status.RESULT.value, Status.POLIGRAF.value]:
            result.status = Status.UPDATE.value
            result.deadline = TODAY
            db.session.commit()
            flash(Markup('Статус обновлен'), 'info')
            return redirect(url_for('route.profile', cand_id=cand_id))
        else:
            flash(Markup('Анкету с текущим статусом обновить нельзя'), 'warning')
            return redirect(url_for('route.index'))
    if candidate.validate_on_submit() and request.method == 'POST' and action == 'edit':  # получаем данные из формы
        resume_dict = {k: v for k, v in candidate.data.items() if k not in ['submit', 'csrf_token']}
        for k, v in resume_dict.items():
            setattr(result, k, v)
            db.session.commit()
            flash(Markup('Данные обновлены'), 'info')
            return redirect(url_for('route.profile', cand_id=cand_id))


@bp.route('/profile/<int:cand_id>', methods=['GET', 'POST'])  # загрузка профиля кандидата
@login_required
def profile(cand_id):  # полный профиль кандидата/сотрудника
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()  # получаем  все данные кандидата из БД
    documents = db.session.query(Document).filter_by(cand_id=cand_id).order_by(Document.cand_id.asc()).all()
    address = db.session.query(Address).filter_by(cand_id=cand_id).order_by(Address.id.asc()).all()
    contacts = db.session.query(Contact).filter_by(cand_id=cand_id).order_by(Contact.id.asc()).all()
    workplaces = db.session.query(Workplace).filter_by(cand_id=cand_id).order_by(Workplace.id.asc()).all()
    relations = db.session.query(RelationShip).filter_by(cand_id=cand_id).order_by(RelationShip.id.asc()).all()
    staffs = db.session.query(Staff).filter_by(cand_id=cand_id).order_by(Staff.id.asc()).all()
    checks = db.session.query(Check).filter_by(cand_id=cand_id).order_by(Check.id.asc()).all()
    registries = [db.session.query(Registry).filter(Registry.check_id == i.id).first() for i in checks]
    pfos = db.session.query(Poligraf).filter_by(cand_id=cand_id).order_by(Poligraf.id.asc()).all()
    invs = db.session.query(Investigation).filter_by(cand_id=cand_id).order_by(Investigation.id.asc()).all()
    inquiries = db.session.query(Inquiry).filter_by(cand_id=cand_id).order_by(Inquiry.id.asc()).all()
    form = ResumeForm(obj=candidate)  # загрузка формы редактирования анкеты
    form_investigation = InvestigationForm()  # загрузка других форм...
    form_inquiry = InquiryForm()
    form_poligraf = PoligrafForm()
    form_staff = StaffForm()
    form_document = DocumentForm()
    form_address = AddressForm()
    form_work = WorkplaceForm()
    form_relation = RelationshipForm()
    form_contact = ContactForm()
    form_registry = RegistryForm()
    return render_template('profile.html', candidate=candidate, documents=documents, addresses=address,
                           relations=relations, staffs=staffs, workplaces=workplaces, contacts=contacts,
                           checks=checks, registr=registries, inquiries=inquiries, pfos=pfos, invs=invs,
                           form=form, form_investigation=form_investigation, form_inquiry=form_inquiry,
                           form_poligraf=form_poligraf, form_staff=form_staff, form_document=form_document,
                           form_address=form_address, form_work=form_work, form_relation=form_relation,
                           form_contact=form_contact, form_registry=form_registry,
                           status={i.name: i.value for i in Status})


@bp.route('/add/<flag>/<int:cand_id>', methods=['GET', 'POST'])
@login_required
def add(flag, cand_id):  # добавление данных через модальные окна
    if request.method == 'POST':
        match flag:
            case "form_investigation":
                form_investigation = InvestigationForm(request.form)  # получаем данные из формы
                if form_investigation.validate_on_submit():
                    db.session.add(Investigation(**{k: v for k, v in form_investigation.data.items() if
                                                    k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
                    db.session.commit()  # передаем в БД
                    flash(Markup(f"Запись успешно добавлена"), 'success')
                    return redirect(url_for('route.profile', cand_id=cand_id))
            case "form_inquiry":
                form_inquiry = InquiryForm(request.form)
                if form_inquiry.validate_on_submit():
                    db.session.add(Inquiry(**{k: v for k, v in form_inquiry.data.items() if
                                              k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
                    db.session.commit()
                    flash(Markup(f"Запись успешно добавлена"), 'success')
                    return redirect(url_for('route.profile', cand_id=cand_id))
            case "form_poligraf":
                form_poligraf = PoligrafForm(request.form)
                if form_poligraf.validate_on_submit():
                    db.session.add(Poligraf(**{k: v for k, v in form_poligraf.data.items() if
                                               k not in ['submit', 'csrf_token']} | {'cand_id': cand_id} |
                                              {'officer': current_user.username}))
                    db.session.commit()
                    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
                    if candidate.status == Status.POLIGRAF.value:  # проверяем статус, если указано ПФО, завершаем
                        candidate.status = Status.RESULT.value
                        db.session.commit()
                    flash(Markup(f"Запись успешно добавлена"), 'success')
                    return redirect(url_for('route.profile', cand_id=cand_id))
            case "form_staff":
                form_staff = StaffForm(request.form)
                if form_staff.validate_on_submit():
                    print(form_staff)
                    db.session.add(Staff(**{k: v for k, v in form_staff.data.items() if
                                            k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
                    db.session.commit()
                    return jsonify({"status ": "success "})
                    # return redirect(url_for('route.profile', cand_id=cand_id))
            case "form_document":
                form_document = DocumentForm(request.form)
                if form_document.validate_on_submit():
                    db.session.add(Document(**{k: v for k, v in form_document.data.items() if
                                               k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
                    db.session.commit()
                    return redirect(url_for('route.profile', cand_id=cand_id))
            case "form_address":
                form_address = AddressForm(request.form)
                if form_address.validate_on_submit():
                    db.session.add(Address(**{k: v for k, v in form_address.data.items() if
                                              k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
                    db.session.commit()
                    return redirect(url_for('route.profile', cand_id=cand_id))
            case "form_contact":
                form_contact = ContactForm(request.form)
                if form_contact.validate_on_submit():
                    db.session.add(Contact(**{k: v for k, v in form_contact.data.items() if
                                              k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
                    db.session.commit()
                    return redirect(url_for('route.profile', cand_id=cand_id))
            case "form_work":
                form_work = WorkplaceForm(request.form)
                if form_work.validate_on_submit():
                    db.session.add(Workplace(**{k: v for k, v in form_work.data.items() if
                                                k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
                    db.session.commit()
                    return redirect(url_for('route.profile', cand_id=cand_id))
            case "form_relation":
                form_relation = RelationshipForm(request.form)
                if form_relation.validate_on_submit():
                    db.session.add(RelationShip(**{k: v for k, v in form_relation.data.items() if
                                                   k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
                    db.session.commit()
                    return redirect(url_for('route.profile', cand_id=cand_id))
            case _:
                flash(Markup(f"Ошибка добавления записи. Неизвестный флаг {flag}"), 'warning')


@bp.route('/send_resume/<int:cand_id>', methods=['GET'])  # отправка анкеты на проверку
def send_resume(cand_id):
    resum = db.session.query(Candidate).filter_by(id=cand_id).first()
    if resum.status == Status.NEWFAG.value or resum.status == Status.UPDATE.value:
        decerial = decerial_resume.decer_res(cand_id, officer=current_user.username)  # десериализация анкетных данных
        response = requests.post(url=URL_CHECK, json=decerial)
        response.raise_for_status()
        if response.status_code == 200:  # проверка статуса отправки
            resum.status = Status.ROBOT.value  # устанавливаем статус Робот
            db.session.commit()
            flash(Markup("Анкета успешно отправлена"), 'success')
            return redirect(url_for('route.index'))
        else:
            flash(Markup("Отправка не удалась. Попробуйте позднее"), 'warning')
        return redirect(url_for('route.profile', cand_id=cand_id))
    else:
        flash(Markup("Анкета не может быть отправлена. Проверка уже начата"), 'warning')
        return redirect(url_for('route.index'))


@bp.route('/check/<int:cand_id>', methods=['GET', 'POST'])  # добавить проверку
@bp.route('/check/<int:cand_id>/<int:check_id>', methods=['GET', 'POST'])  # редактировать проверку
@login_required  # форма проверки кандидата
def check(cand_id, check_id=0):
    check_form = CheckForm()
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    path = os.path.join(BASE_PATH, candidate.fullname[0], f"{str(candidate.id)}-{candidate.fullname}",
                        TODAY.strftime("%Y-%m-%d"))
    result = db.session.query(Check).filter_by(
        id=check_id).first()  # запрашиваем данные проверки, если есть
    if request.method == 'GET':
        if check_id:
            if candidate.status in [Status.SAVE.value, Status.REPLY.value]:
                check_form = CheckForm(request.form, obj=result)  # загружаем  предварительные (старые данные)
            else:
                flash(Markup("Проверку с текущим статусом нельзя отредактировать"), 'warning')
                return redirect(url_for('route.index'))
        else:
            if candidate.status in [Status.NEWFAG.value, Status.UPDATE.value]:
                pass
                # os.makedirs(path)  #  создаем папку для материалов проверки
                # os.startfile(path)  # открываем папку с проверкой
            else:
                flash(Markup("Анкета взята в работу и еще не закончена"), 'warning')
                return redirect(url_for('route.index'))  # проверка на одновременную работу с анкетой
        candidate.status = Status.MANUAL.value  # меняем статус анкеты
        db.session.commit()
    if check_form.validate_on_submit() and request.method == 'POST':
        check_form = CheckForm(request.form)
        check_dict = {k: v for k, v in check_form.data.items() if k not in ['submit', 'csrf_token']} | \
                     {'officer': current_user.username}
        if check_id:  # если редактируется проверка то перезаписываем данные
            for k, v in check_dict.items():
                setattr(result, k, v)
                db.session.commit()
        else:  # если новая проверка, то добавляем его в базу даннных
            check_dict.update({'path': path, "cand_id": cand_id})
            db.session.add(Check(**check_dict))
            db.session.commit()
        if check_dict['conclusion'] == Status.SAVE.value:
            candidate.status = Status.SAVE.value  # меняем статус анкеты сохранен
            db.session.commit()
            flash(Markup("Проверка успешно сохранена"), 'success')
        elif check_dict['conclusion'] == Status.CANCEL.value:
            candidate.status = Status.CANCEL.value
            db.session.commit()
            flash(Markup("Проверка отменена"), 'info')
        else:
            if check_dict['pfo']:  # если поставлена отметка ПФО меняем статус
                candidate.status = Status.POLIGRAF.value
                db.session.commit()
                flash(Markup("Проверка завершена. Назначено проведение ПФО"), 'primary')
            else:
                candidate.status = Status.RESULT.value
                db.session.commit()
                flash(Markup("Проверка завершена"), 'success')
        return redirect(url_for('route.index'))
    return render_template('check.html', form=check_form, title="Проверка кандидата")


@bp.route('/delete/<int:cand_id>/<int:check_id>', methods=['GET', 'POST'])  # редактировать проверку
@login_required  # форма проверки кандидата
def delete(cand_id, check_id):
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    candidate.status = Status.MANUAL.value  # меняем статус анкеты сохранен
    db.session.commit()
    Check.query.filter_by(id=check_id).delete()
    db.session.commit()
    flash(Markup("Проверка успешно удалена"), 'success')
    return render_template('profile.html', cand_id=cand_id)


@bp.route('/registr/<int:cand_id>/<int:check_id>', methods=('GET', 'POST'))  # отправка решения по кандидату
@login_required
def registry(cand_id, check_id):
    form_registry = RegistryForm(request.form)  # загружаем форму согласования
    if form_registry.validate_on_submit() and request.method == 'POST':
        reg = {k: v for k, v in form_registry.data.items() if k not in ['submit', 'csrf_token']} | \
              {'check_id': check_id, 'supervisor': current_user.username, 'deadline': TODAY}
        db.session.add(Registry(**reg))  # получаем данные из формы и записываем в базу данных
        db.session.commit()
        candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
        response = requests.post(url=URL_CHECK, json=json.dumps(
            {
                "id": candidate.request_id,
                "comments": reg['comments'],
                "decision": reg['decision'],
                "deadline": TODAY,
                "supervisor": reg['supervisor']
            },
            default=str))
        response.raise_for_status()
        if response.status_code == 200:  # проверка статуса отправки
            if reg['decision'] == Status.CANCEL.value:
                candidate.status = Status.CANCEL.value  # меняем статус в таблице на "Отмена"
                db.session.commit()
            else:
                candidate.status = Status.FINISH.value  # меняем статус в таблице на "Решение "
                db.session.commit()
            flash(Markup("Решение успешно отправлено"), 'success')
            return redirect(url_for('route.index'))
        else:
            flash(Markup("Отправка анкеты не удалась попробуйте еще раз позднее"), 'warning')
        return redirect(url_for('route.index'))


@bp.route('/info', methods=('GET', 'POST'))  # create statistic info
@login_required
def info():
    statinfo = InfoForm()
    candidates = db.session.query(Registry.decision, func.count(Registry.id)). \
        group_by(Registry.decision).filter(extract('year', Registry.deadline) == TODAY.year).all()
    poligraf = db.session.query(Poligraf.theme, func.count(Poligraf.id)). \
        group_by(Poligraf.theme).filter(extract('year', Poligraf.deadline) == TODAY.year).all()
    if request.method == 'POST':
        statinfo = InfoForm(request.form)
        candidates = db.session.query(Registry.decision, func.count(Registry.id)). \
            group_by(Registry.decision).filter(Registry.deadline.between(statinfo.start.data, statinfo.end.data)).all()
        poligraf = db.session.query(Poligraf.theme, func.count(Poligraf.id)). \
            group_by(Poligraf.theme).filter(Poligraf.deadline.between(statinfo.start.data, statinfo.end.data)).all()
        return render_template('info.html', form=statinfo, candidates=candidates, poligraf=poligraf,
                               title=f'Cтатистика за период c {statinfo.start.data.strftime("%d.%m.%Y")} по '
                                     f'{statinfo.end.data.strftime("%d.%m.%Y")}')
    return render_template('info.html', form=statinfo, candidates=candidates, poligraf=poligraf,
                           title=f'Статистика за {TODAY.year} год')
