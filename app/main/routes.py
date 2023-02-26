import os
import json
import shutil

import requests
from sqlalchemy import func
from flask import Markup, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from . import bpr
from app.forms.form import *
from app.utils.extensions import *


# NAME = db.session.query(Users.full_name).filter_by(username=current_user.id).first()


@bpr.route("/login", methods=["POST", "GET"])  # вход пользователя в систему
def login():  # пароль и логин берутся из таблицы Users куда прописываются через интерфейс БД
    user_form = LoginForm()
    if current_user.is_authenticated:  # если пользователь уже авторизован, возвращаемся на главную страницу
        return redirect(url_for('route.index'))
    if user_form.validate_on_submit() and request.method == "POST":  # если пользователь не авторизован
        user_form = LoginForm(request.form)  # получаем данные из формы
        username = user_form.username.data
        password = user_form.password.data
        rmb = user_form.remember.data
        user = db.session.query(Users).filter_by(username=username).first()  # получаем данные из таблицы Users
        if db.session.query(Users).filter_by(username=username, password=password).first():
            login_user(user, remember=rmb)  # если пользователь успешно авторизован возвращаемся на главную страницу
            return redirect(url_for('route.index'))
        else:  # если авторизация не удалась выводим сообщение об ошибке
            flash("Неверная пара логин/пароль", "error")
    return render_template("share.html", form=user_form, title="Войти в систему")


@bpr.route('/logout')
@login_required
def logout():  # выход пользователя из системы
    logout_user()
    return redirect(url_for('route.login'))


@bpr.route('/', methods=['GET', 'POST'])
@login_required
def index():  # загрузка стартовой страницы
    form_search = SearchForm()  # загрузка формы поиска
    page = request.args.get('page', 1, type=int)  # разбиваем на страницы по указанному параметру
    results = db.session.query(Candidate).order_by(Candidate.status.asc()).paginate(page=page, per_page=12)
    count = db.session.query(Candidate.status, func.count(Candidate.status)). \
        filter_by(status=STATUS['new']).first()[1]
    flash(Markup(f'Новых анкет: {count}'), 'info')  # отображаем количество новых анкет
    if form_search.validate_on_submit() and request.method == 'POST':  # загрузка страницы результатов поиска
        form_search = SearchForm(request.form)
        search_by = form_search.full_name.data
        results = db.session.query(Candidate).filter(Candidate.full_name.ilike(f'%{search_by}%')). \
            paginate(page=page, per_page=12)  # получаем результаты поиска по фильтру фамилии
        return render_template('index.html', results=results, search_form=form_search)
    return render_template('index.html', results=results, search_form=form_search)


@bpr.route('/officer/', methods=['GET', 'POST'])
@login_required
def officer():  # загрузка страницы пользователя, показываем незавершенных кандидатов у сотрудника
    page = request.args.get('page', 1, type=int)
    results = db.session.query(Candidate).filter(Candidate.status != STATUS['result']).join(Check, isouter=True). \
        filter_by(officer=current_user.username).order_by(Candidate.status.asc()).paginate(page=page, per_page=12)
    return render_template('index.html', results=results, user=current_user.username)


