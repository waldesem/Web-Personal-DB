from datetime import datetime
from enum import Enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Roles(Enum):

    admin = 'admin'
    superuser = 'superuser'
    user = 'user'
    api = 'api'


class Status(Enum):

    new = 'Новый'
    update = 'Обновлен'
    manual = 'Проверка'
    save = "Сохранен"
    robot = 'Робот'
    reply = 'Обработан'
    poligraf = 'ПФО'
    result = 'Результат'
    finish = 'Окончено'
    cancel = 'Отмена'
    error = 'Ошибка'


class User(db.Model):
    """ Create model for users"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(250))
    username = db.Column(db.String(250), unique=True)
    password = db.Column(db.LargeBinary)
    pswd_create = db.Column(db.DateTime, default=datetime.now())
    pswd_change = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    blocked = db.Column(db.Boolean(), default=False)
    role = db.Column(db.String(250))
    messages = db.relationship('Message', backref='messages', cascade="all, delete, delete-orphan")

    def has_role(self, role):
        return self.role == role
    

class Message(db.Model):
    """ Create model for message"""

    __tablename__ = 'messages'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    message = db.Column(db.Text)
    status = db.Column(db.String(250), default=Status.new.value)
    create = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Candidate(db.Model):  # модель анкетных данных
    """ Create model for candidates dates"""

    __tablename__ = 'candidates'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    region = db.Column(db.String(250))
    fullname = db.Column(db.String(250), index=True)
    previous = db.Column(db.String(250))
    birthday = db.Column(db.Date, index=True)
    birthplace = db.Column(db.String(250))
    country = db.Column(db.String(250))
    snils = db.Column(db.String(250))
    inn = db.Column(db.String(250))
    education = db.Column(db.String(250))
    addition = db.Column(db.Text)
    status = db.Column(db.String(250), default=Status.new.value)
    create = db.Column(db.DateTime, default=datetime.now())
    update = db.Column(db.DateTime)
    recruiter = db.Column(db.String(250))
    request_id = db.Column(db.Integer)
    documents = db.relationship('Document', backref='candidates', cascade="all, delete, delete-orphan")
    addresses = db.relationship('Address', backref='candidates', cascade="all, delete, delete-orphan")
    workplaces = db.relationship('Workplace', backref='candidates', cascade="all, delete, delete-orphan")
    contacts = db.relationship('Contact', backref='candidates', cascade="all, delete, delete-orphan")
    staffs = db.relationship('Staff', backref='candidates', cascade="all, delete, delete-orphan")
    checks = db.relationship('Check', backref='candidates', cascade="all, delete, delete-orphan")
    poligrafs = db.relationship('Poligraf', backref='candidates', cascade="all, delete, delete-orphan")
    inquiries = db.relationship('Inquiry', backref='candidates', cascade="all, delete, delete-orphan")
    investigations = db.relationship('Investigation', backref='candidates', cascade="all, delete, delete-orphan")


class Staff(db.Model):  # создаем общий класс должности
    """ Create model for staff"""

    __tablename__ = 'staffs'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    position = db.Column(db.String(250))
    department = db.Column(db.String(250))
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Document(db.Model):  # модель паспорта
    """ Create model for Document dates"""

    __tablename__ = 'documents'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    view = db.Column(db.String(250))
    series = db.Column(db.String(25))
    number = db.Column(db.String(25))
    agency = db.Column(db.String(250))
    issue = db.Column(db.Date)
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Address(db.Model):  # создаем общий класс модель адреса
    """ Create model for addresses"""

    __tablename__ = 'addresses'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    view = db.Column(db.String(250))
    region = db.Column(db.String(250))
    address = db.Column(db.String(250))
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Workplace(db.Model):  # создаем общий класс модель рабочих мест
    """ Create model for workplaces"""

    __tablename__ = 'workplaces'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    period = db.Column(db.String(250))
    workplace = db.Column(db.String(250))
    address = db.Column(db.String(250))
    position = db.Column(db.String(250))
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Contact(db.Model):  # создаем общий класс телефонного номера
    """ Create model for phones"""

    __tablename__ = 'contacts'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    view = db.Column(db.String(250))
    contact = db.Column(db.String(250))
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
    path = db.Column(db.String(250))
    pfo = db.Column(db.Boolean, default=False)
    comments = db.Column(db.Text)
    conclusion = db.Column(db.String(250), default=Status.save.value)
    deadline = db.Column(db.DateTime, default=datetime.now())
    officer = db.Column(db.String(250))
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
    registries = db.relationship('Registry', backref='checks', cascade="all, delete, delete-orphan")


class Registry(db.Model):  # модель данных результаты ПФО
    """ Create model for poligraf"""

    __tablename__ = 'registries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    comments = db.Column(db.Text)
    decision = db.Column(db.String(250))
    deadline = db.Column(db.DateTime, default=datetime.now())
    supervisor = db.Column(db.String(25))
    check_id = db.Column(db.Integer, db.ForeignKey('checks.id'))


class Poligraf(db.Model):  # модель данных результаты ПФО
    """ Create model for poligraf"""

    __tablename__ = 'poligrafs'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    theme = db.Column(db.String(250))
    results = db.Column(db.Text)
    officer = db.Column(db.String(25))
    deadline = db.Column(db.Date, default=datetime.now())
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Investigation(db.Model):  # модель данных служебных расследований
    """ Create model for ivestigation"""

    __tablename__ = 'investigations'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    theme = db.Column(db.String(250))
    info = db.Column(db.Text)
    deadline = db.Column(db.Date, default=datetime.now())
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Inquiry(db.Model):  # модель данных запросов по работникам
    """ Create model for candidates inquiries"""

    __tablename__ = 'inquiries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    info = db.Column(db.Text)
    initiator = db.Column(db.String(250))
    source = db.Column(db.String(250))
    deadline = db.Column(db.Date, default=datetime.now())
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
    

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
