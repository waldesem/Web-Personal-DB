import datetime
from datetime import date
import os

from flask import Flask
from flask import flash, Markup, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from sqlalchemy import func

from models import *
import forms
from excelfile import ExcelFile


basedir = os.path.abspath(os.path.dirname(__file__))
secret_key = os.urandom(20).hex()  # generate SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'personal.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@server/dbname'
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost/dbname"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = datetime.timedelta(days=30)

db = SQLAlchemy(app)
# migrate = Migrate()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к базе данных"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    user = db.session.query(Users).select_from(Users).filter_by(id=user_id).first()
    return user


@app.route("/login", methods=["POST", "GET"])
def login():
    user_form = forms.LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        user_form = forms.LoginForm(request.form)
        username = user_form.username.data
        password = user_form.password.data
        rmb = user_form.remember.data
        user = db.session.query(Users).select_from(Users).filter_by(username=username).first()
        if db.session.query(Users).select_from(Users).filter_by(username=username, password=password):
            login_user(user, remember=rmb)
            return redirect(url_for('index'))
        else:
            flash("Неверная пара логин/пароль", "error")
    return render_template("login.html", form=user_form)


@app.route('/logout')  # create func for logout
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=('GET', 'POST'))  # create func for main page, query in db for last dates
@login_required
def index():
    form_search = forms.SearchForm(request.form)
    results = db.session.query(Candidate, Check).select_from(Candidate).join(Check, isouter=True). \
        order_by(Check.date_check.desc()).limit(9).all()
    return render_template('index.html', results=results, form=form_search)


@app.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    form_search = forms.SearchForm(request.form)
    if request.method == 'POST':
        search_by = dict(full_name=request.form.get('full_name'), birthday=request.form.get('birthday'))
        items = {k: v for (k, v) in search_by.items() if v}
        print(items)
        results = db.session.query(Candidate, Check).select_from(Candidate). \
            filter_by(**items).join(Check, isouter=True). \
            order_by(Check.date_check.desc()).all()
        return render_template('index.html', results=results, form=form_search)


@app.route('/profile/<c_id>', methods=('GET', 'POST'))
@login_required
def profile(c_id):
    cand_id = None
    if request.method == 'POST':
        cand_id = request.form.get('id')
    elif request.method == 'GET':
        cand_id = c_id
    candidate = db.session.query(Candidate).select_from(Candidate).filter_by(id=cand_id).first()
    checks = db.session.query(Check).select_from(Check).filter_by(check_id=candidate.id).all()
    inquries = db.session.query(Inquery).select_from(Inquery).filter_by(iquery_id=candidate.id).all()
    registries = db.session.query(Registr).select_from(Registr).filter_by(registry_id=candidate.id).all()
    return render_template('profile.html', candidate=candidate,
                           checks=checks, inquries=inquries, registries=registries)


@app.route('/resume/<int:cand_id>', methods=('GET', 'POST'))
@login_required
def resume(cand_id):
    result = None
    if str(cand_id) == '9999999':
        candidate = forms.ResumeForm(request.form)
    elif str(cand_id) == '8888888':
        candidate = forms.ResumeForm(request.form, obj=Candidate(**ExcelFile.excel))
    else:
        result = db.session.query(Candidate).select_from(Candidate).filter_by(id=cand_id).first()
        candidate = forms.ResumeForm(request.form, obj=result)
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
        if str(cand_id) != '9999999' and str(cand_id) != '8888888':
            for k, v in cand.items():
                setattr(result, k, v)
                db.session.commit()
            return redirect(url_for('profile', c_id=cand_id))

        else:
            cnd = db.session.query(Candidate).select_from(Candidate).filter_by(full_name=candidate.full_name.data,
                                                                               birthday=candidate.birthday.data).first()
            if cnd is not None:
                message = Markup('Такая запись уже существует')
                flash(message)
                return redirect(url_for('profile', c_id=cnd.id))
            else:
                value = Candidate(**cand)
                db.session.add(value)
                db.session.commit()
            return redirect(url_for('profile', c_id=value.id))
    return render_template('resume.html', form=candidate)


@app.route('/upload/', methods=('GET', 'POST'))
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        ExcelFile(file)
        return redirect(url_for('resume', cand_id='8888888'))


@app.route('/check/<int:cand_id>/<int:check_id>', methods=('GET', 'POST'))
@login_required
def check(cand_id, check_id):
    result = None
    if str(check_id) == '0':
        checks = forms.CheckForm(request.form)
    else:
        result = db.session.query(Check).select_from(Check).filter_by(id=check_id).first()
        checks = forms.CheckForm(request.form, obj=result)
    if checks.validate_on_submit() and request.method == 'POST':
        ch = dict(check_work_place=checks.check_work_place.data,
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
        if str(check_id) == '0':
            db.session.add(Check(**ch))
            db.session.commit()
        else:
            for k, v in ch.items():
                setattr(result, k, v)
                db.session.commit()
        return redirect(url_for('index'))
    return render_template('check.html', form=checks)


@app.route('/inquiry/<int:cand_id>', methods=('GET', 'POST'))
@login_required
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


@app.route('/info', methods=('GET', 'POST'))
@login_required
def info():
    if request.method == 'GET':
        results = db.session.query(Registr.fin_decision, func.count(Registr.fin_decision)). \
            group_by(Registr.fin_decision).filter(Registr.final_date.like('%2022%')).all()
        return render_template('info.html', results=results)


if __name__ == "__main__":
    app.run(debug=True)


# export FLASK_APP=app
# export FLASK_ENV=development
