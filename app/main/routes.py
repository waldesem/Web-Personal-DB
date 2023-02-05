from sqlalchemy import func
from flask import Markup, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from app.forms import form
from app.models.model import *
from app.utils.excelfile import ExcelFile
from . import bp_routes
from ..utils.extensions import STATUS, TODAY, send_json, create_folder


@bp_routes.route("/login", methods=["POST", "GET"])  # вход пользователя в систему
def login():  # пароль и логин берутся из таблицы Users куда прописываются через интерфейс БД
    user_form = form.LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    if request.method == "POST":
        user_form = form.LoginForm(request.form)
        username = user_form.username.data
        password = user_form.password.data
        rmb = user_form.remember.data  # сохранить логин-пароль для сеанса
        user = db.session.query(Users).select_from(Users).filter_by(username=username).first()
        if db.session.query(Users).select_from(Users).filter_by(username=username, password=password).first():
            login_user(user, remember=rmb)
            return redirect(url_for('routes.index'))
        else:
            flash("Неверная пара логин/пароль", "error")
    return render_template("login.html", form=user_form)


@bp_routes.route('/logout')
@login_required
def logout():  # выход пользователя из системы
    logout_user()
    return redirect(url_for('routes.login'))


@bp_routes.route('/', methods=('GET', 'POST'))
@login_required  # загрузка стартовой страницы
def index():
    form_search = form.SearchForm()  # загрузка страницы новых кандидатови тех, что находятся в работе
    results = db.session.query(Candidate).filter(Candidate.status != STATUS['result']). \
        order_by(Candidate.status.desc()).all()
    return render_template('index.html', results=results, form=form_search)


@bp_routes.route('/officer', methods=('GET', 'POST'))
@login_required
def officer():  # загрузка страницы пользователя со списком кандидатов которые находятся у него в
    form_search = form.SearchForm()
    results = db.session.query(Candidate).filter(Candidate.status != STATUS['result']). \
        join(Check, isouter=False).filter_by(officer=current_user.username).order_by(Candidate.status.desc()).all()
    return render_template('index.html', results=results, form=form_search)


@bp_routes.route('/search', methods=('GET', 'POST'))
@login_required  # функция поиска по ФИО и (при необходимости) по дате рождения
def search():
    form_search = form.SearchForm(request.form)
    if request.method == 'POST':
        search_by = dict(full_name=request.form.get('full_name'), birthday=request.form.get('birthday'))
        items = {k: v for (k, v) in search_by.items() if v}  # проверка, какие поля заполнены
        results = db.session.query(Candidate).filter_by(**items).all()
        return render_template('index.html', results=results, form=form_search)


@bp_routes.route('/profile/<cand_id>', methods=('GET', 'POST'))  # вся информация  о кандидате
@login_required
def profile(cand_id):
    if request.method == 'GET' or 'POST':
        candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
        checks = db.session.query(Check).filter_by(check_id=cand_id).all()
        pfo = db.session.query(Poligraf).filter_by(poligraf_id=cand_id).all()
        invs = db.session.query(Investigation).filter_by(inv_id=cand_id).all()
        inquries = db.session.query(Inquery).filter_by(iquery_id=cand_id).all()
        registries = db.session.query(Registr).filter_by(registry_id=cand_id).all()
        return render_template('profile.html', candidate=candidate, checks=checks, inquries=inquries,
                               registries=registries, pfos=pfo, invs=invs)


