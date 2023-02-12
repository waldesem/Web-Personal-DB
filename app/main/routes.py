import os

from sqlalchemy import func
from flask import Markup, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from . import bpr
from app.main.apis import STATUS, send_registr
from app.forms.form import *
from app.models.model import *
from app.utils.extensions import ExcelFile, part_excel_data, part_resume_data


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
        user = db.session.query(Users).select_from(Users).filter_by(username=username).first()
        if db.session.query(Users).select_from(Users).filter_by(username=username, password=password).first():
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


@bpr.route('/index', methods=['GET', 'POST'])
@bpr.route('/', methods=['GET', 'POST'])
@login_required
def index():  # загрузка стартовой страницы
    page = request.args.get('page', 1, type=int)
    form_search = SearchForm()  # загрузка страницы новых кандидатов и тех, что находятся в работе
    results = db.session.query(Candidate).filter(Candidate.status != STATUS['result']). \
        order_by(Candidate.status.desc()).paginate(page=page, per_page=12)
    count = db.session.query(Candidate.status, func.count(Candidate.status)). \
        filter_by(status=STATUS['new']).first()[1]
    if request.method == 'POST':
        form_search = SearchForm(request.form)
        search_by = form_search.full_name.data
        results = db.session.query(Candidate).filter(Candidate.full_name.ilike(f'%{search_by}%')). \
            paginate(page=page, per_page=12)
        return render_template('index.html', results=results, form=form_search)
    return render_template('index.html', results=results, form=form_search, count=count)


@bpr.route('/cabinet/', methods=['GET', 'POST'])
@login_required
def cabinet():  # загрузка страницы пользователя со списком кандидатов которые находятся у него в
    page = request.args.get('page', 1, type=int)
    results = db.session.query(Candidate).filter(Candidate.status != STATUS['result'],
                                                 Candidate.status != STATUS['finish']). \
        join(Check, isouter=False).filter_by(officer=current_user.username).order_by(Candidate.status.desc()). \
        paginate(page=page, per_page=12)
    if request.method == 'POST':
        results = db.session.query(Candidate).filter(Candidate.status == STATUS['new']). \
            paginate(page, per_page=12)
        return render_template('cabinet.html', results=results)
    return render_template('cabinet.html', results=results)


@bpr.route('/profile/<int:cand_id>', methods=['GET', 'POST'])  # вся информация  о кандидате
@login_required
def profile(cand_id):  # полный профиль кандидата/сотрудника
    if request.method == 'GET' or 'POST':
        candidate = db.session.query(Candidate).filter_by(id=cand_id).first_or_404()
        last_names = db.session.query(LastName).filter_by(last_name_id=cand_id).all()
        passports = db.session.query(Passport).filter_by(passport_id=cand_id).all()
        address = db.session.query(Address).filter_by(address_id=cand_id).all()
        contacts = db.session.query(Contact).filter_by(phone_id=cand_id).all()
        workplaces = db.session.query(Workplace).filter_by(work_place_id=cand_id).all()
        relations = db.session.query(RelationShip).filter_by(relationsip_id=cand_id).all()
        staffs = db.session.query(Staff).filter_by(staff_id=cand_id).all()
        checks = db.session.query(Check).filter_by(check_id=cand_id).all()
        registries = db.session.query(Registry).filter_by(registr_cand_id=cand_id).all()
        pfos = db.session.query(Poligraf).filter_by(poligraf_id=cand_id).all()
        invs = db.session.query(Investigation).filter_by(inv_id=cand_id).all()
        inquries = db.session.query(Inquery).filter_by(iquery_id=cand_id).all()
        return render_template('profile.html', candidate=candidate, last_names=last_names, passports=passports,
                               addresses=address, relations=relations, staffs=staffs,
                               workplaces=workplaces, phones=contacts, checks=checks, registries=registries,
                               inquries=inquries, pfos=pfos, invs=invs)


