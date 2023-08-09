from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from .classify import Category, Decisions, Status


db = SQLAlchemy()

def default_time():
    return datetime.now()


class Region(db.Model):
    """ Create model for regions"""

    __tablename__ = 'regions'
    
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    region = db.Column(db.String(250))
    users = db.relationship('User', backref='users')
    persons = db.relationship('Person', backref='persons')


class User(db.Model):
    """ Create model for users"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(250))
    username = db.Column(db.String(250), unique=True)
    password = db.Column(db.LargeBinary)
    email = db.Column(db.String(250))
    pswd_create = db.Column(db.DateTime, default=default_time)
    pswd_change = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    blocked = db.Column(db.Boolean(), default=False)
    role = db.Column(db.String(250))
    attempt = db.Column(db.Integer(), default=0)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    reports = db.relationship('Report', backref='reports', cascade="all, delete, delete-orphan")
    
    def has_role(self, role):
        return self.role == role
    
    def has_blocked(self):
        return self.blocked


class Report(db.Model):
    """ Create model for report"""

    __tablename__ = 'reports'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    report = db.Column(db.Text)
    status = db.Column(db.String(250), default=Status.new.value)
    create = db.Column(db.DateTime, default=default_time)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class TokenBlocklist(db.Model):
    """ Create model for tokens"""
    
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default= default_time, nullable=False)

class Person(db.Model):
    """ Create model for persons dates"""

    __tablename__ = 'persons'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    category = db.Column(db.String(250), default=Category.candidate.value)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    fullname = db.Column(db.String(250), nullable=False, index=True)
    previous = db.Column(db.String(250))
    birthday = db.Column(db.Date, nullable=False, index=True)
    birthplace = db.Column(db.String(250))
    country = db.Column(db.String(250))
    snils = db.Column(db.String(250))
    inn = db.Column(db.String(12))
    education = db.Column(db.String(250))
    addition = db.Column(db.Text)
    path = db.Column(db.String(250))
    status = db.Column(db.String(250), default=Status.new.value)
    create = db.Column(db.DateTime, default=default_time)
    update = db.Column(db.DateTime, default=default_time, onupdate=default_time)
    request_id = db.Column(db.Integer, default=0)
    documents = db.relationship('Document', backref='persons', cascade="all, delete, delete-orphan")
    addresses = db.relationship('Address', backref='persons', cascade="all, delete, delete-orphan")
    workplaces = db.relationship('Workplace', backref='persons', cascade="all, delete, delete-orphan")
    contacts = db.relationship('Contact', backref='persons', cascade="all, delete, delete-orphan")
    staffs = db.relationship('Staff', backref='persons', cascade="all, delete, delete-orphan")
    checks = db.relationship('Check', backref='persons', cascade="all, delete, delete-orphan")
    poligrafs = db.relationship('Poligraf', backref='persons', cascade="all, delete, delete-orphan")
    inquiries = db.relationship('Inquiry', backref='persons', cascade="all, delete, delete-orphan")
    investigations = db.relationship('Investigation', backref='persons', cascade="all, delete, delete-orphan")
    relations= db.relationship('Relation', backref='persons', cascade="all, delete, delete-orphan")

    def has_status(self, status):
        return self.status in status


class Relation(db.Model):
    """ Create model for relations"""

    __tablename__ = 'relations'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    relation = db.Column(db.String(250))
    relation_id = db.Column(db.Integer)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    

class Staff(db.Model):
    """ Create model for staff"""

    __tablename__ = 'staffs'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    position = db.Column(db.String(250))
    department = db.Column(db.String(250))
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Document(db.Model):
    """ Create model for Document dates"""

    __tablename__ = 'documents'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    view = db.Column(db.String(250))
    series = db.Column(db.String(25))
    number = db.Column(db.String(25))
    agency = db.Column(db.String(250))
    issue = db.Column(db.Date)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Address(db.Model): 
    """ Create model for addresses"""

    __tablename__ = 'addresses'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    view = db.Column(db.String(250))
    region = db.Column(db.String(250))
    address = db.Column(db.Text)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Workplace(db.Model):
    """ Create model for workplaces"""

    __tablename__ = 'workplaces'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    period = db.Column(db.String(250))
    workplace = db.Column(db.String(250))
    address = db.Column(db.String(250))
    position = db.Column(db.String(250))
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Contact(db.Model):  # создаем общий класс телефонного номера
    """ Create model for phones"""

    __tablename__ = 'contacts'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    view = db.Column(db.String(250))
    contact = db.Column(db.String(250))
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Check(db.Model):  # модель данных проверки кандидатов
    """ Create model for persons checks"""

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
    path = db.Column(db.String(250))
    pfo = db.Column(db.Boolean, default=False)
    comments = db.Column(db.Text)
    conclusion = db.Column(db.String(250), default=Status.save.value)
    officer = db.Column(db.String(250))
    deadline = db.Column(db.DateTime, default=default_time, onupdate=default_time)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    registries = db.relationship('Registry', backref='checks', cascade="all, delete, delete-orphan")


class Registry(db.Model):  # модель данных результаты ПФО
    """ Create model for poligraf"""

    __tablename__ = 'registries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    comments = db.Column(db.Text)
    decision = db.Column(db.String(250), default=Decisions.agreed.value)
    supervisor = db.Column(db.String(25))
    deadline = db.Column(db.DateTime, default=default_time)
    check_id = db.Column(db.Integer, db.ForeignKey('checks.id'))


class Poligraf(db.Model):  # модель данных результаты ПФО
    """ Create model for poligraf"""

    __tablename__ = 'poligrafs'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    theme = db.Column(db.String(250))
    results = db.Column(db.Text)
    officer = db.Column(db.String(25))
    deadline = db.Column(db.Date, default=default_time)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Investigation(db.Model):
    """ Create model for ivestigation"""

    __tablename__ = 'investigations'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    theme = db.Column(db.String(250))
    info = db.Column(db.Text)
    officer = db.Column(db.String(25))
    deadline = db.Column(db.Date, default=default_time)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Inquiry(db.Model):
    """ Create model for persons inquiries"""

    __tablename__ = 'inquiries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    info = db.Column(db.Text)
    initiator = db.Column(db.String(250))
    source = db.Column(db.String(250))
    officer = db.Column(db.String(25))
    deadline = db.Column(db.Date, default=default_time)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Log(db.Model):
    """ Create model for logs"""
    
    __tablename__ = 'logs'
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime)
    level = db.Column(db.String(250))
    message = db.Column(db.Text)
    pathname = db.Column(db.String(250))
    lineno = db.Column(db.Integer)
    status = db.Column(db.String, default=Status.new)

    def __init__(self, timestamp, level, message, pathname, lineno):
        self.timestamp = timestamp
        self.level = level
        self.message = message
        self.pathname = pathname
        self.lineno = lineno
