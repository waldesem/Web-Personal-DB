import os

from sqlalchemy import func
from flask import Markup, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from . import bpr
from app.main.apis import STATUS, send_registr
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
        rmb = user_form.remember.data  # сохранить логин-пароль для сеанса
        user = db.session.query(Users).filter_by(username=username).first()
        if db.session.query(Users).filter_by(username=username, password=password).first():
            login_user(user, remember=rmb)
            return redirect(url_for('route.index'))
        else:
            flash("Неверная пара логин/пароль", "error")
    return render_template("login.html", form=user_form)


@bpr.route('/logout')
@login_required
def logout():  # выход пользователя из системы
    logout_user()
    return redirect(url_for('route.login'))


@bpr.route('/index/<user>', methods=['GET', 'POST'])
@bpr.route('/index', methods=['GET', 'POST'])
@bpr.route('/', methods=['GET', 'POST'])
@login_required
def index(user=None):  # загрузка стартовой страницы
    form_search = SearchForm()
    page = request.args.get('page', 1, type=int)
    if user:  # загрузка личного кабинета
        results = db.session.query(Candidate).filter(Candidate.status != STATUS['result'],
                                                     Candidate.status != STATUS['finish']). \
            join(Check, isouter=False).filter_by(officer=current_user.username).order_by(Candidate.status.desc()). \
            paginate(page=page, per_page=12)
    else:  # загрузка страницы новых кандидатов и тех, что находятся в работе
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
        return render_template('index.html', results=results, form=form_search)
    return render_template('index.html', results=results, search_form=form_search, user=current_user.username)


@bpr.route('/profile/<int:cand_id>', methods=['GET', 'POST'])  # вся информация о кандидате
@login_required
def profile(cand_id):  # полный профиль кандидата/сотрудника
    if request.method == 'GET' or 'POST':
        candidate = db.session.query(Candidate).filter_by(id=cand_id).first_or_404()
        passports = db.session.query(Passport).filter_by(passport_id=cand_id).all()
        address = db.session.query(Address).filter_by(address_id=cand_id).all()
        contacts = db.session.query(Contact).filter_by(contact_id=cand_id).all()
        workplaces = db.session.query(Workplace).filter_by(work_place_id=cand_id).all()
        relations = db.session.query(RelationShip).filter_by(relation_id=cand_id).all()
        staffs = db.session.query(Staff).filter_by(staff_id=cand_id).all()
        checks = db.session.query(Check).filter_by(check_id=cand_id).all()
        registries = db.session.query(Registry).filter_by(registry_cand_id=cand_id).all()
        pfos = db.session.query(Poligraf).filter_by(poligraf_id=cand_id).all()
        invs = db.session.query(Investigation).filter_by(inv_id=cand_id).all()
        inquries = db.session.query(Inquery).filter_by(iquery_id=cand_id).all()
        return render_template('profile.html', candidate=candidate, passports=passports,
                               addresses=address, relations=relations, staffs=staffs,
                               workplaces=workplaces, contact=contacts, checks=checks, registries=registries,
                               inquries=inquries, pfos=pfos, invs=invs)