@bp_routes.route('/resume/<int:cand_id>', methods=('GET', 'POST'))  # добавляем или редактируем анкету
@login_required
def resume(cand_id):
    result = db.session.query(Candidate).filter_by(id=cand_id).first()  # запрашиваем анкету
    file = form.FileForm()
    if cand_id == 9999999:  # создаем новую анкету вручную
        candidate = form.ResumeForm(request.form)
    elif cand_id == 8888888:  # загружаем анкету из файла Excel
        candidate = form.ResumeForm(request.form, obj=ExcelFile.res)
    else:  # редактируем анкету
        candidate = form.ResumeForm(request.form, obj=result)
    if candidate.validate_on_submit() and request.method == 'POST':
        cand = dict(region=candidate.region.data,
                    full_name=candidate.full_name.data,
                    last_name=candidate.last_name.data,
                    birthday=candidate.birthday.data,
                    birth_place=candidate.birth_place.data,
                    country=candidate.country.data,
                    series_passport=candidate.series_passport.data,
                    number_passport=candidate.number_passport.data,
                    agency=candidate.agency.data,
                    date_given=candidate.date_given.data,
                    snils=candidate.snils.data,
                    inn=candidate.inn.data,
                    reg_address=candidate.reg_address.data,
                    live_address=candidate.live_address.data,
                    phone=candidate.phone.data,
                    email=candidate.email.data,
                    education=candidate.education.data,
                    workplace_1=candidate.workplace_1.data,
                    workplace_2=candidate.workplace_2.data,
                    workplace_3=candidate.workplace_3.data,
                    addition=candidate.addition.data,
                    update_date=TODAY,
                    status=STATUS['new'])
        if cand_id != 9999999 and cand_id != 8888888:  # перезаписываем данные после редактирования
            for k, v in cand.items():
                setattr(result, k, v)
                db.session.commit()
            return redirect(url_for('routes.index', cand_id=cand_id))
        else:
            result = db.session.query(Candidate).filter_by(full_name=cand['full_name'],
                                                           birthday=cand['birthday']).first()  # запрашиваем анкету
            print(result)
            if result:  # проверка существования такой же анкеты
                message = Markup(f'Такая запись уже существует')
                flash(message)
            else:
                db.session.add(Candidate(**cand))  # добавляем анкету в БД
                db.session.commit()
                return redirect(url_for('routes.index'))
    return render_template('resume.html', form=candidate, file=file)


@bp_routes.route('/upload', methods=('GET', 'POST'))  # загрузка анкеты из файла Excel
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        ExcelFile(file)
        return redirect(url_for('routes.resume', cand_id=8888888))


@bp_routes.route('/check/<int:cand_id>/<int:check_id>', methods=('GET', 'POST'))
@login_required  # форма проверки кандидата
def check(cand_id, check_id):
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    candidate.status = STATUS['active']  # меняем статус анкеты - Проверка
    db.session.commit()
    if check_id:  # если редактируется старая проверка
        result = db.session.query(Check).filter_by(id=check_id).first()
        url = result.url
        checks = form.CheckForm(request.form, obj=result)
    else:  # если заводится новая проверка
        url = "create_folder(candidate)"    # раскомментировать строку, создаем папку для материалов
        db.session.add(Check(officer=current_user.username, url=url, check_id=cand_id))
        db.session.commit()  # формируем черновую запись проверки, записываем в БД путь, дату
        return redirect(url_for('routes.check', cand_id=cand_id, check_id=cand_id))
    if checks.validate_on_submit() and request.method == 'POST':
        chk = dict(staff=checks.staff.data,
                   department=checks.department.data,
                   check_work_place=checks.check_work_place.data,
                   check_passport=checks.check_passport.data,
                   check_debt=checks.check_debt.data,
                   check_bankruptcy=checks.check_bankruptcy.data,
                   check_bki=checks.check_bki.data,
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
                   date_check=TODAY,
                   check_id=cand_id)
        for k, v in chk.items():
            setattr(result, k, v)
            db.session.commit()
        if chk['resume'] == 'Сохранить':
            return redirect(url_for('routes.index'))
        else:
            if chk['pfo']:  # если поставлена отметка pfo
                candidate.status = STATUS['pfo_start']
                db.session.commit()
            else:
                candidate.status = STATUS['finish']
                db.session.commit()
            return redirect(url_for('routes.index'))
    return render_template('check.html', form=checks, check_url=url)


