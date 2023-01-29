import os
from datetime import date
from getpass import getuser
import json

import requests
from sqlalchemy import func
from flask import Markup, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename

from app.forms import form
from app.models.model import *
from app.utils.excelfile import ExcelFile
from . import bp_routes
from app.main.api import STATUS, TODAY


@bp_routes.route("/login", methods=["POST", "GET"])  # вход пользователя в систему
def login():  # пароль и логин берутся из таблицы Users куда прописываются через интерфейс БД
    user_form = form.LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    if request.method == "POST":
        user_form = form.LoginForm(request.form)
        username = user_form.username.data
        password = user_form.password.data
        rmb = user_form.remember.data  # запомнить логин-пароль
        user = db.session.query(Users).select_from(Users).filter_by(username=username).first()
        if db.session.query(Users).select_from(Users).filter_by(username=username, password=password):
            login_user(user, remember=rmb)
            return redirect(url_for('routes.index'))
        else:
            flash("Неверная пара логин/пароль", "error")
    return render_template("login.html", form=user_form)


@login_required
@bp_routes.route('/logout')
def logout():  # выход пользователя из системы
    logout_user()
    return redirect(url_for('routes.login'))


@login_required  # загрузка стартовой страницы (по умолчанию) либо страницы пользователя
@bp_routes.route('/<username>', methods=('GET', 'POST'))
def index(username):  # загрузка страницы пользователя с фильтром статуса который исключает оконченные проверки
    if username and request.method == 'GET':  # имя пользователя принимается из сеанса
        form_search = form.SearchForm()
        results = db.session.query(Candidate, Users).select_from(Candidate).order_by(Candidate.status). \
            filter(Candidate.status != STATUS['finish'], Candidate.status != STATUS['result']). \
            join(Check, isouter=True).filter(officer=username).all()
        return render_template('index.html', results=results, form=form_search)
    form_search = form.SearchForm()  # загрузка страницы с фильтром статуса который исключает оконченные проверки
    results = db.session.query(Candidate).select_from(Candidate). \
        order_by(Candidate.status != STATUS['finish'], Candidate.status != STATUS['result']).all()
    return render_template('index.html', results=results, form=form_search)


@login_required  # функция поиска по ФИО и (при необходимости) по дате рождения
@bp_routes.route('/search', methods=('GET', 'POST'))
def search():
    form_search = form.SearchForm(request.form)
    if request.method == 'POST':
        search_by = dict(full_name=request.form.get('full_name'), birthday=request.form.get('birthday'))
        items = {k: v for (k, v) in search_by.items() if v}  # проверка, если одно из полей не заполнено
        results = db.session.query(Candidate).select_from(Candidate). \
            filter_by(**items).order_by(Candidate.update_date.desc()).all()
        return render_template('index.html', results=results, form=form_search)


@login_required
@bp_routes.route('/profile/<cand_id>', methods=('GET', 'POST'))  # вся информация  о кандидате
def profile(cand_id):
    if request.method == 'GET' or request.method == 'POST':
        candidate = db.session.query(Candidate).select_from(Candidate).filter_by(id=cand_id).first()
        checks = db.session.query(Check).select_from(Check).filter_by(check_id=cand_id).all()
        pfo = db.session.query(Poligraf).select_from(Poligraf).filter_by(pfo_id=cand_id).all()
        invs = db.session.query(Investigation).select_from(Investigation).filter_by(inv_id=cand_id).all()
        inquries = db.session.query(Inquery).select_from(Inquery).filter_by(iquery_id=cand_id).all()
        registries = db.session.query(Registr).select_from(Registr).filter_by(registry_id=cand_id).all()
        return render_template('profile.html', candidate=candidate,
                               checks=checks, inquries=inquries, registries=registries, pfos=pfo, invs=invs)


