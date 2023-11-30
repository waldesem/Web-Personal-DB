from datetime import datetime

import asyncpg
from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, Boolean, \
      Text, Date, ForeignKey, Table
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, configure_mappers, sessionmaker, relationship
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType
from flask import current_app

from .. import cache
from .classes import Category, Status

engine = create_async_engine(current_app.config['SQLALCHEMY_ASYNC_DATABASE_URI'])
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
make_searchable(Base.metadata)
configure_mappers()


def default_time():
    return datetime.now()


user_groups = Table(
    'user_groups',
    Column('user_id', Integer(), ForeignKey('users.id')),
    Column('group_id', Integer(), ForeignKey('groups.id'))
)
    
    
user_roles = Table(
    'user_roles',
    Column('user_id', Integer(), ForeignKey('users.id')),
    Column('role_id', Integer(), ForeignKey('roles.id'))
)
        
        
class Group(Base):
    """ Create model for groups"""

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    group = Column(String(255), unique=True)


class Role(Base):
    """ Create model for roles"""

    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    role = Column(String(255), unique=True)
    

class User(Base):
    """ Create model for users"""

    __tablename__ = 'users'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    fullname = Column(String(255))
    username = Column(String(255), unique=True)
    password = Column(LargeBinary)
    email = Column(String(255), unique=True)
    pswd_create = Column(DateTime, default=default_time)
    pswd_change = Column(DateTime)
    last_login = Column(DateTime)
    blocked = Column(Boolean(), default=False)
    attempt = Column(Integer(), default=0)
    region_id = Column(Integer, ForeignKey('regions.id'))
    reports = relationship('Report', back_populates='users', 
                            cascade="all, delete, delete-orphan")
    roles = relationship('Role', secondary=user_roles, back_populates='users')
    groups = relationship('Group', secondary=user_groups, back_populates='users')
   
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
    

class Report(Base):
    """ Create model for report"""

    __tablename__ = 'reports'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    category = Column(String(255), default='important')
    title = Column(String(255))
    report = Column(Text)
    status = Column(String(255), default=Status.new.value)
    create = Column(DateTime, default=default_time)
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship('User', back_populates='reports')


class Person(Base):
    """ Create model for persons dates"""

    __tablename__ = 'persons'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    category = Column(String(255), default=Category.candidate.value)
    region_id = Column(Integer, ForeignKey('regions.id'))
    fullname = Column(String(255), nullable=False, index=True)
    previous = Column(Text)
    birthday = Column(Date, nullable=False)
    birthplace = Column(Text)
    country = Column(String(255))
    ext_country = Column(String(255))
    snils = Column(String(11))
    inn = Column(String(12))
    education = Column(Text)
    marital = Column(String(255))
    addition = Column(Text)
    path = Column(Text)
    status = Column(String(255), default=Status.new.value)
    create = Column(DateTime, default=default_time)
    update = Column(DateTime, onupdate=default_time)
    request_id = Column(Integer)
    documents = relationship('Document', back_populates='persons', 
                                cascade="all, delete, delete-orphan")
    addresses = relationship('Address', back_populates='persons', 
                                cascade="all, delete, delete-orphan")
    workplaces = relationship('Workplace', back_populates='persons', 
                                 cascade="all, delete, delete-orphan")
    contacts = relationship('Contact', back_populates='persons', 
                               cascade="all, delete, delete-orphan")
    staffs = relationship('Staff', back_populates='persons', 
                             cascade="all, delete, delete-orphan")
    checks = relationship('Check', back_populates='persons', 
                             cascade="all, delete, delete-orphan")
    registries = relationship('Registry', back_populates='persons', 
                                 cascade="all, delete, delete-orphan")
    poligrafs = relationship('Poligraf', back_populates='persons', 
                                cascade="all, delete, delete-orphan")
    inquiries = relationship('Inquiry', back_populates='persons', 
                                cascade="all, delete, delete-orphan")
    investigations = relationship('Investigation', back_populates='persons', 
                                     cascade="all, delete, delete-orphan")
    relations= relationship('Relation', back_populates='persons', 
                               cascade="all, delete, delete-orphan")
    affilation = relationship('Affilation', back_populates='affilation', 
                           cascade="all, delete, delete-orphan")
    search_vector = Column(TSVectorType('previous', 'fullname', 'inn', 'snils')) 
    
    def has_status(self, status):
        """
        Check if the current status of the object matches any of the given status values.
        Args:
            status (list): A list of status values to check against.
        Returns:
            bool: True if the current status matches any of the given status values, False otherwise.
        """
        return self.status in status


class Category(Base):

    __tablename__ = 'categories'
    
    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    category = ''


class Status(Base):
    
    __tablename__ = 'statuses'
    
    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    status = ''

