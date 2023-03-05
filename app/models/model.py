from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

ma = Marshmallow()
db = SQLAlchemy()


class User(db.Model, UserMixin):  # модель пользователей системы
    """ Create model for users"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String)


class Candidate(db.Model):  # модель анкетных данных
    """ Create model for candidates dates"""

    __tablename__ = 'candidates'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    region = db.Column(db.String)
    fullname = db.Column(db.String, nullable=False, index=True)
    previous = db.Column(db.String)
    birthday = db.Column(db.Date, nullable=False)
    birthplace = db.Column(db.String)
    country = db.Column(db.String)
    snils = db.Column(db.String, unique=True)
    inn = db.Column(db.String, unique=True)
    education = db.Column(db.String)
    addition = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String)
    request_id = db.Column(db.Integer)
    Documents = db.relationship('Document', backref='candidates', cascade="all, delete-orphan")
    addresses = db.relationship('Address', backref='candidates', cascade="all, delete-orphan")
    workplaces = db.relationship('Workplace', backref='candidates', cascade="all, delete-orphan")
    contacts = db.relationship('Contact', backref='candidates', cascade="all, delete-orphan")
    relations = db.relationship('RelationShip', backref='candidates', cascade="all, delete-orphan")
    staffs = db.relationship('Staff', backref='candidates', cascade="all, delete-orphan")
    checks = db.relationship('Check', backref='candidates')
    poligrafs = db.relationship('Poligraf', backref='candidates', cascade="all, delete-orphan")
    inquiries = db.relationship('Inquiry', backref='candidates', cascade="all, delete-orphan")
    investigations = db.relationship('Investigation', backref='candidates', cascade="all, delete-orphan")


class Document(db.Model):  # модель паспорта
    """ Create model for Document dates"""

    __tablename__ = 'documents'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    view = db.Column(db.String)
    series = db.Column(db.String)
    number = db.Column(db.String)
    agency = db.Column(db.String)
    issue = db.Column(db.Date)
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Address(db.Model):  # создаем общий класс модель адреса
    """ Create model for addresses"""

    __tablename__ = 'addresses'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    view = db.Column(db.String)
    region = db.Column(db.String)
    address = db.Column(db.String)
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Workplace(db.Model):  # создаем общий класс модель рабочих мест
    """ Create model for workplaces"""

    __tablename__ = 'workplaces'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    period = db.Column(db.String)
    workplace = db.Column(db.String)
    address = db.Column(db.String)
    position = db.Column(db.String)
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Contact(db.Model):  # создаем общий класс телефонного номера
    """ Create model for phones"""

    __tablename__ = 'contacts'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    view = db.Column(db.String)
    contact = db.Column(db.String)
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class RelationShip(db.Model):  # создаем общий класс связи
    """ Create model for relations"""

    __tablename__ = 'relations'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    relation = db.Column(db.String)
    fullname = db.Column(db.String)
    birthday = db.Column(db.Date)
    address = db.Column(db.String)
    workplace = db.Column(db.String)
    contact = db.Column(db.String)
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Staff(db.Model):  # создаем общий класс должности
    """ Create model for staff"""

    __tablename__ = 'staffs'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    position = db.Column(db.String)
    department = db.Column(db.String)
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Check(db.Model):  # модель данных проверки кандидатов
    """ Create model for candidates checks"""

    __tablename__ = 'checks'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    workplace = db.Column(db.Text)
    employee = db.Column(db.Text)
    document = db.Column(db.Text)
    inn = db.Column(db.Text)
    debt = db.Column(db.Text)
    bankruptcy = db.Column(db.Text)
    bki = db.Column(db.Text)
    courts = db.Column(db.Text)
    affiliation = db.Column(db.Text)
    terrorist = db.Column(db.Text)
    mvd = db.Column(db.Text)
    internet = db.Column(db.Text)
    cronos = db.Column(db.Text)
    cros = db.Column(db.Text)
    addition = db.Column(db.Text)
    path = db.Column(db.String)
    pfo = db.Column(db.Boolean)
    comments = db.Column(db.Text)
    conclusion = db.Column(db.String)
    deadline = db.Column(db.DateTime)
    officer = db.Column(db.String)
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
    registries = db.relationship('Registry', backref='checks', cascade="all, delete-orphan")


class Registry(db.Model):  # модель данных результаты ПФО
    """ Create model for poligraf"""

    __tablename__ = 'registries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    comments = db.Column(db.Text)
    decision = db.Column(db.String)
    deadline = db.Column(db.DateTime)
    supervisor = db.Column(db.String)
    check_id = db.Column(db.Integer, db.ForeignKey('checks.id'))


class Poligraf(db.Model):  # модель данных результаты ПФО
    """ Create model for poligraf"""

    __tablename__ = 'poligrafs'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    theme = db.Column(db.String)
    results = db.Column(db.Text)
    officer = db.Column(db.String)
    deadline = db.Column(db.Date)
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Investigation(db.Model):  # модель данных служебных расследований
    """ Create model for ivestigation"""

    __tablename__ = 'investigations'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    theme = db.Column(db.String)
    info = db.Column(db.Text)
    deadline = db.Column(db.Date)
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Inquiry(db.Model):  # модель данных запросов по работникам
    """ Create model for candidates inqueries"""

    __tablename__ = 'inquiries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    info = db.Column(db.Text)
    initiator = db.Column(db.String)
    # source = db.Column(db.String)
    deadline = db.Column(db.Date)
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class CandidateSchema(ma.Schema):
    class Meta:
        fields = ("id", "fullname", "birthday", "birthplace", "country", "snils", "inn")


class DocumentSchema(ma.Schema):
    class Meta:
        fields = ("series", "number", "agency", "issue")


class AddressSchema(ma.Schema):
    class Meta:
        fields = ("view", "address")


cand_schema = CandidateSchema()
doc_schema = DocumentSchema()
addr_schema = AddressSchema()

# db.create_all()
