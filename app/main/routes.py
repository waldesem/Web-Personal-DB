import os
import json

import requests
from sqlalchemy import func, extract
from flask import Markup, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from . import bpr
from ..utils.extensions import BASE_PATH, ExcelFile, resume_data, URL_CHECK
from ..models.model import db, User, Candidate, Staff, Document, Address, Contact, Workplace, RelationShip, \
    Check, Registry, Poligraf, Investigation, Inquiry, decerial_resume
from ..forms.form import STATUS, LoginForm, ResumeForm, StaffForm, DocumentForm, AddressForm, \
    ContactForm, WorkplaceForm, RelationshipForm, RegistryForm, PoligrafForm, InvestigationForm, InquiryForm, \
    InfoForm, FileForm, CheckForm, TODAY


@bpr.route("/login", methods=["POST", "GET"])  # вход пользователя в систему
def login():  # пароль и логин из таблицы Users прописываются через интерфейс БД
    user_form = LoginForm()
    if current_user.is_authenticated:  # если пользователь уже авторизован, возвращаемся на главную страницу
        return redirect(url_for('route.index'))
    if user_form.validate_on_submit() and request.method == "POST":  # если пользователь не авторизован
        user_form = LoginForm(request.form)  # получаем данные из формы
        username = user_form.username.data
        password = user_form.password.data
        rmb = user_form.remember.data
        user = db.session.query(User).filter_by(username=username).first()  # получаем данные из таблицы Users
        if db.session.query(User).filter_by(username=username, password=password).first():
            login_user(user, remember=rmb)  # если пользователь успешно авторизован возвращаемся на главную страницу
            return redirect(url_for('route.index'))
        else:  # если авторизация не удалась выводим сообщение об ошибке
            flash("Неверная пара логин/пароль", "warning")
    return render_template("login.html", form=user_form, title="Войти в систему")


@bpr.route('/logout')
# @login_required
def logout():  # выход пользователя из системы
    logout_user()
    return redirect(url_for('route.login'))


@bpr.route('/', methods=['GET', 'POST'])
# @login_required
def index():  # загрузка стартовой страницы
    page = request.args.get('page', 1, type=int)  # разбиваем на страницы по указанному параметру
    results = db.session.query(Candidate).order_by(Candidate.status.asc(),
                                                   Candidate.id.desc()).paginate(page=page, per_page=12)
    count = db.session.query(Candidate.status, func.count(Candidate.status)).filter_by(status=STATUS['new']).first()[1]
    flash(Markup(f'Новых анкет: {count}'), 'secondary')  # отображаем количество новых анкет
    if request.method == 'POST':  # загрузка страницы результатов поиска
        search_by = request.form.get('search')
        results = db.session.query(Candidate).filter(Candidate.fullname.ilike(f'%{search_by}%')). \
            paginate(page=page, per_page=16)  # получаем результаты поиска по фильтру фамилии
        return render_template('index.html', results=results)
    return render_template('index.html', results=results)


@bpr.route('/officer/', methods=['GET', 'POST'])
# @login_required
def officer():  # загрузка страницы пользователя, показываем незавершенных кандидатов в работе у сотрудника
    page = request.args.get('page', 1, type=int)
    results = db.session.query(Candidate).filter(Candidate.status != STATUS['finish'],
                                                 Candidate.status != STATUS['cancel']). \
        join(Check, isouter=True).filter_by(officer=current_user.username).order_by(Candidate.status.asc()). \
        paginate(page=page, per_page=12)
    return render_template('index.html', results=results, user=current_user.username)