@bpr.route('/resume/<int:cand_id>', methods=['GET', 'POST'])  # добавляем или редактируем анкету
@login_required
def resume(cand_id):
    file = FileForm()
    result = None
    if cand_id == 88888888:  # создаем новую анкету вручную
        candidate = ResumeForm(request.form)
    else:  # редактируем анкету
        result = db.session.query(Candidate).filter_by(id=cand_id).first()  # запрашиваем анкету
        candidate = ResumeForm(request.form, obj=result)
    if candidate.validate_on_submit() and request.method == 'POST':
        resum = dict(region=candidate.region.data,
                     full_name=candidate.full_name.data,
                     last_name=candidate.last_name.data,
                     birthday=candidate.birthday.data,
                     birth_place=candidate.birth_place.data,
                     country=candidate.country.data,
                     snils=candidate.snils.data,
                     inn=candidate.inn.data,
                     education=candidate.education.data,
                     addition=candidate.addition.data,
                     update_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
        passport = candidate.passport
        address = candidate.address
        work = candidate.work_place
        contact = candidate.contacts
        staff = candidate.staff
        relation = candidate.relation
        if cand_id != 88888888:  # перезаписываем данные после редактирования
            for k, v in resum.items():
                setattr(result, k, v)
                db.session.commit()
            resume_data(result, passport, address, work, contact, staff, relation)
            flash(Markup('Запись успешно изменена'))
            return redirect(url_for('route.profile', cand_id=result.id))
        else:  # проверка существования такой же анкеты
            result = db.session.query(Candidate).filter(Candidate.full_name == candidate.birthday.data,
                                                        Candidate.birthday == candidate.birthday.data).first()
            if result:  # если есть анкета с таким именем
                for k, v in resum:
                    setattr(result, k, v)
                    result.status = STATUS['new']
                    db.session.commit()
                resume_data(result, passport, address, work, contact, staff, relation)
                flash(Markup('Такая запись уже существует. Данные обновлены'))
                return redirect(url_for('route.profile', cand_id=result.id))
            else:
                result = Candidate(**resum)
                result.status = STATUS['new']
                db.session.add(result)
                db.session.flush()
                resume_data(result, passport, address, work, contact, staff, relation)
                db.session.commit()
                flash(Markup('Создана новая запись'))
                return redirect(url_for('route.profile', cand_id=result.id))
    return render_template('resume.html', file=file, form=candidate)


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
            resume_data(result, file_excel.passport, file_excel.address, file_excel.contact,
                        file_excel.work, file_excel.staff)
            flash(Markup('Такая запись уже существует. Данные обновлены'))
        else:
            result = Candidate(**file_excel.resume)
            db.session.add(result)
            db.session.flush()
            resume_data(result, file_excel.passport, file_excel.address, file_excel.contact,
                        file_excel.work, file_excel.staff)
            db.session.commit()
            flash(Markup('Создана новая запись'))
        return redirect(url_for('route.profile', cand_id=result.id))


@bpr.route('/check/<int:cand_id>/<int:check_id>', methods=['GET', 'POST'])
@login_required  # форма проверки кандидата
def check(cand_id, check_id):
    result = None
    url = None
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    if check_id:  # если редактируется старая проверка
        candidate.status = STATUS['active']
        db.session.commit()
        result = db.session.query(Check).filter_by(id=check_id).first()
        checks = CheckForm(request.form, obj=result)
    else:  # если заводится новая проверка
        if candidate.status not in [STATUS['new'], STATUS['result']]:  # проверяем статус
            flash(Markup("Анкета взята в работу и еще не закончена"))
            return redirect(url_for('route.index'))
        else:
            candidate.status = STATUS['active']
            db.session.commit()
            url = os.path.join(rf'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\Персонал\Персонал-2\\',
                               candidate.full_name[0], f"{str(candidate.id)} - {candidate.full_name}",
                               datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))
            # os.makedirs(url)  #  создаем папку для материалов проверки
            # os.startfile(url)
            checks = CheckForm(request.form)
    if checks.validate_on_submit() and request.method == 'POST':
        chk = dict(check_work_place=checks.check_work_place.data,
                   former_employee=checks.former_employee.data,
                   check_passport=checks.check_passport.data,
                   check_inn=checks.check_inn.data,
                   check_debt=checks.check_debt.data,
                   check_bankruptcy=checks.check_bankruptcy.data,
                   check_bki=checks.check_bki.data,
                   check_court=checks.check_court.data,
                   check_affiliation=checks.check_affiliation.data,
                   check_terrorist=checks.check_terrorist.data,
                   check_mvd=checks.check_mvd.data,
                   check_internet=checks.check_internet.data,
                   check_cronos=checks.check_cronos.data,
                   check_cross=checks.check_cross.data,
                   check_addition=checks.check_addition.data,
                   pfo=checks.pfo.data,
                   resume=checks.resume.data,
                   officer=current_user.username,
                   date_check=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                   check_id=cand_id)
        if check_id:
            for k, v in chk.items():
                setattr(result, k, v)
                db.session.commit()
        else:
            result = Check(**chk)
            result.url = url
            db.add(result)
            db.session.commit()
        if chk['resume'] == 'Сохранить':
            return redirect(url_for('route.index'))
        else:
            if chk['pfo']:  # если поставлена отметка pfo
                candidate.status = STATUS['pfo_start']
                db.session.commit()
            else:
                candidate.status = STATUS['finish']
                db.session.commit()
            return redirect(url_for('route.index'))
    return render_template('check.html', form=checks)


