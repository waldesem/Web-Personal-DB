import os

from sqlalchemy import func
from flask import Markup, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from . import bpr
from app.main.apis import send_registr
from app.forms.form import *
from app.models.model import *
from app.utils.extensions import ExcelFile, resume_data


@bpr.route("/login", methods=["POST", "GET"])  # вход пользователя в систему
def login():  # пароль и логин берутся из таблицы Users куда прописываются через интерфейс БД
    user_form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('route.index'))
    if user_form.validate_on_submit() and request.method == "POST":
        user_form = LoginForm(request.form)
        username = user_form.username.data
        password = user_form.password.data
        rmb = user_form.remember.data  # сохранить логин-пароль
        user = db.session.query(Users).filter_by(username=username).first()
        if db.session.query(Users).filter_by(username=username, password=password).first():
            login_user(user, remember=rmb)
            return redirect(url_for('route.index'))
        else:
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
    form_search = SearchForm()
    page = request.args.get('page', 1, type=int)
    results = db.session.query(Candidate).filter(Candidate.status != STATUS['result']). \
        order_by(Candidate.status.desc()).paginate(page=page, per_page=12)
    count = db.session.query(Candidate.status, func.count(Candidate.status)). \
        filter_by(status=STATUS['new']).first()[1]
    flash(Markup(f'Новых анкет: {count}'), 'info')
    if form_search.validate_on_submit() and request.method == 'POST':  # загрузка страницы результатов поиска
        form_search = SearchForm(request.form)
        search_by = form_search.full_name.data
        results = db.session.query(Candidate).filter(Candidate.full_name.ilike(f'%{search_by}%')). \
            paginate(page=page, per_page=12)
        return render_template('index.html', results=results, search_form=form_search)
    return render_template('index.html', results=results, search_form=form_search)


@bpr.route('/officer/', methods=['GET', 'POST'])
@login_required
def officer():  # загрузка страницы пользователя
    form_search = SearchForm()
    page = request.args.get('page', 1, type=int)
    results = db.session.query(Candidate).filter(Candidate.status not in [STATUS['result'], STATUS['finish']]). \
        join(Check, isouter=False).filter_by(officer=current_user.username).order_by(Candidate.status.desc()). \
        paginate(page=page, per_page=12)  # показываем кандидатов в проверке у сотрудника
    if form_search.validate_on_submit() and request.method == 'POST':  # загрузка страницы результатов поиска
        form_search = SearchForm(request.form)
        search_by = form_search.full_name.data  # поиск кандидатов которых проверял пользователь
        results = db.session.query(Candidate).filter(Candidate.full_name.ilike(f'%{search_by}%')). \
            join(Check, isouter=False).filter_by(officer=current_user.username).paginate(page=page, per_page=12)
        return render_template('index.html', results=results, search_form=form_search, user=current_user.username)
    return render_template('index.html', results=results, search_form=form_search, user=current_user.username)


@bpr.route('/profile/<int:cand_id>', methods=['GET', 'POST'])  # вся информация о кандидате
@login_required
def profile(cand_id):  # полный профиль кандидата/сотрудника
    candidate, passports, staffs, relations, address, workplaces, contacts, \
        checks, registries, inquries, pfos, invs = \
        None, None, None, None, None, None, None, None, None, None, None, None
    form_passport = PassportForm(request.form)
    form_address = AddressForm(request.form)
    form_work = WorkplaceForm(request.form)
    form_contact = ContactForm(request.form)
    form_staff = StaffForm(request.form)
    form_relation = RelationshipForm(request.form)
    if request.method == 'GET':
        candidate = db.session.query(Candidate).filter_by(id=cand_id).first_or_404()
        passports = db.session.query(Passport).filter_by(passport_id=cand_id).all()
        address = db.session.query(Address).filter_by(address_id=cand_id).all()
        contacts = db.session.query(Contact).filter_by(contact_id=cand_id).all()
        workplaces = db.session.query(Workplace).filter_by(work_place_id=cand_id).all()
        relations = db.session.query(RelationShip).filter_by(relation_id=cand_id).all()
        staffs = db.session.query(Staff).filter_by(staff_id=cand_id).all()
        checks = db.session.query(Check).filter_by(check_id=cand_id).all()
        # join(Registry, isouter=False).filter_by(registry_check_id=Check.id).all()
        pfos = db.session.query(Poligraf).filter_by(poligraf_id=cand_id).all()
        invs = db.session.query(Investigation).filter_by(inv_id=cand_id).all()
        inquries = db.session.query(Inquery).filter_by(iquery_id=cand_id).all()
    elif request.method == 'POST':  # добавление анкетных данных через модальные окна
        if form_passport.number_passport.data:
            result = {k: v for k, v in form_passport.data.items() if k != 'submit' and k != 'csrf_token'} | \
                     {'passport_id': cand_id}
            db.session.add(Passport(**result))
            db.session.commit()
        if form_address.address.data:
            result = {k: v for k, v in form_address.data.items() if k != 'submit' and k != 'csrf_token'} | \
                     {'address_id': cand_id}
            db.session.add(Address(**result))
            db.session.commit()
        if form_work.work_place.data:
            result = {k: v for k, v in form_work.data.items() if k != 'submit' and k != 'csrf_token'} | \
                     {'work_place_id': cand_id}
            db.session.add(Workplace(**result))
            db.session.commit()
        if form_contact.contact.data:
            result = {k: v for k, v in form_contact.data.items() if k != 'submit' and k != 'csrf_token'} | \
                     {'contact_id': cand_id}
            db.session.add(Contact(**result))
            db.session.commit()
        if form_staff.staff.data:
            result = {k: v for k, v in form_staff.data.items() if k != 'submit' and k != 'csrf_token'} | \
                     {'staff_id': cand_id}
            db.session.add(Staff(**result))
            db.session.commit()
        if form_relation.full_name.data:
            result = {k: v for k, v in form_relation.data.items() if k != 'submit' and k != 'csrf_token'} | \
                     {'relation_id': cand_id}
            db.session.add(RelationShip(**result))
            db.session.commit()
        flash(Markup(f"Запись успешно добавлена"))
        return redirect(url_for('route.profile', cand_id=cand_id, flag='profile'))
    return render_template('profile.html', candidate=candidate, passports=passports, addresses=address,
                           relations=relations, staffs=staffs, workplaces=workplaces, contact=contacts,
                           checks=checks, registries=registries, inquries=inquries, pfos=pfos, invs=invs,
                           form_passport=form_passport, form_address=form_address, form_work=form_work,
                           form_contact=form_contact, form_staff=form_staff, form_relation=form_relation)