@bp_routes.route('/poligraf/<int:cand_id>', methods=('GET', 'POST'))  # результаты проверки на полиграфе
@login_required
def poligraf(cand_id):
    pfo = form.PoligrafForm(request.form)
    if pfo.validate_on_submit() and request.method == 'POST':
        db.session.add(Poligraf(theme=pfo.theme.data,
                                results=pfo.results.data,
                                officer=current_user.username,
                                date_pfo=pfo.date_pfo.data,
                                poligraf_id=cand_id))
        db.session.commit()
        candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
        candidate.status = STATUS['finish']
        db.session.commit()
        return redirect(url_for('routes.index'))
    return render_template('poligraf.html', form=pfo)


@bp_routes.route('/investigation/<int:cand_id>', methods=('GET', 'POST'))  # результаты служебной проверки
@login_required
def investigation(cand_id):
    inv = form.InvestigationForm(request.form)
    if inv.validate_on_submit() and request.method == 'POST':
        db.session.add(Investigation(theme=inv.theme.data,
                                     info=inv.info.data,
                                     date_inv=inv.date_inv.data,
                                     inv_id=cand_id))
        db.session.commit()
        return redirect(url_for('routes.index'))
    return render_template('investigation.html', form=inv)


@bp_routes.route('/inquiry/<int:cand_id>', methods=('GET', 'POST'))  # дополнительная информация о сотруднике
@login_required
def inquiry(cand_id):
    iqueries = form.InquiryForm(request.form)
    if iqueries.validate_on_submit() and request.method == 'POST':
        db.session.add(Inquery(info=iqueries.info.data,
                               initiator=iqueries.initiator.data,
                               date_inq=iqueries.date_inq.data,
                               iquery_id=cand_id))
        db.session.commit()
        return redirect(url_for('routes.index'))
    return render_template('inquiry.html', form=iqueries)


@bp_routes.route('/registr/<int:cand_id>', methods=('GET', 'POST'))  # финальное решение по кандидату
@login_required  # согласование кандидата
def registr(cand_id):
    registry = form.RegistrForm(request.form)
    if registry.validate_on_submit() and request.method == 'POST':
        reg = dict(supervisor=current_user.username,
                   marks=registry.marks.data,
                   decision=registry.decision.data,
                   dec_date=TODAY,
                   registry_id=cand_id)
        db.session.add(Registr(**reg))
        db.session.commit()
        candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
        candidate.status = STATUS['result']  # меняем статус в таблице на "Решение принято"
        db.session.commit()
        return redirect(url_for('routes.index'))
        # reg['request_id'] = candidate.request_id
        # url = "http://localhost:8080"
        # resp = send_json(url, reg)  # отправка ответа в виде json файла
        # if resp.json()['request'] == 'successful':
        #     flash(Markup("Анкета успешно отправлена"))
        #     candidate.status = STATUS['result']  # меняем статус в таблице на "Решение принято"
        #     db.session.commit()
        #     return redirect(url_for('routes.index'))
        # else:
        #     flash(Markup("Отправка анкеты не удалась попробуйте еще раз позднее"))
    return render_template('registr.html', form=registry)


@bp_routes.route('/info', methods=('GET', 'POST'))  # create statistic info
@login_required
def info():
    statinfo = form.InfoForm(request.form)
    results = db.session.query(Registr.decision, func.count(Registr.decision)). \
        group_by(Registr.decision).filter(Registr.dec_date.like(f'%{TODAY[:5]}%')).all()
    if statinfo.validate_on_submit() and request.method == 'POST':
        month_year = form.InfoForm(request.form)
        results = db.session.query(Registr.decision, func.count(Registr.decision)). \
            group_by(Registr.decision).filter(Registr.dec_date.like(f'%{month_year.year.data}-'
                                                                    f'{month_year.month.data}%')).all()
        return render_template('info.html', form=statinfo, results=results)
    return render_template('info.html', form=statinfo, results=results)