@bpr.route('/registr/<int:cand_id>/<int:check_id>', methods=('GET', 'POST'))  # финальное решение по кандидату
@login_required  # согласование кандидата
def registr(cand_id, check_id):
    registry = RegistrForm(request.form)  # загружаем форму согласования
    if registry.validate_on_submit() and request.method == 'POST':
        reg = dict(supervisor=current_user.username,
                   marks=registry.marks.data,
                   decision=registry.decision.data,
                   dec_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                   registr_check_id=check_id,
                   registr_cand_id=cand_id)
        db.session.add(Registry(**reg))
        db.session.commit()
        candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
        candidate.status = STATUS['result']  # меняем статус в таблице на "Решение"
        db.session.commit()
        response = send_registr(candidate, reg)
        if response.json():  # какой ответ будет от сервера пока не понятно
            candidate.status = STATUS['result']  # меняем статус в таблице на "Решение принято"
            db.session.commit()
            flash(Markup("Решение успешно отправлено"))
            return redirect(url_for('route.index'))
        else:
            flash(Markup("Отправка анкеты не удалась попробуйте еще раз позднее"))
    return render_template('registr.html', form=registry)


@bpr.route('/poligraf/<int:cand_id>', methods=('GET', 'POST'))  # результаты проверки на полиграфе
@login_required
def poligraf(cand_id):
    pfo = PoligrafForm(request.form)
    if pfo.validate_on_submit() and request.method == 'POST':
        db.session.add(Poligraf(theme=pfo.theme.data,
                                results=pfo.results.data,
                                officer=current_user.username,
                                date_pfo=pfo.date_pfo.data,
                                poligraf_id=cand_id))
        db.session.commit()
        candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
        if candidate.status == STATUS['pfo']:
            candidate.status = STATUS['finish']
            db.session.commit()
        flash(Markup("Запись успешно добавлена"))
        return redirect(url_for('route.index'))
    return render_template('poligraf.html', form=pfo)


@bpr.route('/investigation/<int:cand_id>', methods=('GET', 'POST'))  # результаты служебной проверки
@login_required
def investigation(cand_id):
    inv = InvestigationForm(request.form)
    if inv.validate_on_submit() and request.method == 'POST':
        db.session.add(Investigation(theme=inv.theme.data,
                                     info=inv.info.data,
                                     date_inv=inv.date_inv.data,
                                     inv_id=cand_id))
        db.session.commit()
        flash(Markup("Запись успешно добавлена"))
        return redirect(url_for('route.index'))
    return render_template('investigation.html', form=inv)


@bpr.route('/inquiry/<int:cand_id>', methods=('GET', 'POST'))  # дополнительная информация о сотруднике
@login_required
def inquiry(cand_id):
    iqueries = InquiryForm(request.form)
    if iqueries.validate_on_submit() and request.method == 'POST':
        db.session.add(Inquery(info=iqueries.info.data,
                               initiator=iqueries.initiator.data,
                               date_inq=iqueries.date_inq.data,
                               iquery_id=cand_id))
        db.session.commit()
        flash(Markup("Запись успешно добавлена"))
        return redirect(url_for('route.index'))
    return render_template('inquiry.html', form=iqueries)


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