@login_required
@bp_routes.route('/resume/<cand_id>', methods=('GET', 'POST'))
def resume(cand_id):
    result = None
    if cand_id is 'create':
        candidate = form.ResumeForm(request.form)
    elif cand_id is 'upload':
        candidate = form.ResumeForm(request.form, obj=Candidate(**ExcelFile.excel))
    else:
        result = db.session.query(Candidate).select_from(Candidate).filter_by(id=cand_id).first()
        candidate = form.ResumeForm(request.form, obj=result)
    if candidate.validate_on_submit() and request.method == 'POST':
        cand = dict(full_name=candidate.full_name.data,
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
                    addition=candidate.addition.data,
                    update_date=TODAY,
                    status=STATUS['new'])
        if cand_id is not 'create' and cand_id is not 'upload':
            for k, v in cand.items():
                setattr(result, k, v)
                db.session.commit()
            return redirect(url_for('routes.check', cand_id=cand_id))
        else:
            cnd = db.session.query(Candidate).select_from(Candidate).filter_by(full_name=candidate.full_name.data,
                                                                               birthday=candidate.birthday.data).first()
            if cnd is not None:
                message = Markup('Такая запись уже существует')
                flash(message)
                return redirect(url_for('routes.profile', cand_id=cnd.id))
            else:
                value = Candidate(**cand)
                db.session.add(value)
                db.session.commit()
                return redirect(url_for('routes.check', cand_id=value.id))
    return render_template('resume.html', form=candidate)


@login_required
@bp_routes.route('/upload/', methods=('GET', 'POST'))  # загрузка анкеты из файла Excel
def upload():
    if request.method == 'POST':
        file = request.files['file']
        ExcelFile(file)
        file.save(f'/path/{secure_filename(file.filename)}')
        return redirect(url_for('routes.resume', cand_id='upload'))


@login_required  # форма проверки кандидата
@bp_routes.route('/check/<int:cand_id>/<int:check_id>', methods=('GET', 'POST'))
def check(cand_id, check_id=0):
    candidate = db.session.query(Candidate).select_from(Candidate).filter_by(id=cand_id).first()
    setattr(candidate, candidate.status, STATUS['active'])  # меняем статус анкеты - Проверка
    if str(check_id) == 0:  # если заводится новая проверка, а не редактирование
        url = rf'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\Персонал\Персонал-2\{candidate.full_name[0]}\
                    \{candidate.id} - {candidate.full_name}'
        os.mkdir(os.path.join(url, TODAY))  # создаем папку для хранения анкет и материалов проверки
        start_check = Check()
        start_check.officer = getuser()
        start_check.url = url
        start_check.date_check = TODAY
        db.session.add(Check(start_check))
        db.session.commit()  # формируем черновую запись проверки, записываем в БД путь, дату и сотрудника СБ
        result = db.session.query(Check).select_from(Check).filter_by(id=start_check.id).first()
        checks = form.CheckForm(request.form, obj=result)  # передаем данные в форму проверки
    else:  # если редактируется старая проверка
        result = db.session.query(Check).select_from(Check).filter_by(id=check_id).first()
        result.officer = getuser()
        setattr(result, result.officer, getuser())
        db.session.commit()
        checks = form.CheckForm(request.form, obj=result)
    if checks.validate_on_submit() and request.method == 'POST':
        ch = dict(staff=checks.staff.data,
                  department=checks.department.data,
                  check_work_place=checks.check_work_place.data,
                  check_passport=checks.check_passport.data,
                  check_debt=checks.check_debt.data,
                  check_bankruptcy=checks.check_bankruptcy.data,
                  check_bki=checks.check_bki.data,
                  check_affiliation=checks.check_affiliation.data,
                  check_terrorist=checks.check_terrorist.data,
                  check_internet=checks.check_internet.data,
                  check_cronos=checks.check_cronos.data,
                  check_cross=checks.check_cross.data,
                  check_addition=checks.check_addition.data,
                  pfo=checks.pfo.data,
                  resume=checks.resume.data,
                  officer=getuser(),
                  date_check=TODAY,
                  url=checks.url.data,
                  check_id=cand_id)
        for k, v in ch.items():
            setattr(result, k, v)
            db.session.commit()
        if ch['pfo'] is False:
            setattr(candidate, candidate.status, STATUS['finish'])
        else:
            setattr(candidate, candidate.status, STATUS['pfo_start'])
        return redirect(url_for('routes.profile', cand_id=cand_id))
    return render_template('check.html', form=checks, candidate=candidate)