@bpr.route('/profile/<int:cand_id>', methods=['GET', 'POST'])  # загрузка профиля кандидата
@login_required
def profile(cand_id):  # полный профиль кандидата/сотрудника
    form_passport = PassportForm(request.form)  # загружаем дополнительные формы для добавления анкетных данных
    form_address = AddressForm(request.form)
    form_work = WorkplaceForm(request.form)
    form_contact = ContactForm(request.form)
    form_staff = StaffForm(request.form)
    form_relation = RelationshipForm(request.form)
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()  # получаем  все данные кандидата из БД
    passports = db.session.query(Passport).filter_by(passport_id=cand_id).all()
    address = db.session.query(Address).filter_by(address_id=cand_id).all()
    contacts = db.session.query(Contact).filter_by(contact_id=cand_id).all()
    workplaces = db.session.query(Workplace).filter_by(work_place_id=cand_id).all()
    relations = db.session.query(RelationShip).filter_by(relation_id=cand_id).all()
    staffs = db.session.query(Staff).filter_by(staff_id=cand_id).all()
    checks = db.session.query(Check).filter_by(check_id=cand_id).all()
    # записи из реестра согласований выбираются на основании результата запроса результатов проверок
    registries = [db.session.query(Registry).filter(Registry.registry_check_id == i.id).first() for i in checks]
    pfos = db.session.query(Poligraf).filter_by(poligraf_id=cand_id).all()
    invs = db.session.query(Investigation).filter_by(inv_id=cand_id).all()
    inquries = db.session.query(Inquery).filter_by(iquery_id=cand_id).all()
    if (form_passport.validate_on_submit or
        form_address.validate_on_submit or
        form_work.validate_on_submit or
        form_contact.validate_on_submit or
        form_staff.validate_on_submit or
        form_relation.validate_on_submit) \
            and request.method == 'POST':  # добавление анкетных данных через модальные окна
        if form_passport.p_number_passport.data:  # если номер паспорта не пустой, то добавляем запись
            result = {k: v for k, v in form_passport.data.items() if k != 'p_submit' and k != 'csrf_token'} | \
                     {'passport_id': cand_id}
            db.session.add(Passport(**result))
            db.session.commit()
        if form_address.a_address.data:  # если адрес не пустой, то добавляем запись
            result = {k: v for k, v in form_address.data.items() if k != 'a_submit' and k != 'csrf_token'} | \
                     {'address_id': cand_id}
            db.session.add(Address(**result))
            db.session.commit()
        if form_work.w_work_place.data:  # если место работы не пусто, то добавляем запись
            result = {k: v for k, v in form_work.data.items() if k != 'w_submit' and k != 'csrf_token'} | \
                     {'work_place_id': cand_id}
            db.session.add(Workplace(**result))
            db.session.commit()
        if form_contact.c_contact.data:  # если контакт не пустой, то добавляем запись
            result = {k: v for k, v in form_contact.data.items() if k != 'c_submit' and k != 'csrf_token'} | \
                     {'contact_id': cand_id}
            db.session.add(Contact(**result))
            db.session.commit()
        if form_staff.s_staff.data:  # если должность заполнена, то добавляем запись
            result = {k: v for k, v in form_staff.data.items() if k != 's_submit' and k != 'csrf_token'} | \
                     {'staff_id': cand_id}
            db.session.add(Staff(**result))
            db.session.commit()
        if form_relation.r_full_name.data:  # если указаны связи, то добавляем запись
            result = {k: v for k, v in form_relation.data.items() if k != 'r_submit' and k != 'csrf_token'} | \
                     {'relation_id': cand_id}
            db.session.add(RelationShip(**result))
            db.session.commit()
        flash(Markup(f"Запись успешно добавлена"))
        return redirect(url_for('route.profile', cand_id=cand_id, flag='profile'))
    return render_template('profile.html', candidate=candidate, passports=passports, addresses=address,
                           relations=relations, staffs=staffs, workplaces=workplaces, contact=contacts,
                           checks=checks, registr=registries, inquries=inquries, pfos=pfos, invs=invs,
                           form_passport=form_passport, form_address=form_address, form_work=form_work,
                           form_contact=form_contact, form_staff=form_staff, form_relation=form_relation)


