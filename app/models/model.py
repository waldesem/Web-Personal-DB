from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

ma = Marshmallow()

db = SQLAlchemy()


class Personal(db.Model):  # создаем общий класс модели базы данных
    __abstract__ = True


class Users(Personal, UserMixin):  # модель пользователей системы
    """ Create model for users"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    full_name = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    role = db.Column(db.Text)


class Candidate(Personal):  # модель анкетных данных
    """ Create model for candidates dates"""

    __tablename__ = 'candidates'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    region = db.Column(db.Text)
    full_name = db.Column(db.Text, index=True)
    last_name = db.Column(db.Text)
    birthday = db.Column(db.Text)
    birth_place = db.Column(db.Text)
    country = db.Column(db.Text)
    snils = db.Column(db.Text)
    inn = db.Column(db.Text)
    education = db.Column(db.Text)
    addition = db.Column(db.Text)
    update_date = db.Column(db.Text)
    status = db.Column(db.Text)
    request_id = db.Column(db.Integer)
    passports = db.relationship('Passport', backref='candidates', cascade="all, delete-orphan")
    addresses = db.relationship('Address', backref='candidates', cascade="all, delete-orphan")
    workplaces = db.relationship('Workplace', backref='candidates', cascade="all, delete-orphan")
    contacts = db.relationship('Contact', backref='candidates', cascade="all, delete-orphan")
    relations = db.relationship('RelationShip', backref='candidates', cascade="all, delete-orphan")
    staffs = db.relationship('Staff', backref='candidates', cascade="all, delete-orphan")
    checks = db.relationship('Check', backref='candidates')
    poligrafs = db.relationship('Poligraf', backref='candidates', cascade="all, delete-orphan")
    inqueries = db.relationship('Inquery', backref='candidates', cascade="all, delete-orphan")
    investigations = db.relationship('Investigation', backref='candidates', cascade="all, delete-orphan")


class Passport(Personal):  # модель паспорта
    """ Create model for passport dates"""

    __tablename__ = 'passports'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    p_series_passport = db.Column(db.Text)
    p_number_passport = db.Column(db.Text)
    p_agency = db.Column(db.Text)
    p_date_given = db.Column(db.Text)
    passport_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Address(Personal):  # создаем общий класс модель адреса
    """ Create model for addresses"""

    __tablename__ = 'addresses'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    a_region = db.Column(db.Text)
    a_address = db.Column(db.Text)
    a_type = db.Column(db.Text)
    address_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Workplace(Personal):  # создаем общий класс модель рабочих мест
    """ Create model for workplaces"""

    __tablename__ = 'workplaces'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    w_period = db.Column(db.Text)
    w_work_place = db.Column(db.Text)
    w_address = db.Column(db.Text)
    w_staff = db.Column(db.Text)
    work_place_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Contact(Personal):  # создаем общий класс телефонного номера
    """ Create model for phones"""

    __tablename__ = 'contacts'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    c_type = db.Column(db.Text)
    c_contact = db.Column(db.Text)
    contact_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class RelationShip(Personal):  # создаем общий класс связи
    """ Create model for relations"""

    __tablename__ = 'relations'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    r_relation = db.Column(db.Text)
    r_full_name = db.Column(db.Text)
    r_birthday = db.Column(db.Text)
    r_address = db.Column(db.Text)
    r_workplace = db.Column(db.Text)
    r_contact = db.Column(db.Text)
    relation_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Staff(Personal):  # создаем общий класс должности
    """ Create model for staff"""

    __tablename__ = 'staffs'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    s_staff = db.Column(db.Text)
    s_department = db.Column(db.Text)
    staff_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Check(Personal):  # модель данных проверки кандидатов
    """ Create model for candidates checks"""

    __tablename__ = 'checks'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    check_work_place = db.Column(db.Text)
    former_employee = db.Column(db.Text)
    check_passport = db.Column(db.Text)
    check_inn = db.Column(db.Text)
    check_debt = db.Column(db.Text)
    check_bankruptcy = db.Column(db.Text)
    check_bki = db.Column(db.Text)
    check_court = db.Column(db.Text)
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
    path = db.Column(db.Text)
    check_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
    registries = db.relationship('Registry', backref='checks', cascade="all, delete-orphan")


class Registry(Personal):  # модель данных результаты ПФО
    """ Create model for poligraf"""

    __tablename__ = 'registries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    marks = db.Column(db.Text)
    decision = db.Column(db.Text)
    dec_date = db.Column(db.Text)
    supervisor = db.Column(db.Text)
    registry_check_id = db.Column(db.Integer, db.ForeignKey('checks.id'))


class Poligraf(Personal):  # модель данных результаты ПФО
    """ Create model for poligraf"""

    __tablename__ = 'poligrafs'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    theme = db.Column(db.Text)
    results = db.Column(db.Text)
    officer = db.Column(db.Text)
    date_pfo = db.Column(db.Text)
    poligraf_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Investigation(Personal):  # модель данных служебных расследований
    """ Create model for ivestigation"""
    __tablename__ = 'investigations'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    theme = db.Column(db.Text)
    info = db.Column(db.Text)
    date_inv = db.Column(db.Text)
    inv_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Inquery(Personal):  # модель данных запросов по работникам
    """ Create model for candidates inqueries"""

    __tablename__ = 'inqueries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    info = db.Column(db.Text)
    initiator = db.Column(db.Text)
    date_inq = db.Column(db.Text)
    iquery_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class CandidateSchema(ma.Schema):
    class Meta:
        fields = ("id", "full_name", "birthday", "birth_place", "country", "snils", "inn")


class PassportSchema(ma.Schema):
    class Meta:
        fields = ("p_series_passport", "p_number_passport", "p_agency", "p_date_given")


class AddressSchema(ma.Schema):
    class Meta:
        fields = ("a_type", "a_address")


cand_schema = CandidateSchema()
passp_schema = PassportSchema()
addr_schema = AddressSchema()