@bpr.route('/resume/<int:cand_id>', methods=['GET', 'POST'])  # добавляем новую анкету или редактируем
# @login_required
def resume(cand_id):
    file = FileForm()  # форма для добавления файла
    candidate = ResumeForm()  # форма для добавления новой анкеты
    title = "Новая анкета кандидата"
    if cand_id:  # если анкета редактируется, то загружаем старые данные в форму
        result = db.session.query(Candidate).filter_by(id=cand_id).first()  # запрашиваем/проверяем наличие анкеты
        candidate = ResumeForm(request.form, obj=result)
        title = "Редактирование анкеты"
    if candidate.validate_on_submit() and request.method == 'POST':  # получаем данные из формы
        candidate = ResumeForm(request.form)  # форма для добавления новой анкеты
        resume_dict = {k: v for k, v in candidate.data.items() if k not in ['submit', 'csrf_token']}
        result = db.session.query(Candidate).filter(Candidate.fullname == resume_dict['fullname'],
                                                    Candidate.birthday == resume_dict['birthday']).first()
        if result:  # проверка существования такой же анкеты, если есть анкета с таким именем, обновляем данные
            for k, v in resume_dict.items() | {'status': STATUS['update']}:
                setattr(result, k, v)
                db.session.commit()
            flash(Markup('Такая запись уже существует. Данные обновлены'), 'info')
        else:  # если нет таких анкет, добавляем новую запись
            value = Candidate(**resume_dict | {'status': STATUS['new'], 'deadline': TODAY})
            db.session.add(value)
            db.session.flush()
            cand_id = value.id
            db.session.commit()
            flash(Markup('Создана новая запись'), 'success')
        return redirect(url_for('route.profile', cand_id=cand_id))
    return render_template('resume.html', file=file, form=candidate, title=title)


@bpr.route('/profile/<int:cand_id>', methods=['GET', 'POST'])  # загрузка профиля кандидата
# @login_required
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
                           form_contact=form_contact, form_registry=form_registry, status=STATUS)