@bpr.route('/resume', methods=['GET', 'POST'])  # добавляем новую анкету
@login_required
def resume():
    file = FileForm()  # форма для добавления файла
    candidate = ResumeForm(request.form)  # форма для добавления новой анкеты
    if candidate.validate_on_submit() and request.method == 'POST':  # получаем данные из формы
        resume_dict = {k: v for k, v in candidate.data.items() if k != 'submit' and k != 'csrf_token'} | \
                      {'status': STATUS['new']} | {'update_date': TIME_NOW}
        result = db.session.query(Candidate).filter(Candidate.full_name == resume_dict['full_name'],
                                                    Candidate.birthday == resume_dict['birthday']).first()
        if result:  # проверка существования такой же анкеты, если есть анкета с таким именем, обновляем данные
            for k, v in resume_dict:
                setattr(result, k, v)
                db.session.commit()
            flash(Markup('Такая запись уже существует. Данные обновлены'))
        else:  # если нет таких анкет, добавляем новую запись
            db.session.add(Candidate(**resume_dict))
            db.session.commit()
            flash(Markup('Создана новая запись'))
            result = db.session.query(Candidate).filter(Candidate.full_name == resume_dict['full_name'],
                                                        Candidate.birthday == resume_dict['birthday']).first()
            flash(Markup('Добавлена новая запись'))
        return redirect(url_for('route.profile', cand_id=result.id))
    return render_template('share.html', file=file, form=candidate, title="Новая анкета кандидата")


@bpr.route('/resume_edit/<int:cand_id>', methods=['GET', 'POST'])  # редактируем основные данные анкеты
@login_required
def resume_edit(cand_id):
    result = db.session.query(Candidate).filter_by(id=cand_id).first()  # запрашиваем анкету
    candidate = ResumeForm(request.form, obj=result)  # выгружаем данные в форму
    if candidate.validate_on_submit() and request.method == 'POST':
        resume_dict = {k: v for k, v in candidate.data.items() if k != 'submit' and k != 'csrf_token'} | \
                      {'update_date': TIME_NOW}
        for k, v in resume_dict.items():  # обновляем данные
            setattr(result, k, v)
            db.session.commit()
        flash(Markup('Данные обновлены'))
        return redirect(url_for('route.profile', cand_id=result.id))
    return render_template('share.html', form=candidate, title="Редактирование анкеты")


@bpr.route('/add/<flag>/<int:cand_id>', methods=['GET', 'POST'])
@login_required
def add(flag, cand_id):  # добавляем данные расследований, запросов и результатов ПФО
    result = None
    title = None
    match flag:  # проверяем какие результаты добавляем в базу данных, флаг получаем из веб-интерфейса
        case "investigation":
            title = " Расследования"
            result = InvestigationForm(request.form)
        case "inquery":
            title = "Запросы"
            result = InquiryForm(request.form)
        case "poligraf":
            title = "Полиграф"
            result = PoligrafForm(request.form)  # загружаем нужные формы
    if result.validate_on_submit() and request.method == 'POST':
        match flag:  # передадем данные из формы в базу данных, фильруем данные, добавляем ID
            case "investigation":
                db.session.add(Investigation(**{k: v for k, v in result.data.items() if k != 'submit' and
                                                k != 'csrf_token'} | {'inv_id': cand_id}))
                db.session.commit()
            case "inquery":
                db.session.add(Inquery(**{k: v for k, v in result.data.items() if k != 'submit' and
                                          k != 'csrf_token'} | {'iquery_id': cand_id}))
            case "poligraf":
                db.session.add(Poligraf(**{k: v for k, v in result.data.items() if k != 'submit' and
                                           k != 'csrf_token'} | {'poligraf_id': cand_id}))
                db.session.commit()
                candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
                if candidate.status == STATUS['pfo_start']:  # проверяем статус анкеты, если указано ПФО, то завершаем
                    candidate.status = STATUS['finish']
                    db.session.commit()
        flash(Markup(f"Запись '{title}' успешно добавлена"))
        return redirect(url_for('route.profile', cand_id=cand_id))
    return render_template('share.html', form=result, title=title)