@bpr.route('/resume', methods=['GET', 'POST'])  # добавляем новую анкету
@login_required
def resume():
    file = FileForm()
    candidate = ResumeForm(request.form)
    if candidate.validate_on_submit() and request.method == 'POST':
        resume_dict = {k: v for k, v in candidate.data.items() if k != 'submit' and k != 'csrf_token'} | \
                      {'status': STATUS['new']} | {'update_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
        result = db.session.query(Candidate).filter(Candidate.full_name == resume_dict['full_name'],
                                                    Candidate.birthday == resume_dict['birthday']).first()
        if result:  # проверка существования такой же анкеты, если есть анкета с таким именем
            for k, v in resume_dict:
                setattr(result, k, v)
                db.session.commit()
            flash(Markup('Такая запись уже существует. Данные обновлены'))
            return redirect(url_for('route.profile', cand_id=result.id))
        else:  # если нет таких анкет
            values = Candidate(**resume_dict)  # распаковываем словарь и записываем в БД
            db.session.add(values)
            db.session.commit()
            flash(Markup('Создана новая запись'))
            result = db.session.query(Candidate).filter(Candidate.full_name == resume_dict['full_name'],
                                                        Candidate.birthday == resume_dict['birthday']).first()
            return redirect(url_for('route.profile', cand_id=result.id))
    return render_template('share.html', file=file, form=candidate, title="Новая анкета кандидата")


@bpr.route('/resume_edit/<int:cand_id>', methods=['GET', 'POST'])  # редактируем основные данные анкеты
@login_required
def resume_edit(cand_id):
    result = db.session.query(Candidate).filter_by(id=cand_id).first()  # запрашиваем анкету
    candidate = ResumeForm(request.form, obj=result)
    if candidate.validate_on_submit() and request.method == 'POST':
        resume_dict = {k: v for k, v in candidate.data.items() if k != 'submit' and k != 'csrf_token'} | \
                      {'update_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
        for k, v in resume_dict.items():
            setattr(result, k, v)
            db.session.commit()
        flash(Markup('Данные обновлены'))
        return redirect(url_for('route.profile', cand_id=result.id))
    return render_template('share.html', form=candidate, title="Редактирование анкеты")


@bpr.route('/add/<flag>/<int:cand_id>', methods=['GET', 'POST'])  # добавить данные в анкету
@login_required
def add(flag, cand_id):
    result = None
    title = None
    match flag:
        case "investigation":
            title = " Расследования"
            result = InvestigationForm(request.form)
        case "inquery":
            title = "Запросы"
            result = InquiryForm(request.form)
        case "poligraf":
            title = "Полиграф"
            result = PoligrafForm(request.form)
    if result.validate_on_submit() and request.method == 'POST':
        match flag:
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
                if candidate.status == STATUS['pfo_start']:  # проверяем статус анкеты, если ПФО, то завершаем
                    candidate.status = STATUS['finish']
                    db.session.commit()
        flash(Markup(f"Запись '{title}' успешно добавлена"))
        return redirect(url_for('route.profile', cand_id=cand_id))
    return render_template('share.html', form=result, title=title)


@bpr.route('/upload', methods=['GET', 'POST'])  # загрузка анкеты из файла Excel
@login_required
def upload():
    file = request.files['file']
    if request.method == 'POST':
        file_excel = ExcelFile(file)
        result = db.session.query(Candidate).filter(Candidate.full_name.ilike(file_excel.resume['full_name']),
                                                    Candidate.birthday == (file_excel.resume['birthday'])).first()
        if result:  # если есть анкета с таким именем
            for k, v in file_excel.resume.items():
                setattr(result, k, v)
                db.session.commit()
            resume_data(result.id, file_excel.passport, file_excel.address, file_excel.contact,
                        file_excel.work, file_excel.staff)
            flash(Markup('Такая запись уже существует. Данные обновлены'))
        else:
            result = Candidate(**file_excel.resume)
            db.session.add(result)
            db.session.flush()
            resume_data(result.id, file_excel.passport, file_excel.address, file_excel.contact,
                        file_excel.work, file_excel.staff)
            db.session.commit()
            flash(Markup('Создана новая запись'))
        return redirect(url_for('route.profile', cand_id=result.id))


@bpr.route('/check/<int:cand_id>', methods=['GET', 'POST'])
@login_required
def check(cand_id):  # новая проверка кандидата
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    if candidate.status not in [STATUS['new'], STATUS['result']]:  # проверка на одновременную работу с анкетой
        flash(Markup("Анкета взята в работу и еще не закончена"))
        return redirect(url_for('route.index'))
    else:
        path = os.path.join(rf'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\Персонал\Персонал-2\\',
                            candidate.full_name[0], f"{str(candidate.id)} - {candidate.full_name}",
                            datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))
        # os.makedirs(path)  #  создаем папку для материалов проверки
        chkc = {'check_id': cand_id} | {'date_check': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} | \
               {'path': path} | {'officer': current_user.username}
        result = Check(**chkc)
        db.session.add(result)
        db.session.flush()
        check_id = result.id
        db.session.commit()
        return redirect(url_for('route.check_edit', cand_id=candidate.id, check_id=check_id))


@bpr.route('/check_edit/<int:cand_id>/<int:check_id>', methods=['GET', 'POST'])
@login_required  # редактирование проверки кандидата
def check_edit(cand_id, check_id):
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    result = db.session.query(Check).filter_by(id=check_id).first()
    checks = CheckForm(request.form, obj=result)
    candidate.status = STATUS['active']
    db.session.commit()
    path = result.path
    if os.path.isdir(path):
        os.startfile(path)  # открываем папку с проверкой
    else:
        path = os.path.join(rf'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\Персонал\Персонал-2\\',
                            candidate.full_name[0], f"{str(candidate.id)} - {candidate.full_name}",
                            datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))
        # os.makedirs(path)  #  создаем папку для материалов проверки
        # os.startfile(path)
        flash(Markup('Папка не найдена. Создана новая папка'))
    if checks.validate_on_submit() and request.method == 'POST':
        chkc = {k: v for k, v in checks.data.items() if k != 'submit' and k != 'csrf_token'} | \
               {'inv_id': cand_id} | {'date_check': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} | \
               {'path': path} | {'officer': current_user.username}
        for k, v in chkc.items():
            setattr(result, k, v)
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