class Region(Base):
    """ Create model for regions"""

    __tablename__ = 'regions'
    
    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    region = Column(String(255), unique=True)
    persons = relationship('Person', back_populates='persons')
   

class Staff(Base):
    """ Create model for staff"""

    __tablename__ = 'staffs'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    position = Column(Text)
    department = Column(Text)
    person_id = Column(Integer, ForeignKey('persons.id'))


class Document(Base):
    """ Create model for Document dates"""

    __tablename__ = 'documents'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    view = Column(String(255))
    series = Column(String(255))
    number = Column(String(255))
    agency = Column(Text)
    issue = Column(Date)
    person_id = Column(Integer, ForeignKey('persons.id'))


class Address(Base): 
    """ Create model for addresses"""

    __tablename__ = 'addresses'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    view = Column(String(255))
    region = Column(String(255))
    address = Column(Text)
    person_id = Column(Integer, ForeignKey('persons.id'))


class Contact(Base):  # создаем общий класс телефонного номера
    """ Create model for contacts"""

    __tablename__ = 'contacts'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    view = Column(String(255))
    contact = Column(String(255))
    person_id = Column(Integer, ForeignKey('persons.id'))


class Workplace(Base):
    """ Create model for workplaces"""

    __tablename__ = 'workplaces'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    start_date = Column(Date)
    end_date = Column(Date)
    workplace = Column(String(255))
    address = Column(Text)
    position = Column(Text)
    reason = Column(Text)
    person_id = Column(Integer, ForeignKey('persons.id'))


class Affilation(Base):
    """ Create model for affilation"""

    __tablename__ = 'affilation'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    view = Column(String(255))
    name = Column(Text)
    inn = Column(String(255))
    position = Column(Text)
    deadline = Column(Text, default=default_time)
    person_id = Column(Integer, ForeignKey('persons.id'))


class Relation(Base):
    """ Create model for relations"""

    __tablename__ = 'relations'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    relation = Column(String(255))
    relation_id = Column(Integer)
    person_id = Column(Integer, ForeignKey('persons.id'))
    
    
class Check(Base):  # модель данных проверки кандидатов
    """ Create model for persons checks"""

    __tablename__ = 'checks'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    workplace = Column(Text)
    employee = Column(Text)
    document = Column(Text)
    inn = Column(Text)
    debt = Column(Text)
    bankruptcy = Column(Text)
    bki = Column(Text)
    courts = Column(Text)
    affiliation = Column(Text)
    terrorist = Column(Text)
    mvd = Column(Text)
    internet = Column(Text)
    cronos = Column(Text)
    cros = Column(Text)
    addition = Column(Text)
    pfo = Column(Boolean, default=False)
    comments = Column(Text)
    conclusion = Column(String(255))
    officer = Column(String(255))
    deadline = Column(DateTime, default=default_time, 
                         onupdate=default_time)
    person_id = Column(Integer, ForeignKey('persons.id'))
    registries = relationship('Registry', back_populates='checks', 
                                 cascade="all, delete, delete-orphan")


class Conclusion(Base):
    
    __tablename__ = 'conclusions'
    
    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)


class Poligraf(Base):  # модель данных результаты ПФО
    """ Create model for poligraf"""

    __tablename__ = 'poligrafs'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    theme = Column(String(255))
    results = Column(Text)
    officer = Column(String(255))
    deadline = Column(Date, default=default_time)
    person_id = Column(Integer, ForeignKey('persons.id'))


class Investigation(Base):
    """ Create model for ivestigation"""
    
    __tablename__ = 'investigations'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    theme = Column(String(255))
    info = Column(Text)
    officer = Column(String(255))
    deadline = Column(Date, default=default_time, onupdate=default_time)
    person_id = Column(Integer, ForeignKey('persons.id'))


class Inquiry(Base):
    """ Create model for persons inquiries"""

    __tablename__ = 'inquiries'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    info = Column(Text)
    initiator = Column(String(255))
    source = Column(String(255))
    officer = Column(String(255))
    deadline = Column(Date, default=default_time)
    person_id = Column(Integer, ForeignKey('persons.id'))


class Connect(Base):
    """ Create model for persons connects"""
    
    __tablename__ = 'connects'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    company = Column(String(255))
    city = Column(String(255))
    fullname = Column(String(255))
    phone = Column(String(255))
    adding = Column(String(255))
    mobile = Column(String(255))
    mail = Column(String(255))
    comment = Column(Text)
    data = Column(Date, default=default_time, onupdate=default_time)
    group_id = Column(Integer, ForeignKey('groups.id'))
    search_vector = Column(TSVectorType('company', 'fullname', 'mobile', 'phone')) 
