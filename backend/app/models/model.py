from datetime import datetime
from sqlalchemy import select
from sqlalchemy_searchable import SearchQueryMixin, make_searchable
from sqlalchemy_utils.types import TSVectorType
from flask_sqlalchemy.query import Query

from .. import db, cache
from ..models.classes import Statuses


make_searchable(db.metadata)


def default_time():
    return datetime.now()

                
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
       

class Base(db.Model):
    
    __abstract__ = True


class Group(Base):
    """ Create model for groups"""

    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(255), unique=True)
    
    def get_group(self, group):
        return db.session.execute(
                select(Group)
                .filter_by(group=group)
                ).scalar_one_or_none()

class Role(Base):
    """ Create model for roles"""

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(255), unique=True)

    def get_role(self, role):
        return db.session.execute(
                select(Role)
                .filter_by(role=role)
                ).scalar_one_or_none()


class User(Base):
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
    messages = db.relationship('Message', backref='users', 
                              cascade="all, delete, delete-orphan")
    roles = db.relationship('Role', secondary=user_roles, 
                            backref=db.backref('users', lazy='dynamic'))
    groups = db.relationship('Group', secondary=user_groups, 
                             backref=db.backref('users', lazy='dynamic'))
    

    @staticmethod
    def get_user(user_name):
        return db.session.execute(
            select(User)
            .filter_by(username=user_name)
            ).scalar_one_or_none()
    
    @cache.memoize(60)
    def has_group(self, *groups):
        """
        Checks if the given group exists in the list of groups.
        """
        return any(g.group in groups for g in self.groups)
    
    @cache.memoize(60)
    def has_role(self, *roles):
        """
        A function that checks if the user has a specific role.
        """
        return any(r.role in roles for r in self.roles)
    

class Message(Base):
    """ Create model for messages"""

    __tablename__ = 'messages'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    title = db.Column(db.String(255))
    message = db.Column(db.Text)
    status = db.Column(db.String(255), default=Statuses.new.name)
    create = db.Column(db.DateTime, default=default_time)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Category(Base):

    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    category = db.Column(db.String(255))
    persons = db.relationship('Person', backref='categories')

    def get_id(self, category):
        print(db.session.execute(
            select(Category.id)
            .filter(Category.category == category)
            ).scalar_one_or_none())
        return db.session.execute(
            select(Category.id)
            .filter(Category.category == category)
            ).scalar_one_or_none()


class Status(Base):
    
    __tablename__ = 'statuses'
    
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    status = db.Column(db.String(255))
    persons = db.relationship('Person', backref='statuses')

    def get_id(self, status):
        return db.session.execute(
            select(Status.id)
            .filter(Status.status == status)
            ).scalar_one_or_none()


class Region(Base):
    """ Create model for regions"""

    __tablename__ = 'regions'
    
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    region = db.Column(db.String(255), unique=True)
    persons = db.relationship('Person', backref='regions')
   
    def get_id(self, region):
        return db.session.execute(
            select(Region.id)
            .filter(Region.region == region)
            ).scalar_one_or_none()


class PersonQuery(Query, SearchQueryMixin):
    """ Class for searchable Connect table (only postgresql)"""
    pass


class Person(Base):
    """ Create model for persons dates"""
    query_class = PersonQuery

    __tablename__ = 'persons'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    fullname = db.Column(db.String(255), nullable=False, index=True)
    previous = db.Column(db.Text)
    birthday = db.Column(db.Date, nullable=False)
    birthplace = db.Column(db.Text)
    country = db.Column(db.String(255))
    ext_country = db.Column(db.String(255))
    snils = db.Column(db.String(11))
    inn = db.Column(db.String(12))
    education = db.Column(db.Text)
    marital = db.Column(db.String(255))
    addition = db.Column(db.Text)
    path = db.Column(db.Text)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'))
    create = db.Column(db.DateTime, default=default_time)
    update = db.Column(db.DateTime, onupdate=default_time)
    search_vector = db.Column(TSVectorType('previous', 'fullname', 'inn', 'snils')) 
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
    robots = db.relationship('Robot', backref='persons',
                             cascade="all, delete, delete-orphan")
    poligrafs = db.relationship('Poligraf', backref='persons', 
                                cascade="all, delete, delete-orphan")
    inquiries = db.relationship('Inquiry', backref='persons', 
                                cascade="all, delete, delete-orphan")
    investigations = db.relationship('Investigation', backref='persons', 
                                     cascade="all, delete, delete-orphan")
    relations = db.relationship('Relation', backref='persons', 
                               cascade="all, delete, delete-orphan")
    affilations = db.relationship('Affilation', backref='persons', 
                           cascade="all, delete, delete-orphan")

    def has_status(self, *statuses):
        """
        Check if the current status of the object matches any of the given status values.
        """
        return any(self.status_id == [db.session.execute(
            select(Status)
            .filter_by(status=status)
            ).scalar_one_or_none().id for status in statuses])
    
    def has_category(self, *args):
        """
        Check if the current category of the object matches any of the given category values.
        """
        return any(self.category_id == [db.session.execute(
            select(Category)
            .filter(Category.category.in_(category))
            ).scalar_one_or_none().id for category in args])  
    
    def has_region(self, *args):
        """
        Check if the current region of the object matches any of the given region values.
        """
        return any(self.region_id == [db.session.execute(
            select(Region)
            .filter(Region.region.in_(region))
            ).scalar_one_or_none() for region in args])