@bpr.route('/registr/<int:cand_id>/<int:check_id>', methods=('GET', 'POST'))  # финальное решение по кандидату
@login_required  # согласование кандидата
def registr(cand_id, check_id):
    registry = RegistrForm(request.form)  # загружаем форму согласования
    if registry.validate_on_submit() and request.method == 'POST':
        reg = dict(supervisor=current_user.username,
                   marks=registry.marks.data,
                   decision=registry.decision.data,
                   dec_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                   registry_check_id=check_id)
        db.session.add(Registry(**reg))
        db.session.commit()
        candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
        candidate.status = STATUS['result']  # меняем статус в таблице на "Решение"
        db.session.commit()
        response = send_registr(candidate, reg)
        if response.status_code == 200:
            print(response.status_code)
            candidate.status = STATUS['result']  # меняем статус в таблице на "Решение принято"
            db.session.commit()
            flash(Markup("Решение успешно отправлено"))
            return redirect(url_for('route.index'))
        else:
            flash(Markup("Отправка анкеты не удалась попробуйте еще раз позднее"))
    return render_template('share.html', form=registry, title="Согласование кандидата")


@bpr.route('/info', methods=('GET', 'POST'))  # create statistic info
@login_required
def info():
    statinfo = InfoForm(request.form)
    results = db.session.query(Registry.decision, func.count(Registry.decision)). \
        group_by(Registry.decision).filter(
        Registry.dec_date.like(f"%{datetime.datetime.now().strftime('%Y-%m-%d')[:5]}%")).all()
    if statinfo.validate_on_submit() and request.method == 'POST':
        month_year = InfoForm(request.form)
        results = db.session.query(Registry.decision, func.count(Registry.decision)). \
            group_by(Registry.decision).filter(Registry.dec_date.like(f'%{month_year.year.data}-'
                                                                      f'{month_year.month.data}%')).all()
        return render_template('info.html', form=statinfo, results=results)
    return render_template('info.html', form=statinfo, results=results)
