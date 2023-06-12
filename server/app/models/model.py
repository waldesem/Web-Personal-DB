from datetime import datetime
from enum import Enum

from flask_security import RoleMixin
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields

db = SQLAlchemy()
ma = Marshmallow()

TODAY = datetime.now()


class Status(Enum):
    """Класс статусов"""

    NEWFAG = 'Новый'
    UPDATE = 'Обновлен'
    MANUAL = 'Проверка'
    SAVE = "Сохранено"
    AUTO = 'Автомат'
    ROBOT = 'Робот'
    REPLY = 'Обработано'
    POLIGRAF = 'ПФО'
    RESULT = 'Результат'
    FINISH = 'Окончено'
    CANCEL = 'Отмена'
    ERROR = 'Ошибка'

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):  # модель пользователей системы
    """ Create model for users"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(250))
    username = db.Column(db.String(250), unique=True)
    password = db.Column(db.LargeBinary)
    pswd_create = db.Column(db.Date)
    pswd_change = db.Column(db.Date)
    last_login = db.Column(db.DateTime)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})
    

class Candidate(db.Model):  # модель анкетных данных
    """ Create model for candidates dates"""

    __tablename__ = 'candidates'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    region = db.Column(db.String(250))
    fullname = db.Column(db.String(250), index=True)
    previous = db.Column(db.String(250))
    birthday = db.Column(db.Date)
    birthplace = db.Column(db.String(250))
    country = db.Column(db.String(250))
    snils = db.Column(db.String(11))
    inn = db.Column(db.String(12))
    education = db.Column(db.String(250))
    addition = db.Column(db.Text)
    status = db.Column(db.String(250))
    deadline = db.Column(db.DateTime)
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
    autostatus = db.Column(db.String(250))
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
    pfo = db.Column(db.Boolean)
    comments = db.Column(db.Text)
    conclusion = db.Column(db.String(250))
    deadline = db.Column(db.DateTime)
    officer = db.Column(db.String(250))
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
    registries = db.relationship('Registry', backref='checks', cascade="all, delete, delete-orphan")


class Registry(db.Model):  # модель данных результаты ПФО
    """ Create model for poligraf"""

    __tablename__ = 'registries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    comments = db.Column(db.Text)
    decision = db.Column(db.String(250))
    deadline = db.Column(db.DateTime)
    supervisor = db.Column(db.String(25))
    check_id = db.Column(db.Integer, db.ForeignKey('checks.id'))


class Poligraf(db.Model):  # модель данных результаты ПФО
    """ Create model for poligraf"""

    __tablename__ = 'poligrafs'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    theme = db.Column(db.String(250))
    results = db.Column(db.Text)
    officer = db.Column(db.String(25))
    deadline = db.Column(db.Date)
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Investigation(db.Model):  # модель данных служебных расследований
    """ Create model for ivestigation"""

    __tablename__ = 'investigations'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    theme = db.Column(db.String(250))
    info = db.Column(db.Text)
    deadline = db.Column(db.Date)
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class Inquiry(db.Model):  # модель данных запросов по работникам
    """ Create model for candidates inquiries"""

    __tablename__ = 'inquiries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    info = db.Column(db.Text)
    initiator = db.Column(db.String(250))
    source = db.Column(db.String(250))
    deadline = db.Column(db.Date)
    cand_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))


class CandidateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Candidate
        ordered = True


class DocumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Document
        exclude = ("id",)
        ordered = True


class AddressSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Address
        exclude = ("id",)
        ordered = True


class StaffSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Staff
        exclude = ("id",)
        ordered = True


class WorkplaceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workplace
        exclude = ("id",)
        ordered = True


class ContactSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Contact
        exclude = ("id",)
        ordered = True


class CheckSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Check
        ordered = True


class InvestigationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Investigation
        ordered = True


class InquirySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inquiry
        ordered = True


class PoligrafSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Poligraf
        ordered = True


class RegistrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Registry
        ordered = True


class DeserialResume(ma.SQLAlchemyAutoSchema):
    """Схема для десериализации и верификации анкеты присланной по API"""

    resume = fields.Nested(CandidateSchema())
    document = fields.Nested(DocumentSchema())
    staff = fields.Nested(StaffSchema())
    addresses = fields.List(fields.Nested(AddressSchema()))
    workplaces = fields.List(fields.Nested(WorkplaceSchema()))
    contacts = fields.List(fields.Nested(ContactSchema()))


class SerialResume:
    """
    A class representing a candidate.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        # Set send_resume to None initially.
        self.send_resume = None

        # Initialize a new instance of the CandidateSchema class, including only certain fields.
        self.resume = CandidateSchema(only=('id', 'fullname', 'birthday', 'birthplace', 'snils', 'inn',))

        # Initialize a new instance of the DocumentSchema class.
        self.document = DocumentSchema()

        # Initialize a new instance of the AddressSchema class, including only the address field.
        self.address = AddressSchema(only=('address',))

    def decer_res(self, new_id, **kwargs):
        """
        This function retrieves a candidate's information from the database and returns it as a dictionary.
        Args:
            new_id (int): The ID of the candidate whose information is being retrieved.
            **kwargs (dict): Any additional information to be included in the final dictionary.
        Returns:
            dict: A dictionary containing the candidate's information and any additional information provided.
        """
        # Retrieve the Candidate object with the given ID.
        resum = db.session.query(Candidate).get(new_id)
        # Retrieve the most recent Document object associated with the candidate.
        docum = db.session.query(Document).filter_by(cand_id=new_id).order_by(Document.id.desc()).first()
        # Retrieve the most recent Address object associated with the candidate that contains the word "регистрац" (
        # registration).
        addr = db.session.query(Address).filter_by(cand_id=new_id).filter(Address.view.ilike("%регистрац%")). \
            order_by(Address.id.desc()).first()
        # Combine the candidate's information, document information, address information, and any additional
        # information into a dictionary.
        self.send_resume = self.resume.dump(resum) | self.document.dump(docum) | self.address.dump(addr) | dict(kwargs)
        return self.send_resume


candidate_schema = DeserialResume()
serial_resume = SerialResume()

resume_schema = CandidateSchema()
staff_schema = StaffSchema()
document_schema = DocumentSchema()
address_schema = AddressSchema()
contact_schema = ContactSchema()
work_schema = WorkplaceSchema()
check_schema = CheckSchema()
registry_schema = RegistrySchema()
poligraf_schema = PoligrafSchema()
investigation_schema = InvestigationSchema()
inquiry_schema = InquirySchema()
