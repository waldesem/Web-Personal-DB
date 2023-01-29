from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
    full_name = db.Column(db.Text, index=True)
    last_name = db.Column(db.Text)
    birthday = db.Column(db.Text)
    birth_place = db.Column(db.Text)
    country = db.Column(db.Text)
    series_passport = db.Column(db.Text)
    number_passport = db.Column(db.Text)
    agency = db.Column(db.Text)
    date_given = db.Column(db.Text)
    snils = db.Column(db.Text)
    inn = db.Column(db.Text)
    reg_address = db.Column(db.Text)
    live_address = db.Column(db.Text)
    phone = db.Column(db.Text)
    email = db.Column(db.Text)
    education = db.Column(db.Text)
    addition = db.Column(db.Text)
    update_date = db.Column(db.Text)
    status = db.Column(db.Text)
    checks = db.relationship('Check', backref='candidates')
    investigations = db.relationship('Investigations', backref='candidates')
    poligraf = db.relationship('Poligraf', backref='candidates')
    inqueries = db.relationship('Inquery', backref='candidates')
    registries = db.relationship('Registr', backref='candidates')


class Check(Personal):
    """ Create model for candidates checks"""

    __tablename__ = 'checks'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    staff = db.Column(db.Text)
    department = db.Column(db.Text)
    check_work_place = db.Column(db.Text)
    check_passport = db.Column(db.Text)
    check_debt = db.Column(db.Text)
    check_bankruptcy = db.Column(db.Text)
    check_bki = db.Column(db.Text)
    check_affiliation = db.Column(db.Text)
    check_terrorist = db.Column(db.Text)
    check_internet = db.Column(db.Text)
    check_cronos = db.Column(db.Text)
    check_cross = db.Column(db.Text)
    check_addition = db.Column(db.Text)
    pfo = db.Column(db.Text)
    resume = db.Column(db.Text)
    date_check = db.Column(db.Text)
    officer = db.Column(db.Text)
    url = db.Column(db.Text)
    check_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Investigation(Personal):
    """ Create model for ivestigation"""
    __tablename__ = 'investigations'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)

    info = db.Column(db.Text)
    source = db.Column(db.Text)
    date_inv = db.Column(db.Text)
    inv_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Inquery(Personal):
    """ Create model for candidates inqueries"""

    __tablename__ = 'iqueries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    staff = db.Column(db.Text)
    period = db.Column(db.Text)
    firm = db.Column(db.Text)
    date_inq = db.Column(db.Text)
    iquery_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Poligraf(Personal):
    """ Create model for poligraf investigation"""

    __tablename__ = 'poligraf'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    info = db.Column(db.Text)
    date_pfo = db.Column(db.Text)
    officer = db.Column(db.Text)
    poligraf_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Registr(Personal):
    """ Create model for registry of candidates"""

    __tablename__ = 'registries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    supervisor = db.Column(db.Text)
    checks = db.Column(db.Text)
    fin_decision = db.Column(db.Text)
    final_date = db.Column(db.Text)
    registry_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


# for replace upper code after migrating to postgresql

# class Personal(db.Model):  # create model DB for personal date, checks, inquries and for registry
#     __abstract__ = True


# class Users(Personal, UserMixin):
#     """ Create model for registry of candidates"""

#     __tablename__ = 'users'

#     id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
#     username = db.Column(db.String)
#     password = db.Column(db.String)


# class Candidate(Personal):
#     """ Create model for candidates dates"""

#     __tablename__ = 'candidates'

#     id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
#     full_name = db.Column(db.String, index=True)
#     last_name = db.Column(db.String)
#     birthday = db.Column(db.Date, index=True)
#     birth_place = db.Column(db.String)
#     country = db.Column(db.String)
#     series_passport = db.Column(db.String)
#     number_passport = db.Column(db.String)
#     agency = db.Column(db.String)
#     date_given = db.Column(db.Date)
#     snils = db.Column(db.String)
#     inn = db.Column(db.String)
#     reg_address = db.Column(db.String)
#     live_address = db.Column(db.String)
#     phone = db.Column(db.String)
#     email = db.Column(db.String)
#     education = db.Column(db.String)
#     addition = db.Column(db.Text)
#     update_date = db.Column(db.Date)
#     checks = db.relationship('Check', backref='candidates', cascade="all,delete")
#     iqueries = db.relationship('Inquery', backref='candidates', cascade="all,delete")
#     registries = db.relationship('Registr', backref='candidates', cascade="all,delete")


# class Check(Personal):
#     """ Create model for candidates checks"""

#     __tablename__ = 'checks'

#     id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
#     staff = db.Column(db.String)
#     department = db.Column(db.String)
#     check_work_place = db.Column(db.Text)
#     check_passport = db.Column(db.Text)
#     check_debt = db.Column(db.Text)
#     check_bankruptcy = db.Column(db.Text)
#     check_bki = db.Column(db.Text)
#     check_affiliation = db.Column(db.Text)
#     check_terrorist = db.Column(db.Text)
#     check_internet = db.Column(db.Text)
#     check_cronos = db.Column(db.Text)
#     check_cross = db.Column(db.Text)
#     check_addition = db.Column(db.Text)
#     resume = db.Column(db.String)
#     date_check = db.Column(db.Date)
#     officer = db.Column(db.String)
#     check_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


# class Inquery(Personal):
#     """ Create model for candidates inqueries"""

#     __tablename__ = 'inqueries'

#     id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
#     staff = db.Column(db.String)
#     period = db.Column(db.String)
#     info = db.Column(db.Text)
#     firm = db.Column(db.String)
#     date_inq = db.Column(db.Date)
#     iquery_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


# class Registr(Personal):
#     """ Create model for registry of candidates"""

#     __tablename__ = 'registries'

#     id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
#     checks = db.Column(db.String)
#     recruiter = db.Column(db.String)
#     fin_decision = db.Column(db.String)
#     final_date = db.Column(db.Date)
#     url = db.Column(db.String)
#     registry_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