@bpr.route('/add/<flag>/<int:cand_id>', methods=['GET', 'POST'])
# @login_required
def add(flag, cand_id):
    match flag:
        case "investigation":
            if request.method == 'POST':
                form_investigation = InvestigationForm(request.form)  # получаем данные из формы
                db.session.add(Investigation(**{k: v for k, v in form_investigation.data.items() if
                                                k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
                db.session.commit()  # передаем в БД
                flash(Markup(f"Запись успешно добавлена"), 'success')
                return redirect(url_for('route.profile', cand_id=cand_id))
        case "inquiry":
            if request.method == 'POST':
                form_inquiry = InquiryForm(request.form)
                db.session.add(Inquiry(**{k: v for k, v in form_inquiry.data.items() if
                                          k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
                db.session.commit()
                flash(Markup(f"Запись успешно добавлена"), 'success')
                return redirect(url_for('route.profile', cand_id=cand_id))
        case "poligraf":
            if request.method == 'POST':
                form_poligraf = PoligrafForm(request.form)
                db.session.add(Poligraf(**{k: v for k, v in form_poligraf.data.items() if
                                           k not in ['submit', 'csrf_token']} | {'cand_id': cand_id} |
                                          {'officer': current_user.username}))
                db.session.commit()
                candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
                if candidate.status == STATUS['pfo']:  # проверяем статус анкеты, если указано ПФО, то завершаем
                    candidate.status = STATUS['result']
                    db.session.commit()
                flash(Markup(f"Запись успешно добавлена"), 'success')
                return redirect(url_for('route.profile', cand_id=cand_id))
        case "staff":
            if request.method == 'POST':
                form_staff = StaffForm(request.form)
                db.session.add(Staff(**{k: v for k, v in form_staff.data.items() if
                                        k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
                db.session.commit()
                return redirect(url_for('route.profile', cand_id=cand_id))
        case "document":
            if request.method == 'POST':
                form_document = DocumentForm(request.form)
                db.session.add(Document(**{k: v for k, v in form_document.data.items() if
                                           k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
                db.session.commit()
                return redirect(url_for('route.profile', cand_id=cand_id))
        case "address":
            if request.method == 'POST':
                form_address = AddressForm(request.form)
                db.session.add(Address(**{k: v for k, v in form_address.data.items() if
                                          k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
                db.session.commit()
                return redirect(url_for('route.profile', cand_id=cand_id))
        case "contact":
            if request.method == 'POST':
                form_contact = ContactForm(request.form)
                db.session.add(Contact(**{k: v for k, v in form_contact.data.items() if
                                          k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
                db.session.commit()
                return redirect(url_for('route.profile', cand_id=cand_id))
        case "work":
            if request.method == 'POST':
                form_work = WorkplaceForm(request.form)
                db.session.add(Workplace(**{k: v for k, v in form_work.data.items() if
                                            k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
                db.session.commit()
                return redirect(url_for('route.profile', cand_id=cand_id))
        case "relation":
            if request.method == 'POST':
                print(flag)
                form_relation = RelationshipForm(request.form)
                db.session.add(RelationShip(**{k: v for k, v in form_relation.data.items() if
                                               k not in ['submit', 'csrf_token']} | {'cand_id': cand_id}))
                db.session.commit()
                return redirect(url_for('route.profile', cand_id=cand_id))
        case _:
            flash(Markup(f"При добавлении записи возникла ошибка {flag}"), 'warning')


@bpr.route('/upload', methods=['GET', 'POST'])  # загрузка анкеты из файла Excel
# @login_required
def upload():
    file = request.files['file']  # получаем файл
    if request.method == 'POST':
        excel = ExcelFile(file)  # создаем экземпляр класса ExcelFile для разборки файла,
        result = db.session.query(Candidate).filter(Candidate.fullname.ilike(excel.resume['fullname']),
                                                    Candidate.birthday == (excel.resume['birthday'])).first()
        if result:  # проверяем, есть анкета с таким именем; если есть, то обновляем основные данные
            for k, v in excel.resume.items() | {'status': STATUS['update'], 'deadline': TODAY}:
                setattr(result, k, v)
                db.session.commit()
            resume_data(result.id, excel.passport, excel.addresses, excel.contacts,
                        excel.workplaces, excel.staff)  # добавляем новые данные в базу данных
            flash(Markup('Такая запись уже существует. Данные обновлены'), 'info')
        else:  # если нет таких анкет, добавляем новую запись
            result = Candidate(**excel.resume | {'status': STATUS['new'], 'deadline': TODAY})
            db.session.add(result)
            db.session.flush()  # фиксируем id для последующей записи
            resume_data(result.id, excel.passport, excel.addresses, excel.contacts,
                        excel.workplaces, excel.staff)  # добавляем новые данные в базу данных
            db.session.commit()  # окончательно сохраняем в базу данных основные данные
            flash(Markup('Создана новая запись'), 'info')
        return redirect(url_for('route.profile', cand_id=result.id))


@bpr.route('/send_resume/<int:cand_id>', methods=['GET'])  # отправка анкеты на проверку
def send_resume(cand_id):
    resum = db.session.query(Candidate).filter_by(id=cand_id).first()
    if resum.status == STATUS['new']:
        decerial = decerial_resume.decer_res(cand_id, officer='current_user.username')
        url = URL_CHECK  # отправка анкеты на проверку
        response = requests.post(url=url, json=decerial)
        response.raise_for_status()
        if response.status_code == 200:   # проверка статуса отправки
            resum.status = STATUS['robot']  # устанавливаем статус Робот
            db.session.commit()
            flash(Markup("Анкета успешно отправлена"), 'success')
            return redirect(url_for('route.index'))
        else:
            flash(Markup("Отправка анкеты не удалась попробуйте еще раз позднее"), 'warning')
        return redirect(url_for('route.profile', cand_id=cand_id))
    else:
        # flash(Markup("Анкета ге может быть отправлена, т.к. проверка уже начата"), 'warning')
        return redirect(url_for('route.index'))


@bpr.route('/check/<int:cand_id>/<int:check_id>', methods=['GET', 'POST'])
# @login_required  # форма проверки кандидата
def check(cand_id, check_id):
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    result = db.session.query(Check).filter_by(id=check_id).first()  # запрашиваем данные проверки, если есть
    checks = CheckForm()
    if cand_id:
        checks = CheckForm(request.form, obj=result)  # загружаем  предварительные (старые данные)
    path = os.path.join(BASE_PATH, candidate.fullname[0], f"{str(candidate.id)}-{candidate.fullname}",
                        TODAY.strftime("%Y-%m-%d"))
    if request.method == 'GET':
        # if check_id is False:  # создаем  путь и папку к материалам проверки
        #   os.makedirs(path)  #  создаем папку для материалов проверки
        #   os.startfile(path)  # открываем папку с проверкой
        if check_id is False and candidate.status not in [STATUS['new'], STATUS['update'],
                                                          STATUS['finish'], STATUS['cancel']]:
            flash(Markup("Анкета взята в работу и еще не закончена"), 'warning')
            return redirect(url_for('route.index'))  # проверка на одновременную работу с анкетой
        candidate.status = STATUS['check']  # меняем статус анкеты
        db.session.commit()
    if checks.validate_on_submit() and request.method == 'POST':
        checks = CheckForm(request.form)
        check_dict = {k: v for k, v in checks.data.items() if k not in ['submit', 'csrf_token']} | \
                     {'officer': 'current_user.username', 'deadline': TODAY}
        if check_id:  # если редактируется проверка то перезаписываем данные
            for k, v in check_dict.items():
                setattr(result, k, v)
                db.session.commit()
        else:  # если новая проверка, то добавляем его в базу даннных
            check_dict.update({'path': path, "cand_id": cand_id})
            db.session.add(Check(**check_dict))
            db.session.commit()
        if check_dict['conclusion'] == 'Сохранить':
            flash(Markup("Проверка успешно сохранена"), 'success')
        elif check_dict['conclusion'] == 'Снят с проверки':
            candidate.status = STATUS['cancel']
            db.session.commit()
            flash(Markup("Проверка отменена"), 'info')
        else:
            if check_dict['pfo']:  # если поставлена отметка ПФО меняем статус
                candidate.status = STATUS['pfo']
                db.session.commit()
                flash(Markup("Проверка завершена. Назначено проведение ПФО"), 'primary')
            else:
                candidate.status = STATUS['result']
                db.session.commit()
                flash(Markup("Проверка завершена"), 'primary')
        return redirect(url_for('route.index'))
    return render_template('check.html', form=checks, title="Проверка кандидата")


@bpr.route('/registr/<int:cand_id>/<int:check_id>', methods=('GET', 'POST'))  # отправка решения по кандидату
# @login_required
def registry(cand_id, check_id):
    if request.method == 'POST':
        form_registry = RegistryForm(request.form)  # загружаем форму согласования
        reg = {k: v for k, v in form_registry.data.items() if k not in ['submit', 'csrf_token']} | \
              {'check_id': check_id, 'supervisor': 'current_user.username', 'deadline': TODAY}
        db.session.add(Registry(**reg))  # получаем данные из формы и записываем в базу данных
        db.session.commit()
        candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
        candidate.status = STATUS['finish']  # меняем статус в таблице на "Решение"
        db.session.commit()
        response = requests.post(url=URL_CHECK, json=json.dumps(
            {
                "id": candidate.request_id,
                "comments": reg['comments'],
                "decision": reg['decision'],
                "deadline": TODAY,
                "supervisor": reg['supervisor']
            }
        ))
        response.raise_for_status()
        if response.status_code == 200 or response.status_code == 201:  # проверка статуса отправки
            print(response.status_code)
            candidate.status = STATUS['finish']  # меняем статус в таблице на "Решение принято"
            db.session.commit()
            flash(Markup("Решение успешно отправлено"), 'success')
            return redirect(url_for('route.index'))
        else:
            flash(Markup("Отправка анкеты не удалась попробуйте еще раз позднее"), 'warning')
        return redirect(url_for('route.index'))


@bpr.route('/info', methods=('GET', 'POST'))  # create statistic info
# @login_required
def info():
    statinfo = InfoForm()
    results = db.session.query(Registry.decision, func.count(Registry.id)). \
        group_by(Registry.decision).filter(extract('year', Registry.deadline) == TODAY.year).all()
    pfo_count = db.session.query(Poligraf.theme, func.count(Poligraf.id)). \
        group_by(Poligraf.theme).filter(extract('year', Poligraf.deadline) == TODAY.year).all()
    if request.method == 'POST':
        statinfo = InfoForm(request.form)
        results = db.session.query(Registry.decision, func.count(Registry.id)). \
            group_by(Registry.decision).filter(Registry.deadline.between(statinfo.start.data, statinfo.end.data)).all()
        pfo_count = db.session.query(Poligraf.theme, func.count(Poligraf.id)). \
            group_by(Poligraf.theme).filter(Poligraf.deadline.between(statinfo.start.data, statinfo.end.data)).all()
        return render_template('info.html', form=statinfo, results=results, pfo_count=pfo_count,
                               title=f'Cтатистика за период c {statinfo.start.data} по {statinfo.end.data}')
    return render_template('info.html', form=statinfo, results=results, pfo_count=pfo_count,
                           title=f'Статистика за {TODAY.year} год')
