from flask_login import UserMixin

from app import db


# db.drop_all()
# db.create_all()

class Personal(db.Model):  # create model DB for personal date, checks, inquries and for registry
    __abstract__ = True


class Users(Personal, UserMixin):
    """ Create model for registry of candidates"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    role = db.Column(db.Text)


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


# if __name__ == "__main__":
# db.session.add_all()
# db.session.commit()
