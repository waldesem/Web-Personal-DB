from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/semenenko/MyProjects/personal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Personal(db.Model):
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
    checks = db.relationship('Check', backref='candidates')
    iqueries = db.relationship('Inquery', backref='candidates')
    registries = db.relationship('Registr', backref='candidates')


class Check(Personal):
    """ Create model for candidates checks"""

    __tablename__ = 'checks'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
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
    """ Create model for candidates iqueries"""

    __tablename__ = 'iqueries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    staff = db.Column(db.Text)
    period = db.Column(db.Text)
    info = db.Column(db.Text)
    firm = db.Column(db.Text)
    date_inq = db.Column(db.Text)
    iquery_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Registr(Personal):
    """ Create model for candidates iqueries"""

    __tablename__ = 'registries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    checks = db.Column(db.Text)
    recruiter = db.Column(db.Text)
    fin_decision = db.Column(db.Text)
    final_date = db.Column(db.Text)
    url = db.Column(db.Text)
    registry_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


@app.route('/', methods=('GET', 'POST'))
def index():
    results = db.session.query(Candidate,
                               Check).select_from(Candidate).join(Check, isouter=True). \
        order_by(Check.date_check.desc()).limit(5).all()
    return render_template('index.html', results=results)


@app.route('/search/', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        birthday = request.form.get('birthday')
        results = db.session.query(Candidate,
                                   Check,
                                   Inquery,
                                   Registr).select_from(Candidate).filter_by(full_name=full_name,
                                                                             birthday=birthday). \
            join(Check, isouter=True).join(Inquery, isouter=True).join(Registr, isouter=True).all()
        return render_template('search.html', results=results)
    return redirect(url_for('index'))


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        candidate = dict(staff=request.form['staff'],
                         department=request.form['department'],
                         full_name=request.form['full_name'],
                         last_name=request.form['last_name'],
                         birthday=request.form['birthday'],
                         birth_place=request.form['staff'],
                         country=request.form['birth_place'],
                         series_passport=request.form['series_passport'],
                         number_passport=request.form['number_passport'],
                         date_given=request.form['date_given'],
                         snils=request.form['snils'],
                         inn=request.form['inn'],
                         reg_address=request.form['reg_address'],
                         live_address=request.form['live_address'],
                         phone=request.form['phone'],
                         email=request.form['email'],
                         education=request.form['education'])
        cand = Candidate(**candidate)
        db.session.add(cand)
        db.session.flush()

        checks = dict(check_work_place=request.form['staff'],
                      check_passport=request.form['check_passport'],
                      check_debt=request.form['check_debt'],
                      check_bankruptcy=request.form['check_bankruptcy'],
                      check_bki=request.form['check_bki'],
                      check_affiliation=request.form['check_affiliation'],
                      check_internet=request.form['check_internet'],
                      check_cronos=request.form['check_cronos'],
                      check_cross=request.form['check_cronos'],
                      resume=request.form['resume'],
                      date_check=request.form['date_check'],
                      officer=request.form['officer'],
                      check_id=cand.id)
        check = Check(**checks)
        db.session.add(check)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/edit/<int:cand_id>', methods=('GET', 'POST'))
def edit(cand_id):
    results = db.session.query(Candidate, Check, Inquery).select_from(Candidate).filter_by(id=cand_id). \
        join(Check, isouter=True).join(Inquery, isouter=True).all()
    if request.method == 'POST':
        candidate = dict(staff=request.form.get('staff'),
                         department=request.form.get('department'),
                         full_name=request.form.get('full_name'),
                         last_name=request.form.get('last_name'),
                         birthday=request.form.get('birthday'),
                         birth_place=request.form.get('staff'),
                         country=request.form.get('birth_place'),
                         series_passport=request.form.get('series_passport'),
                         number_passport=request.form.get('number_passport'),
                         date_given=request.form.get('date_given'),
                         snils=request.form.get('snils'),
                         inn=request.form.get('inn'),
                         reg_address=request.form.get('reg_address'),
                         live_address=request.form.get('live_address'),
                         phone=request.form.get('phone'),
                         email=request.form.get('email'),
                         education=request.form.get('education'))
        for k, v in candidate.items():
            setattr(results[0].Candidate, k, v)
        db.session.flush()

        checks = dict(check_work_place=request.form.get('check_work_place'),
                      check_passport=request.form.get('check_passport'),
                      check_debt=request.form.get('check_debt'),
                      check_bankruptcy=request.form.get('check_bankruptcy'),
                      check_bki=request.form.get('check_bki'),
                      check_affiliation=request.form.get('check_affiliation'),
                      check_internet=request.form.get('check_internet'),
                      check_cronos=request.form.get('check_cronos'),
                      check_cross=request.form.get('check_cronos'),
                      resume=request.form.get('resume'),
                      date_check=request.form.get('date_check'),
                      officer=request.form.get('officer'),
                      check_id=cand_id)
        if any(checks.items()) is not None:
            check = Check(**checks)
            db.session.add(check)
            db.session.flush()

        iqueries = dict(staff=request.form.get('staff'),
                        period=request.form.get('period'),
                        info=request.form.get('info'),
                        firm=request.form.get('firm'),
                        date_inq=request.form.get('date_inq'),
                        iquery_id=cand_id)
        if any(iqueries.items()) is not None:
            iquery = Inquery(**iqueries)
            db.session.add(iquery)
            db.session.commit()

        return redirect(url_for('search'))
    return render_template('edit.html', results=results)


if __name__ == "__main__":
    app.run(debug=True)