@bpr.route('/upload', methods=['GET', 'POST'])  # загрузка анкеты из файла Excel
@login_required
def upload():
    file = request.files['file']  # получаем файл
    if request.method == 'POST':
        file_excel = ExcelFile(file)  # создаем экземпляр класса ExcelFile для разборки файла,
        result = db.session.query(Candidate).filter(Candidate.full_name.ilike(file_excel.resume['full_name']),
                                                    Candidate.birthday == (file_excel.resume['birthday'])).first()
        if result:  # проверяем, есть анкета с таким именем
            for k, v in file_excel.resume.items():  # если есть, то обновляем основные данные
                setattr(result, k, v)
                db.session.commit()
            resume_data(result.id, file_excel.passport, file_excel.address, file_excel.contact,
                        file_excel.work, file_excel.staff)  # добавляем новые данные в базу данных через функцию
            flash(Markup('Такая запись уже существует. Данные обновлены'))
        else:  # если нет таких анкет, добавляем новую запись
            result = Candidate(**file_excel.resume)
            db.session.add(result)
            db.session.flush()  # фиксируем id для последующей записи
            resume_data(result.id, file_excel.passport, file_excel.address, file_excel.contact,
                        file_excel.work, file_excel.staff)  # добавляем новые данные в базу данных через функцию
            db.session.commit()  # окончательно сохраняем в базу данных основные данные
            flash(Markup('Создана новая запись'))
        return redirect(url_for('route.profile', cand_id=result.id))


@bpr.route('/send_resume/<int:cand_id>', methods=['GET'])  # отправка анкеты на проверку
def send_resume(cand_id):
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()  # выбираем данные анкеты
    passport = db.session.query(Passport).filter_by(passport_id=cand_id).order_by(Passport.passport_id.desc()).first()
    address = db.session.query(Address).filter_by(address_id=cand_id). \
        filter(Address.type.ilike("%регистрац%")).order_by(Address.address_id.desc()).first()
    decerial = json.dumps({"resume": cand_schema.dump(candidate)} |
                          {"passport": passp_schema.dump(passport)} |
                          {"address": addr_schema.dump(address)} |
                          {"officer": current_user.username})  # десериализация результатов запроса, создаем json
    # url = "https://httpbin.org/post"  # адрес для отправки анкеты на проверку
    # response = requests.post(url=url, json=decerial)  # отправка анкеты на проверку
    # response.raise_for_status()
    # if response.status_code == 200:   # проверка статуса отправки
    #     flash(Markup("Анкета успешно отправлена"))
    #     candidate.status = STATUS['robot_start']  # устанавливаем статус Автопроверка
    #     db.session.commit()
    #     return redirect(url_for('route.index'))
    # else:
    #     flash(Markup("Отправка анкеты не удалась попробуйте еще раз позднее"))
    #     return redirect(url_for('route.profile', cand_id=cand_id))
    print(decerial)
    flash(Markup("Анкета успешно отправлена"))
    return redirect(url_for('route.index'))


