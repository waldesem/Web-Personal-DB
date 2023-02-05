from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Personal(db.Model):  # создаем общий класс модели базы данных
    __abstract__ = True


class Users(Personal, UserMixin):   # модель пользователей системы
    """ Create model for users"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    role = db.Column(db.Text)
    region = db.Column(db.Text)


class Candidate(Personal):  # модель анкетных данных
    """ Create model for candidates dates"""

    __tablename__ = 'candidates'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    region = db.Column(db.Text)
    full_name = db.Column(db.Text, index=True)
    last_name = db.Column(db.Text)
    birthday = db.Column(db.Text, index=True)
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
    workplace_1 = db.Column(db.Text)
    workplace_2 = db.Column(db.Text)
    workplace_3 = db.Column(db.Text)
    addition = db.Column(db.Text)
    update_date = db.Column(db.Text)
    status = db.Column(db.Text)
    request_id = db.Column(db.Text)
    checks = db.relationship('Check', backref='candidates')
    poligraf = db.relationship('Poligraf', backref='candidates')
    inqueries = db.relationship('Inquery', backref='candidates')
    registries = db.relationship('Registr', backref='candidates')
    investigations = db.relationship('Investigation', backref='candidates')


class Check(Personal):  # модель данных проверки кандидатов
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
    check_mvd = db.Column(db.Text)
    check_internet = db.Column(db.Text)
    check_cronos = db.Column(db.Text)
    check_cross = db.Column(db.Text)
    check_addition = db.Column(db.Text)
    pfo = db.Column(db.Text)
    comment = db.Column(db.Text)
    resume = db.Column(db.Text)
    date_check = db.Column(db.Text)
    officer = db.Column(db.Text)
    url = db.Column(db.Text)
    check_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Poligraf(Personal):   # модель данных результаты ПФО
    """ Create model for poligraf"""

    __tablename__ = 'poligraf'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    theme = db.Column(db.Text)
    results = db.Column(db.Text)
    officer = db.Column(db.Text)
    date_pfo = db.Column(db.Text)
    poligraf_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Registr(Personal):    # модель данных результаты согласования
    """ Create model for registry of candidates"""

    __tablename__ = 'registries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    supervisor = db.Column(db.Text)
    marks = db.Column(db.Text)
    decision = db.Column(db.Text)
    dec_date = db.Column(db.Text)
    registry_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Investigation(Personal):  # модель данных служебных расследований
    """ Create model for ivestigation"""
    __tablename__ = 'investigations'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    theme = db.Column(db.Text)
    info = db.Column(db.Text)
    date_inv = db.Column(db.Text)
    inv_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Inquery(Personal):    # модель данных запросов по работникам
    """ Create model for candidates inqueries"""

    __tablename__ = 'inqueries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    info = db.Column(db.Text)
    initiator = db.Column(db.Text)
    date_inq = db.Column(db.Text)
    iquery_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
