import os
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, Boolean, \
      Text, Date, ForeignKey, Table
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base, configure_mappers, relationship
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType

from .. import cache
from ..models.classes import Statuses


engine = create_async_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
make_searchable(Base.metadata)
configure_mappers()

def default_time():
    return datetime.now()


user_groups = Table(
    'user_groups',
    Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('group_id', ForeignKey('groups.id'))
)
    
    
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('role_id', ForeignKey('roles.id'))
)
       

class Group(Base):
    """ Create model for groups"""

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    group = Column(String(255), unique=True)
    users = relationship('User', secondary=user_groups, back_populates='groups')


class Role(Base):
    """ Create model for roles"""

    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    role = Column(String(255), unique=True)
    users = relationship('User', secondary=user_roles, back_populates='roles')


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
    roles = relationship('Role', secondary=user_roles, back_populates='users')
    groups = relationship('Group', secondary=user_groups, back_populates='users')
    messages = relationship('Message', back_populates='users', 
                            cascade="all, delete, delete-orphan")
    
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
    

class Message(Base):
    """ Create model for messages"""

    __tablename__ = 'messages'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    title = Column(String(255))
    report = Column(Text)
    status = Column(String(255), default=Statuses.new.value)
    create = Column(DateTime, default=default_time)
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship('User', back_populates='messages')


class Person(Base):
    """ Create model for persons dates"""

    __tablename__ = 'persons'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
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
    status_id = Column(Integer, ForeignKey('statuses.id'))
    create = Column(DateTime, default=default_time)
    update = Column(DateTime, onupdate=default_time)
    request_id = Column(Integer)
    regions = relationship('Region', back_populates='persons')
    categories = relationship('Category', back_populates='persons')
    statuses = relationship('Status', back_populates='persons')
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
    poligrafs = relationship('Poligraf', back_populates='persons', 
                                cascade="all, delete, delete-orphan")
    inquiries = relationship('Inquiry', back_populates='persons', 
                                cascade="all, delete, delete-orphan")
    investigations = relationship('Investigation', back_populates='persons', 
                                     cascade="all, delete, delete-orphan")
    relations = relationship('Relation', back_populates='persons', 
                               cascade="all, delete, delete-orphan")
    affilations = relationship('Affilation', back_populates='persons', 
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
    
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    category = Column(String(255))
    persons = relationship('Person', back_populates='categories')


class Status(Base):
    
    __tablename__ = 'statuses'
    
    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    status = Column(String(255))
    persons = relationship('Person', back_populates='statuses')


class Region(Base):
    """ Create model for regions"""

    __tablename__ = 'regions'
    
    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    region = Column(String(255), unique=True)
    persons = relationship('Person', back_populates='regions')
   

class Staff(Base):
    """ Create model for staff"""

    __tablename__ = 'staffs'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    position = Column(Text)
    department = Column(Text)
    person_id = Column(Integer, ForeignKey('persons.id'))
    persons = relationship('Person', back_populates='staffs')


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
    persons = relationship('Person', back_populates='documents')
    search_vector = Column(TSVectorType('series', 'number')) 

combined_search_vector = Person.search_vector | Document.search_vector


class Address(Base): 
    """ Create model for addresses"""

    __tablename__ = 'addresses'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    view = Column(String(255))
    region = Column(String(255))
    address = Column(Text)
    person_id = Column(Integer, ForeignKey('persons.id'))
    persons = relationship('Person', back_populates='addresses')


class Contact(Base):  # создаем общий класс телефонного номера
    """ Create model for contacts"""

    __tablename__ = 'contacts'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    view = Column(String(255))
    contact = Column(String(255))
    person_id = Column(Integer, ForeignKey('persons.id'))
    persons = relationship('Person', back_populates='contacts')
    

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
    persons = relationship('Person', back_populates='workplaces')
    

class Affilation(Base):
    """ Create model for affilations"""

    __tablename__ = 'affilations'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    view = Column(String(255))
    name = Column(Text)
    inn = Column(String(255))
    position = Column(Text)
    deadline = Column(Text, default=default_time)
    person_id = Column(Integer, ForeignKey('persons.id'))
    persons = relationship('Person', back_populates='affilations')
    

class Relation(Base):
    """ Create model for relations"""

    __tablename__ = 'relations'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    relation = Column(String(255))
    relation_id = Column(Integer)
    person_id = Column(Integer, ForeignKey('persons.id'))
    persons = relationship('Person', back_populates='relations')
    
    
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
    conclusion = Column(Integer, ForeignKey('conclusions.id'))
    officer = Column(String(255))
    deadline = Column(DateTime, default=default_time, 
                         onupdate=default_time)
    person_id = Column(Integer, ForeignKey('persons.id'))
    persons = relationship('Person', back_populates='checks')   
    conclusions = relationship('Conclusion', back_populates='checks')   

class Conclusion(Base):
    
    __tablename__ = 'conclusions'
    
    id = Column(Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    conclusion = Column(String(255))
    checks = relationship('Check', back_populates='conclusions')   


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
    persons = relationship('Person', back_populates='poligrafs')   


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
    persons = relationship('Person', back_populates='investigations') 
    

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
    persons = relationship('Person', back_populates='inquiries')   


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
    search_vector = Column(TSVectorType('company', 'fullname', 'mobile', 'phone'))

