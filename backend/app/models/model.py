from datetime import datetime

from sqlalchemy_searchable import SearchQueryMixin, make_searchable
from sqlalchemy_utils.types import TSVectorType
from flask_sqlalchemy.query import Query

from .. import db, cache
from .classes import Category, Status


make_searchable(db.metadata)


def default_time():
    """
    Returns the current datetime.
    :return: The current datetime.
    :rtype: datetime
    """
    return datetime.now()


class Region(db.Model):
    """ Create model for regions"""

    __tablename__ = 'regions'
    
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    region = db.Column(db.String(255), unique=True)
    users = db.relationship('User', backref='users')
    persons = db.relationship('Person', backref='persons')
   
    
user_groups = db.Table(
    'user_groups',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer(), db.ForeignKey('groups.id'))
)
    
    
user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)
        
        
class Group(db.Model):
    """ Create model for groups"""

    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(255), unique=True)
    connects = db.relationship('Connect', backref='groups')


class Role(db.Model):
    """ Create model for roles"""

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(255), unique=True)
    

class User(db.Model):
    """ Create model for users"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    fullname = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.LargeBinary)
    email = db.Column(db.String(255), unique=True)
    pswd_create = db.Column(db.DateTime, default=default_time)
    pswd_change = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    blocked = db.Column(db.Boolean(), default=False)
    attempt = db.Column(db.Integer(), default=0)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    reports = db.relationship('Report', backref='users', 
                              cascade="all, delete, delete-orphan")
    roles = db.relationship('Role', secondary=user_roles, 
                            backref=db.backref('users', lazy='dynamic'))
    groups = db.relationship('Group', secondary=user_groups, 
                             backref=db.backref('users', lazy='dynamic'))
   
    @cache.memoize(60)
    def has_group(self, group):
        """
        Checks if the given group exists in the list of groups.
        Parameters:
            group (str): The name of the group to check.
        Returns:
            bool: True if the group exists, False otherwise.
        """
        return any(g.group == group for g in self.groups)
    
    @cache.memoize(60)
    def has_role(self, role):
        """
        A function that checks if the user has a specific role.
        Parameters:
            role (str): The role to check for.
        Returns:
            bool: True if the user has the specified role, False otherwise.
        """
        return any(r.role == role for r in self.roles)
    
    @cache.memoize(60)
    def has_blocked(self):
        """
        A function that checks if the current user is blocked.
        Returns:
            bool: True if the user is blocked, False otherwise.
        """
        return self.blocked
    

class Report(db.Model):
    """ Create model for report"""

    __tablename__ = 'reports'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    report = db.Column(db.Text)
    status = db.Column(db.String(255), default=Status.new.value)
    create = db.Column(db.DateTime, default=default_time)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class PersonQuery(Query, SearchQueryMixin):
    """ Class for searchable Connect table (only postgresql)"""
    pass
   

class Person(db.Model):
    """ Create model for persons dates"""
    query_class = PersonQuery

    __tablename__ = 'persons'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    category = db.Column(db.String(255), default=Category.candidate.value)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    fullname = db.Column(db.String(255), nullable=False, index=True)
    previous = db.Column(db.String(255))
    birthday = db.Column(db.Date, nullable=False)
    birthplace = db.Column(db.Text)
    country = db.Column(db.String(255))
    snils = db.Column(db.String(11))
    inn = db.Column(db.String(12))
    education = db.Column(db.Text)
    addition = db.Column(db.Text)
    path = db.Column(db.Text)
    status = db.Column(db.String(255), default=Status.new.value)
    create = db.Column(db.DateTime, default=default_time)
    update = db.Column(db.DateTime, onupdate=default_time)
    request_id = db.Column(db.Integer)
    documents = db.relationship('Document', backref='persons', 
                                cascade="all, delete, delete-orphan")
    addresses = db.relationship('Address', backref='persons', 
                                cascade="all, delete, delete-orphan")
    workplaces = db.relationship('Workplace', backref='persons', 
                                 cascade="all, delete, delete-orphan")
    contacts = db.relationship('Contact', backref='persons', 
                               cascade="all, delete, delete-orphan")
    staffs = db.relationship('Staff', backref='persons', 
                             cascade="all, delete, delete-orphan")
    checks = db.relationship('Check', backref='persons', 
                             cascade="all, delete, delete-orphan")
    registries = db.relationship('Registry', backref='persons', 
                                 cascade="all, delete, delete-orphan")
    poligrafs = db.relationship('Poligraf', backref='persons', 
                                cascade="all, delete, delete-orphan")
    inquiries = db.relationship('Inquiry', backref='persons', 
                                cascade="all, delete, delete-orphan")
    investigations = db.relationship('Investigation', backref='persons', 
                                     cascade="all, delete, delete-orphan")
    relations= db.relationship('Relation', backref='persons', 
                               cascade="all, delete, delete-orphan")
    tags= db.relationship('Tag', backref='tags', 
                          cascade="all, delete, delete-orphan")
    ones = db.relationship('OneS', backref='ones', 
                           cascade="all, delete, delete-orphan")
    # comment if not use Postgres
    search_vector = db.Column(TSVectorType('previous', 'fullname', 'inn')) 
    
    def has_status(self, status):
        """
        Check if the current status of the object matches any of the given status values.
        Args:
            status (list): A list of status values to check against.
        Returns:
            bool: True if the current status matches any of the given status values, False otherwise.
        """
        return self.status in status


class Relation(db.Model):
    """ Create model for relations"""

    __tablename__ = 'relations'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    relation = db.Column(db.String(255))
    relation_id = db.Column(db.Integer)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    

class Staff(db.Model):
    """ Create model for staff"""

    __tablename__ = 'staffs'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    position = db.Column(db.Text)
    department = db.Column(db.Text)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Document(db.Model):
    """ Create model for Document dates"""

    __tablename__ = 'documents'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    view = db.Column(db.String(255))
    series = db.Column(db.String(255))
    number = db.Column(db.String(255))
    agency = db.Column(db.Text)
    issue = db.Column(db.Date)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Address(db.Model): 
    """ Create model for addresses"""

    __tablename__ = 'addresses'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    view = db.Column(db.String(255))
    region = db.Column(db.String(255))
    address = db.Column(db.Text)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Workplace(db.Model):
    """ Create model for workplaces"""

    __tablename__ = 'workplaces'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    now_work = db.Column(db.Boolean, default=False)
    workplace = db.Column(db.Text)
    address = db.Column(db.Text)
    position = db.Column(db.Text)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Contact(db.Model):  # создаем общий класс телефонного номера
    """ Create model for contacts"""

    __tablename__ = 'contacts'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    view = db.Column(db.String(255))
    contact = db.Column(db.String(255))
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Check(db.Model):  # модель данных проверки кандидатов
    """ Create model for persons checks"""

    __tablename__ = 'checks'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
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
    path = db.Column(db.Text)
    pfo = db.Column(db.Boolean, default=False)
    comments = db.Column(db.Text)
    conclusion = db.Column(db.String(255))
    officer = db.Column(db.String(255))
    deadline = db.Column(db.DateTime, default=default_time, 
                         onupdate=default_time)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    registries = db.relationship('Registry', backref='checks', 
                                 cascade="all, delete, delete-orphan")


class Registry(db.Model):  # модель данных результаты ПФО
    """ Create model for poligraf"""

    __tablename__ = 'registries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    comments = db.Column(db.Text)
    decision = db.Column(db.String(255))
    supervisor = db.Column(db.String(255))
    deadline = db.Column(db.DateTime, default=default_time)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    check_id = db.Column(db.Integer, db.ForeignKey('checks.id'))


class Poligraf(db.Model):  # модель данных результаты ПФО
    """ Create model for poligraf"""

    __tablename__ = 'poligrafs'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    theme = db.Column(db.String(255))
    results = db.Column(db.Text)
    path = db.Column(db.Text)
    officer = db.Column(db.String(255))
    deadline = db.Column(db.Date, default=default_time)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Investigation(db.Model):
    """ Create model for ivestigation"""

    __tablename__ = 'investigations'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    theme = db.Column(db.String(255))
    info = db.Column(db.Text)
    path = db.Column(db.Text)
    officer = db.Column(db.String(255))
    deadline = db.Column(db.Date, default=default_time, onupdate=default_time)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Inquiry(db.Model):
    """ Create model for persons inquiries"""

    __tablename__ = 'inquiries'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    info = db.Column(db.Text)
    initiator = db.Column(db.String(255))
    source = db.Column(db.String(255))
    officer = db.Column(db.String(255))
    deadline = db.Column(db.Date, default=default_time)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class ConnectQuery(Query, SearchQueryMixin):
    """ Class for searchable Connect table (only postgresql)"""
    pass

class Connect(db.Model):
    """ Create model for persons connects"""
    
    query_class = ConnectQuery
    __tablename__ = 'connects'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    company = db.Column(db.String(255))
    city = db.Column(db.String(255))
    fullname = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    adding = db.Column(db.String(255))
    mobile = db.Column(db.String(255))
    mail = db.Column(db.String(255))
    comment = db.Column(db.Text)
    data = db.Column(db.Date, default=default_time, onupdate=default_time)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    search_vector = db.Column(TSVectorType('company', 'fullname', 'mobile')) 


class OneS(db.Model):
    """ Create model for 1C database table"""

    __tablename__ = 'ones'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    fullname = db.Column(db.String(255))
    birth_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    start_position = db.Column(db.Text)
    end_date = db.Column(db.Date)
    end_position = db.Column(db.Text)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


db.configure_mappers()