class Staff(Base):
    """ Create model for staff"""

    __tablename__ = 'staffs'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    position = db.Column(db.Text)
    department = db.Column(db.Text)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class DocumentQuery(Query, SearchQueryMixin):
    """ Class for searchable Connect table (only postgresql)"""
    pass


class Document(Base):
    """ Create model for Document dates"""

    query_class = DocumentQuery

    __tablename__ = 'documents'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    view = db.Column(db.String(255))
    series = db.Column(db.String(255))
    number = db.Column(db.String(255))
    agency = db.Column(db.Text)
    issue = db.Column(db.Date)
    search_vector = db.Column(TSVectorType('series', 'number',))
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    

class Address(Base): 
    """ Create model for addresses"""

    __tablename__ = 'addresses'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    view = db.Column(db.String(255))
    region = db.Column(db.String(255))
    address = db.Column(db.Text)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Contact(Base):  # создаем общий класс телефонного номера
    """ Create model for contacts"""

    __tablename__ = 'contacts'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    view = db.Column(db.String(255))
    contact = db.Column(db.String(255))
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    

class Workplace(Base):
    """ Create model for workplaces"""

    __tablename__ = 'workplaces'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    workplace = db.Column(db.String(255))
    address = db.Column(db.Text)
    position = db.Column(db.Text)
    reason = db.Column(db.Text)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    

class Affilation(Base):
    """ Create model for affilations"""

    __tablename__ = 'affilations'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    view = db.Column(db.String(255))
    name = db.Column(db.Text)
    inn = db.Column(db.String(255))
    position = db.Column(db.Text)
    deadline = db.Column(db.Text, default=default_time)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    

class Relation(Base):
    """ Create model for relations"""

    __tablename__ = 'relations'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    relation = db.Column(db.String(255))
    relation_id = db.Column(db.Integer)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    
    
class Check(Base):  # модель данных проверки кандидатов
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
    pfo = db.Column(db.Boolean, default=False)
    comments = db.Column(db.Text)
    conclusion = db.Column(db.Integer, db.ForeignKey('conclusions.id'))
    officer = db.Column(db.String(255))
    deadline = db.Column(db.DateTime, default=default_time, 
                         onupdate=default_time)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Robot(Base):
    """ Create model for robots"""

    __tablename__ = 'robots'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
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
    deadline = db.Column(db.DateTime, default=default_time)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Conclusion(Base):
    
    __tablename__ = 'conclusions'
    
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    conclusion = db.Column(db.String(255))
    checks = db.relationship('Check', backref='conclusions')   

    def get_id(self, conclusion):
        return db.session.execute(
            select(Conclusion)
            .filter(Conclusion.conclusion == conclusion)
            ).scalar_one_or_none().id


class Poligraf(Base):  # модель данных результаты ПФО
    """ Create model for poligraf"""

    __tablename__ = 'poligrafs'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    theme = db.Column(db.String(255))
    results = db.Column(db.Text)
    officer = db.Column(db.String(255))
    deadline = db.Column(db.Date, default=default_time)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


class Investigation(Base):
    """ Create model for ivestigation"""
    
    __tablename__ = 'investigations'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, 
                   autoincrement=True)
    theme = db.Column(db.String(255))
    info = db.Column(db.Text)
    officer = db.Column(db.String(255))
    deadline = db.Column(db.Date, default=default_time, onupdate=default_time)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    

class Inquiry(Base):
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


class Connect(Base):
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
    search_vector = db.Column(TSVectorType('company', 'fullname', 'mobile', 'phone')) 


combined_search_vector = Person.search_vector | Document.search_vector

db.configure_mappers()  # very important!