@bpr.route('/resume/<int:cand_id>', methods=['GET', 'POST'])  # добавляем или редактируем анкету
@login_required
def resume(cand_id):
    file = FileForm()
    result = None
    if cand_id == 88888888:  # создаем новую анкету вручную
        candidate = ResumeForm(request.form)
    elif cand_id == 999999999:  # загружаем анкету из файла Excel
        result = db.session.query(Candidate).filter(Candidate.full_name.ilike(ExcelFile.resume['full_name']),
                                                    Candidate.birthday == (ExcelFile.resume['birthday'])).first()
        if result:  # если есть анкета с таким именем
            part_excel_data(result)
            flash(Markup('Такая запись уже существует. Данные обновлены'))
        else:
            result = Candidate(**ExcelFile.resume)
            db.session.add(result)
            db.session.flush()
            part_excel_data(result)
            db.session.commit()
            flash(Markup('Создана новая запись'))
        return redirect(url_for('route.profile', cand_id=result.id))
    else:  # редактируем анкету
        result = db.session.query(Candidate).filter_by(id=cand_id).first()  # запрашиваем анкету
        candidate = ResumeForm(request.form, obj=result)
    if candidate.validate_on_submit() and request.method == 'POST':
        resum = dict(region=candidate.region.data,
                     full_name=candidate.full_name.data,
                     birthday=candidate.birthday.data,
                     birth_place=candidate.birth_place.data,
                     country=candidate.country.data,
                     snils=candidate.snils.data,
                     inn=candidate.inn.data,
                     education=candidate.education.data,
                     addition=candidate.addition.data,
                     update_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                     status=STATUS['new'])
        last_name = LastName(candidate.lastname.data)
        passport = Passport(candidate.passport.data)
        address = Address(candidate.address.data)
        work = Workplace(candidate.work_place.data)
        contact = Contact(candidate.contacts.data, )
        staff = Staff(candidate.staff.data)
        relation = RelationShip(candidate.relation.data)
        if cand_id != 88888888 and cand_id != 999999999:  # перезаписываем данные после редактирования
            for k, v in resum.items():
                setattr(result, k, v)
                db.session.commit()
            part_resume_data(result, last_name, passport, address, work, contact, staff, relation)
            return redirect(url_for('route.profile', cand_id=result.id))
        if cand_id == 88888888:  # проверка существования такой же анкеты
            result = db.session.query(Candidate).filter(Candidate.full_name == candidate.birthday.data,
                                                        Candidate.birthday == candidate.birthday.data).first()
            if result:  # если есть анкета с таким именем
                part_resume_data(result, last_name, passport, address, work, contact, staff, relation)
                flash(Markup('Такая запись уже существует. Данные обновлены'))
                return redirect(url_for('route.profile', cand_id=result.id))
            else:
                result = Candidate(**resum)
                db.add(result)
                db.session.flush()
                part_resume_data(result, last_name, passport, address, work, contact, staff, relation)
                db.session.commit()
                flash(Markup('Создана новая запись'))
                return redirect(url_for('route.profile', cand_id=result.id))
    return render_template('resume.html', file=file, form=candidate)


@bpr.route('/upload', methods=('GET', 'POST'))  # загрузка анкеты из файла Excel
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        ExcelFile(file)
        return redirect(url_for('route.resume', cand_id=999999999))


@bpr.route('/check/<int:cand_id>/<int:check_id>', methods=('GET', 'POST'))
@login_required  # форма проверки кандидата
def check(cand_id, check_id):
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    if check_id:  # если редактируется старая проверка
        candidate.status = STATUS['active']
        db.session.commit()
        result = db.session.query(Check).filter_by(id=check_id).first()
        url = result.url
        checks = CheckForm(request.form, obj=result)
    else:  # если заводится новая проверка
        if candidate.status == STATUS['new'] or candidate.status == STATUS['result']:  # проверяем статус
            url = os.path.join(rf'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\Персонал\Персонал-2\\',
                               candidate.full_name[0], f"{str(candidate.id)} - {candidate.full_name}",
                               datetime.datetime.now().strftime('%Y-%m-%d'))
            # os.makedirs(url)  #  создаем папку для материалов проверки
            db.session.add(Check(officer=current_user.username, url=url, check_id=cand_id))
            db.session.commit()  # формируем черновую запись проверки, записываем в БД путь, дату
            return redirect(url_for('route.check', cand_id=cand_id, check_id=cand_id))
        else:
            flash(Markup("Анкета взята в работу и еще не закончена"))
            return redirect(url_for('route.index'))
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
        for k, v in chk.items():
            setattr(result, k, v)
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
    return render_template('check.html', form=checks, check_url=url)


@bpr.route('/registr/<int:cand_id>/<int:check_id>', methods=('GET', 'POST'))  # финальное решение по кандидату
@login_required  # согласование кандидата
def registr(cand_id, check_id):
    registry = RegistrForm(request.form)  # загружаем форму согласования
    if registry.validate_on_submit() and request.method == 'POST':
        reg = dict(supervisor=current_user,
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
            flash(Markup("Решение успешно отправлено"))
            candidate.status = STATUS['result']  # меняем статус в таблице на "Решение принято"
            db.session.commit()
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
                                officer=current_user,
                                date_pfo=pfo.date_pfo.data,
                                poligraf_id=cand_id))
        db.session.commit()
        candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
        candidate.status = STATUS['finish']
        db.session.commit()
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