@login_required
@bp_routes.route('/poligraf/<int:cand_id>', methods=('GET', 'POST'))  # результаты проверки на полиграфе
def poligraf(cand_id):
    pfo = form.PoligrafForm(request.form)
    if pfo.validate_on_submit() and request.method == 'POST':
        pfo_val = Poligraf(staff=poligraf.info.data,
                           period=date.today().strftime('%Y-%m-%d'),
                           info=poligraf.officer.data,
                           pfo_id=cand_id)
        db.session.add(pfo_val)
        db.session.commit()
        candidate = db.session.query(Candidate).select_from(Candidate).filter_by(id=cand_id).first()
        setattr(candidate, candidate.status, STATUS['finish'])
        return redirect(url_for('routes.index'))
    return render_template('poligraf.html', form=pfo)


@login_required
@bp_routes.route('/investigation/<int:cand_id>', methods=('GET', 'POST'))  # результаты служебной проверки
def investigation(cand_id):
    inv = form.InvestigationForm(request.form)
    if inv.validate_on_submit() and request.method == 'POST':
        inv = Investigation(info=inv.info.data,
                            source=inv.source.data,
                            date_inv=inv.date_inv.data,
                            inv_id=cand_id)
        db.session.add(inv)
        db.session.commit()
        return redirect(url_for('routes.index'))
    return render_template('investigation.html', form=inv)


@login_required
@bp_routes.route('/inquiry/<int:cand_id>', methods=('GET', 'POST'))  # дополнительная информация о сотруднике
def inquiry(cand_id):
    iqueries = form.InquiryForm(request.form)
    if iqueries.validate_on_submit() and request.method == 'POST':
        inq = Inquery(staff=iqueries.staff.data,
                      period=iqueries.period.data,
                      info=iqueries.info.data,
                      firm=iqueries.firm.data,
                      date_inq=date.today().strftime('%Y-%m-%d'),
                      iquery_id=cand_id)
        db.session.add(inq)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('inquiry.html', form=iqueries)


@login_required     # согласование кандидата
@bp_routes.route('/registr/<int:cand_id>', methods=('GET', 'POST'))  # финальное решение по кандидату
def registr(cand_id):
    registry = form.RegistrForm(request.form)
    if registry.validate_on_submit() and request.method == 'POST':
        reg = Registr(supervisor=getuser(),
                      checks=registry.checks.data,
                      fin_decision=registry.fin_decision.data,
                      submit=date.today().strftime('%Y-%m-%d'),
                      iquery_id=cand_id)
        db.session.add(reg)
        db.session.commit()
        url = "http://localhost:8080"
        data = jsonify(reg)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        resp = requests.post(url=url, data=data, headers=headers)
        resp.raise_for_status()
        if json.loads(resp.json())['request'] == 'successful':
            message = Markup("Анкета успешно отправлена")
            flash(message)
            cnd = db.session.query(Candidate).select_from(Candidate).filter_by(id=cand_id).first()
            setattr(cnd, cnd.status, STATUS['result'])  # меняем статус в таблице "кандидаты" на "Решение принято"
            return redirect(url_for('index'))
        else:
            message = Markup("Отправка анкеты не удалась попробуйте еще раз позднее")
            flash(message)
    candidate = db.session.query(Candidate).select_from(Candidate).filter_by(id=cand_id).first()
    checks = db.session.query(Check).select_from(Check).filter_by(check_id=cand_id). \
        order_by(Check.check_id.desc()).first()
    return render_template('registr.html', form=registry, candidate=candidate, checks=checks)


@login_required
@bp_routes.route('/info', methods=('GET', 'POST'))  # create statistic info
def info():
    if request.method == 'GET':
        results = db.session.query(Registr.fin_decision, func.count(Registr.fin_decision)). \
            group_by(Registr.fin_decision).filter(Registr.final_date.like('%2022%')).all()
        return render_template('info.html', results=results)
    if request.method == 'POST':
        month_year = form.InfoForm(request.form)
        results = db.session.query(Registr.fin_decision, func.count(Registr.fin_decision)). \
            group_by(Registr.fin_decision).filter(Registr.final_date.like(f'%{month_year.month.data}-\
                {month_year.year.data}%')).all()
        return render_template('info.html', results=results)