@bpr.route('/check/<int:cand_id>/<int:check_id>', methods=['GET', 'POST'])
@login_required  # форма проверки кандидата
def check(cand_id, check_id):
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    result = db.session.query(Check).filter_by(id=check_id).first()  # запрашиваем данные проверки, если есть
    path = os.path.join(BASE_PATH, candidate.full_name[0], f"{str(candidate.id)}-{candidate.full_name}", TIME_NOW[:-9])
    if request.method == 'GET':
        # if check_id is False:  # создаем  путь и папку к материалам проверки
        #   os.makedirs(path)  #  создаем папку для материалов проверки
        #   os.startfile(path)  # открываем папку с проверкой
        if check_id is False and candidate.status not in [STATUS['new'], STATUS['result']]:
            flash(Markup("Анкета взята в работу и еще не закончена"))
            return redirect(url_for('route.index'))  # проверка на одновременную работу с анкетой
        candidate.status = STATUS['active']  # меняем статус анкеты
        db.session.commit()
    checks = CheckForm(request.form)
    if cand_id:
        checks = CheckForm(request.form, obj=result)  # загружаем  предварительные (старые данные)
    if checks.validate_on_submit() and request.method == 'POST':
        if check_id:    # если редактируется проверка то перезаписываем данные
            chkc = {k: v for k, v in checks.data.items() if k != 'submit' and k != 'csrf_token'} | \
                   {'date_check': TIME_NOW} | {'officer': current_user.username}
            for k, v in chkc.items():
                setattr(result, k, v)
                db.session.commit()
        else:   # если новая проверка, то добавляем его в базу даннных
            chkc = {k: v for k, v in checks.data.items() if k != 'submit' and k != 'csrf_token'} | \
                   {'date_check': TIME_NOW} | {'path': path} | {'officer': current_user.username}
            db.session.add(Check(**chkc))
            db.session.commit()
        if chkc['resume'] == 'Сохранить':
            flash(Markup("Проверка успешно сохранена"))
        else:
            if chkc['pfo']:  # если поставлена отметка ПФО меняем статус
                candidate.status = STATUS['pfo_start']
                db.session.commit()
            else:
                candidate.status = STATUS['finish']
                db.session.commit()
            flash(Markup("Проверка завершена"))
        return redirect(url_for('route.index'))
    return render_template('share.html', form=checks, title="Проверка кандидата")


@bpr.route('/registr/<int:cand_id>/<int:check_id>', methods=('GET', 'POST'))  # отправка решения по кандидату
@login_required
def registr(cand_id, check_id):
    registry = RegistrForm(request.form)  # загружаем форму согласования
    if registry.validate_on_submit() and request.method == 'POST':
        reg = {k: v for k, v in registry.data.items() if k != 'submit' and k != 'csrf_token'} | \
              {'registry_check_id': check_id} | {'dec_date': TIME_NOW} | \
              {'supervisor': current_user.username}
        db.session.add(Registry(**reg))  # получаем данные из формы и записываем в базу данных
        db.session.commit()
        candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
        candidate.status = STATUS['result']  # меняем статус в таблице на "Решение"
        db.session.commit()
        # url = "https://httpbin.org/post"  # адрес для отправки ответа по результам проверки
        # value = json.dumps(
        #     {
        #         "id": candidate.request_id,
        #         "marks": reg['marks'],
        #         "decision": reg['decision'],
        #         "date": reg['dec_date'],
        #         "supervisor": reg['supervisor']
        #     }
        # )
        # response = requests.post(url=url, json=value)
        # response.raise_for_status()
        # if response.status_code == 200:
        #     print(response.status_code)
        #     candidate.status = STATUS['result']  # меняем статус в таблице на "Решение принято"
        #     db.session.commit()
        #     flash(Markup("Решение успешно отправлено"))
        #     return redirect(url_for('route.index'))
        # else:
        #     flash(Markup("Отправка анкеты не удалась попробуйте еще раз позднее"))
        flash(Markup("Решение успешно отправлено"))
        return redirect(url_for('route.index'))
    return render_template('share.html', form=registry, title="Согласование кандидата")


@bpr.route('/info', methods=('GET', 'POST'))  # create statistic info
@login_required
def info():
    statinfo = InfoForm(request.form)
    results = db.session.query(Registry.decision, func.count(Registry.decision)). \
        group_by(Registry.decision).filter(
        Registry.dec_date.like(f"%{TIME_NOW[:-15]}%")).all()
    if statinfo.validate_on_submit() and request.method == 'POST':
        month_year = InfoForm(request.form)
        results = db.session.query(Registry.decision, func.count(Registry.decision)). \
            group_by(Registry.decision).filter(Registry.dec_date.like(f'%{month_year.year.data}-'
                                                                      f'{month_year.month.data}%')).all()
        return render_template('info.html', form=statinfo, results=results)
    return render_template('info.html', form=statinfo, results=results)
