from datetime import date
import re

from flask import Flask, flash, Markup
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import openpyxl

import forms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/semenenko/MyProjects/personal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Personal(db.Model):  # create model DB for personal date, checks, inquries and for registry
    __abstract__ = True


class Candidate(Personal):
    """ Create model for candidates dates"""

    __tablename__ = 'candidates'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    staff = db.Column(db.Text)
    department = db.Column(db.Text)
    full_name = db.Column(db.Text, index=True)
    last_name = db.Column(db.Text)
    birthday = db.Column(db.Text)
    birth_place = db.Column(db.Text)
    country = db.Column(db.Text)
    series_passport = db.Column(db.Text)
    number_passport = db.Column(db.Text)
    date_given = db.Column(db.Text)
    snils = db.Column(db.Text)
    inn = db.Column(db.Text)
    reg_address = db.Column(db.Text)
    live_address = db.Column(db.Text)
    phone = db.Column(db.Text)
    email = db.Column(db.Text)
    education = db.Column(db.Text)
    # upd_date = db.Column(db.Text)
    checks = db.relationship('Check', backref='candidates')
    iqueries = db.relationship('Inquery', backref='candidates')
    registries = db.relationship('Registr', backref='candidates')


class Check(Personal):
    """ Create model for candidates checks"""

    __tablename__ = 'checks'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    # staff = db.Column(db.Text)
    # department = db.Column(db.Text)
    check_work_place = db.Column(db.Text)
    check_passport = db.Column(db.Text)
    check_debt = db.Column(db.Text)
    check_bankruptcy = db.Column(db.Text)
    check_bki = db.Column(db.Text)
    check_affiliation = db.Column(db.Text)
    check_internet = db.Column(db.Text)
    check_cronos = db.Column(db.Text)
    check_cross = db.Column(db.Text)
    resume = db.Column(db.Text)
    date_check = db.Column(db.Text)
    officer = db.Column(db.Text)
    check_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Inquery(Personal):
    """ Create model for candidates inqueries"""

    __tablename__ = 'iqueries'
    # __tablename__ = 'inqueries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    staff = db.Column(db.Text)
    period = db.Column(db.Text)
    info = db.Column(db.Text)
    firm = db.Column(db.Text)
    # source = db.Column(db.Text)
    date_inq = db.Column(db.Text)
    iquery_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Registr(Personal):
    """ Create model for registry of candidates"""

    __tablename__ = 'registries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    checks = db.Column(db.Text)
    recruiter = db.Column(db.Text)
    fin_decision = db.Column(db.Text)
    final_date = db.Column(db.Text)
    url = db.Column(db.Text)
    registry_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Users(Personal):
    """ Create model for registry of candidates"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    role = db.Column(db.Text)


# @app.route("/login", methods=["POST", "GET"])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = forms.LoginForm()
#     if form.validate_on_submit():
#         user = dbase.getUserByEmail(form.email.data)
#         if user and check_password_hash(user['psw'], form.psw.data):
#             userlogin = UserLogin().create(user)
#             rm = form.remember.data
#             login_user(userlogin, remember=rm)
#             return redirect(request.args.get("next") or url_for("profile"))
#         flash("Неверная пара логин/пароль", "error")
#     return render_template("login.html", menu=dbase.getMenu(), title="Авторизация", form=form)


@app.route('/', methods=('GET', 'POST'))  # create func for main page, query in db for last dates
def index():
    results = db.session.query(Candidate, Check).select_from(Candidate).join(Check, isouter=True).\
        order_by(Check.date_check.desc()).limit(9).all()
    return render_template('index.html', results=results)


@app.route('/search', methods=('GET', 'POST'))
def search():
    results = []
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        birthday = request.form.get('birthday')
        cnd = Candidate.query.filter_by(full_name=full_name, birthday=birthday).first()
        chk = Check.query.filter_by(check_id=cnd.id).all()
        inq = Inquery.query.filter_by(iquery_id=cnd.id).all()
        reg = Registr.query.filter_by(registry_id=cnd.id).all()
        results.extend([cnd, chk, inq, reg])
    return render_template('search.html', results=results)


@app.route('/resume/<int:cand_id>', methods=('GET', 'POST'))
def resume(cand_id):
    results = Candidate.query.get(cand_id)
    candidate = forms.ResumeForm(request.form, obj=results)
    if candidate.validate_on_submit() and request.method == 'POST':
        cand = dict(staff=candidate.staff.data,
                    department=candidate.department.data,
                    full_name=candidate.full_name.data,
                    last_name=candidate.last_name.data,
                    birthday=candidate.birthday.data,
                    birth_place=candidate.birth_place.data,
                    country=candidate.country.data,
                    series_passport=candidate.series_passport.data,
                    number_passport=candidate.number_passport.data,
                    date_given=candidate.date_given.data,
                    snils=candidate.snils.data,
                    inn=candidate.inn.data,
                    reg_address=candidate.reg_address.data,
                    live_address=candidate.live_address.data,
                    phone=candidate.phone.data,
                    email=candidate.email.data,
                    education=candidate.education.data)
        for k, v in cand.items():
            setattr(results, k, v)
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('resume.html', form=candidate)


@app.route('/check/<int:cand_id>', methods=('GET', 'POST'))
def check(cand_id):
    checks = forms.CheckForm(request.form)
    if checks.validate_on_submit() and request.method == 'POST':
        ch = Check(check_work_place=checks.check_work_place.data,
                   check_passport=checks.check_passport.data,
                   check_debt=checks.check_debt.data,
                   check_bankruptcy=checks.check_bankruptcy.data,
                   check_bki=checks.check_bki.data,
                   check_affiliation=checks.check_affiliation.data,
                   check_internet=checks.check_internet.data,
                   check_cronos=checks.check_cronos.data,
                   check_cross=checks.check_cross.data,
                   resume=checks.resume.data,
                   officer=checks.officer.data,
                   date_check=date.today().strftime('%Y-%m-%d'),
                   check_id=cand_id)
        db.session.add(ch)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('check.html', form=checks)


@app.route('/inquiry/<int:cand_id>', methods=('GET', 'POST'))
def inquiry(cand_id):
    iqueries = forms.InquiryForm(request.form)
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


@app.route('/create/', methods=('GET', 'POST'))
def create():   # create new candidate
    candidate = forms.CreateForm(request.form)  # create form
    if candidate.validate_on_submit() and request.method == 'POST':
        cnd = Candidate.query.filter_by(full_name=candidate.full_name.data, birthday=candidate.birthday.data).first()
        if cnd.id is not None:
            flash(Markup(f'Такая запись уже существует <a href="/resume/{cnd.id}" '
                         f'class="alert-link">Открыть ID {cnd.id}</a>'))
        else:
            res = Candidate(staff=candidate.staff.data,
                            department=candidate.department.data,
                            full_name=candidate.full_name.data,
                            last_name=candidate.last_name.data,
                            birthday=candidate.birthday.data,
                            birth_place=candidate.birth_place.data,
                            country=candidate.country.data,
                            series_passport=candidate.series_passport.data,
                            number_passport=candidate.number_passport.data,
                            date_given=candidate.date_given.data,
                            snils=candidate.snils.data,
                            inn=candidate.inn.data,
                            reg_address=candidate.reg_address.data,
                            live_address=candidate.live_address.data,
                            phone=candidate.phone.data,
                            email=candidate.email.data,
                            education=candidate.education.data)
            db.session.add(res)
            db.session.flush()
            chck = Check(check_work_place=candidate.check_work_place.data,
                         check_passport=candidate.check_passport.data,
                         check_debt=candidate.check_debt.data,
                         check_bankruptcy=candidate.check_bankruptcy.data,
                         check_bki=candidate.check_bki.data,
                         check_affiliation=candidate.check_affiliation.data,
                         check_internet=candidate.check_internet.data,
                         check_cronos=candidate.check_cronos.data,
                         check_cross=candidate.check_cross.data,
                         resume=candidate.resume.data,
                         officer=candidate.officer.data,
                         date_check=date.today().strftime('%Y-%m-%d'),
                         check_id=res.id)
            db.session.add(chck)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template("create.html", form=candidate)


@app.route('/create', methods=('GET', 'POST'))
def upload():
    file = request.files['file']
    wb = openpyxl.load_workbook(file, keep_vba=True)
    sheet = wb.worksheets[0]
    res = {'staff': sheet['C3'].value,
           'department': sheet['D3'].value,
           'full_name': sheet['K3'].value,
           'last_name': sheet['S3'].value,
           'birthday': data_check(sheet['L3'].value),
           'birth_place': sheet['M3'].value,
           'country': sheet['T3'].value,
           'series_passport': sheet['P3'].value,
           'number_passport': sheet['Q3'].value,
           'date_given': data_check(sheet['R3'].value),
           'snils': sheet['U3'].value,
           'inn': sheet['V3'].value,
           'reg_address': sheet['N3'].value,
           'live_address': sheet['O3'].value,
           'phone': sheet['Y3'].value,
           'email': sheet['Z3'].value,
           'education': sheet['X3'].value}
    wb.close()
    candidate = forms.CreateForm(**res)

    if candidate.validate_on_submit() and request.method == 'POST':
        res = Candidate(staff=candidate.staff.data,
                        department=candidate.department.data,
                        full_name=candidate.full_name.data,
                        last_name=candidate.last_name.data,
                        birthday=candidate.birthday.data,
                        birth_place=candidate.birth_place.data,
                        country=candidate.country.data,
                        series_passport=candidate.series_passport.data,
                        number_passport=candidate.number_passport.data,
                        date_given=candidate.date_given.data,
                        snils=candidate.snils.data,
                        inn=candidate.inn.data,
                        reg_address=candidate.reg_address.data,
                        live_address=candidate.live_address.data,
                        phone=candidate.phone.data,
                        email=candidate.email.data,
                        education=candidate.education.data)
        db.session.add(res)
        db.session.flush()
        chck = Check(check_work_place=candidate.check_work_place.data,
                     check_passport=candidate.check_passport.data,
                     check_debt=candidate.check_debt.data,
                     check_bankruptcy=candidate.check_bankruptcy.data,
                     check_bki=candidate.check_bki.data,
                     check_affiliation=candidate.check_affiliation.data,
                     check_internet=candidate.check_internet.data,
                     check_cronos=candidate.check_cronos.data,
                     check_cross=candidate.check_cross.data,
                     resume=candidate.resume.data,
                     officer=candidate.officer.data,
                     date_check=date.today().strftime('%Y-%m-%d'),
                     check_id=res.id)
        db.session.add(chck)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html', form=candidate)


def data_check(val):  # check string format date
    if isinstance(val, str):
        data = re.findall(r'\d{2}.\d{2}.\d{4}', val)
        if len(data):
            view = ' '.join(data).strip()
            str_date = f'{view[-4:]}-{view[-7:-5]}-{view[:2]}'
        else:
            str_date = val.strip()
    else:
        str_date = val
    return str_date


@app.route('/info', methods=('GET', 'POST'))
def info():
    if request.method == 'POST':
        results = Registr.query(Registr.fin_decision, Registr.final_date).filter_by(final_date='%-%-2023').count()
        return render_template('info', results=results)


if __name__ == "__main__":
    app.run(debug=True)
