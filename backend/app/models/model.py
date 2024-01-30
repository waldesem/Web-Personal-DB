from datetime import datetime
from typing import List
from sqlalchemy import select
from sqlalchemy_searchable import SearchQueryMixin, make_searchable
from sqlalchemy_utils.types import TSVectorType
from flask_sqlalchemy.query import Query
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa

from .. import db #, cache
from ..models.classes import Statuses


make_searchable(db.metadata)


def default_time():
    return datetime.now()


user_groups = db.Table(
    "user_groups",
    sa.Column("user_id", sa.ForeignKey("users.id"), primary_key=True),
    sa.Column("group_id", sa.ForeignKey("groups.id"), primary_key=True),
)


user_roles = db.Table(
    "user_roles",
    sa.Column("user_id", sa.ForeignKey("users.id"), primary_key=True),
    sa.Column("role_id", sa.ForeignKey("roles.id"), primary_key=True),
)


class Base(db.Model):
    __abstract__ = True


class Group(Base):
    """Create model for groups"""

    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    group: Mapped[str] = mapped_column(sa.String(255), unique=True)

    def get_group(self, group):
        return db.session.execute(
            select(Group).filter_by(group=group)
        ).scalar_one_or_none()


class Role(Base):
    """Create model for roles"""

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    role: Mapped[str] = mapped_column(sa.String(255), unique=True)

    def get_role(self, role):
        return db.session.execute(
            select(Role).filter_by(role=role)
        ).scalar_one_or_none()


class User(Base):
    """Create model for users"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    fullname: Mapped[str] = mapped_column(sa.String(255))
    username: Mapped[str] = mapped_column(sa.String(255), unique=True)
    password: Mapped[str] = mapped_column(sa.LargeBinary)
    email: Mapped[str] = mapped_column(sa.String(255), unique=True)
    pswd_create: Mapped[datetime] = mapped_column(sa.DateTime, default=default_time)
    pswd_change: Mapped[datetime] = mapped_column(sa.DateTime)
    last_login: Mapped[datetime] = mapped_column(sa.DateTime)
    blocked: Mapped[bool] = mapped_column(sa.Boolean(), default=False)
    deleted: Mapped[bool] = mapped_column(sa.Boolean(), default=False)
    attempt: Mapped[int] = mapped_column(sa.Integer(), default=0)
    search_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("fullname", "username", "email")
    )
    messages: Mapped[List["Message"]] = relationship(
        back_populates="users", cascade="all, delete, delete-orphan"
    )
    roles: Mapped[List["Role"]] = relationship(
        back_populates="users", secondary=user_roles, lazy="dynamic"
    )
    groups: Mapped[List["Group"]] = relationship(
        back_populates="users", secondary=user_groups, lazy="dynamic"
    )

    @staticmethod
    def get_user(user_name):
        return db.session.execute(
            select(User).filter_by(username=user_name)
        ).scalar_one_or_none()

    # @cache.memoize(60)
    # def has_group(self, *groups):
    #     """
    #     Checks if the given group exists in the list of groups.
    #     """
    #     return any(g.group in groups for g in self.groups)

    # @cache.memoize(60)
    # def has_role(self, *roles):
    #     """
    #     A function that checks if the user has a specific role.
    #     """
    #     return any(r.role in roles for r in self.roles)


class Message(Base):
    """Create model for messages"""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    title: Mapped[str] = mapped_column(sa.String(255))
    message: Mapped[str] = mapped_column(sa.Text)
    status: Mapped[str] = mapped_column(sa.String(255), default=Statuses.new.name)
    created: Mapped[datetime] = mapped_column(sa.DateTime, default=default_time)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"))


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    category: Mapped[str] = mapped_column(sa.String(255))
    persons: Mapped[List["Person"]] = relationship(back_populates="categories")

    def get_id(self, category):
        return db.session.execute(
            select(Category.id).filter(Category.category == category)
        ).scalar_one_or_none()


class Status(Base):
    __tablename__ = "statuses"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    status: Mapped[str] = mapped_column(sa.String(255))
    persons: Mapped[List["Person"]] = relationship(back_populates="statuses")

    def get_id(self, status):
        return db.session.execute(
            select(Status.id).filter(Status.status == status)
        ).scalar_one_or_none()


class Region(Base):
    """Create model for regions"""

    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(
        nullable=True, unique=True, primary_key=True, autoincrement=True
    )
    region: Mapped[str] = mapped_column(sa.String(255))
    persons: Mapped[List["Person"]] = relationship(back_populates="regions")

    def get_id(self, region):
        return db.session.execute(
            select(Region.id).filter(Region.region == region)
        ).scalar_one_or_none()


class PersonQuery(Query, SearchQueryMixin):
    """Class for searchable Connect table (only postgresql)"""

    pass


class Person(Base):
    """Create model for persons dates"""

    query_class = PersonQuery

    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    category_id: Mapped[int] = mapped_column(sa.ForeignKey("categories.id"))
    region_id: Mapped[int] = mapped_column(sa.ForeignKey("regions.id"))
    fullname: Mapped[str] = mapped_column(sa.String(255), nullable=False, index=True)
    previous: Mapped[str] = mapped_column(sa.Text, nullable=True)
    birthday: Mapped[datetime] = mapped_column(sa.Date, nullable=False, index=True)
    birthplace: Mapped[str] = mapped_column(sa.Text, nullable=True)
    country: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    ext_country: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    snils: Mapped[str] = mapped_column(sa.String(11), nullable=True)
    inn: Mapped[str] = mapped_column(sa.String(12), nullable=True)
    education: Mapped[str] = mapped_column(sa.Text, nullable=True)
    marital: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    addition: Mapped[str] = mapped_column(sa.Text, nullable=True)
    path: Mapped[str] = mapped_column(sa.Text, nullable=True)
    status_id: Mapped[int] = mapped_column(sa.ForeignKey("statuses.id"))
    created: Mapped[datetime] = mapped_column(
        sa.Date, default=default_time, nullable=True
    )
    updated: Mapped[datetime] = mapped_column(
        sa.Date, onupdate=default_time, nullable=True
    )
    search_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("previous", "fullname", "birthday", "inn", "snils")
    )
    staffs: Mapped[List["Staff"]] = relationship(
        back_populates="persons", cascade="all, delete, delete-orphan"
    )
    documents: Mapped[List["Document"]] = relationship(
        back_populates="persons", cascade="all, delete, delete-orphan"
    )
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="persons", cascade="all, delete, delete-orphan"
    )
    workplaces: Mapped[List["Workplace"]] = relationship(
        back_populates="persons", cascade="all, delete, delete-orphan"
    )
    contacts: Mapped[List["Contact"]] = relationship(
        back_populates="persons", cascade="all, delete, delete-orphan"
    )
    affilations: Mapped[List["Affilation"]] = relationship(
        back_populates="persons", cascade="all, delete, delete-orphan"
    )
    relations: Mapped[List["Relation"]] = relationship(
        back_populates="persons", cascade="all, delete, delete-orphan"
    )
    checks: Mapped[List["Check"]] = relationship(
        back_populates="persons", cascade="all, delete, delete-orphan"
    )
    robots: Mapped[List["Robot"]] = relationship(
        back_populates="persons", cascade="all, delete, delete-orphan"
    )
    inquiries: Mapped[List["Inquiry"]] = relationship(
        back_populates="persons", cascade="all, delete, delete-orphan"
    )
    poligrafs: Mapped[List["Poligraf"]] = relationship(
        back_populates="persons", cascade="all, delete, delete-orphan"
    )
    investigations: Mapped[List["Investigation"]] = relationship(
        back_populates="persons", cascade="all, delete, delete-orphan"
    )
    categories: Mapped["Category"] = relationship(back_populates="persons")
    statuses: Mapped["Status"] = relationship(back_populates="persons")
    regions: Mapped["Region"] = relationship(back_populates="persons")

    def has_status(self, *statuses):
        """
        Check if the current status of the object matches any of the given status values.
        """
        return any(
            self.status_id
            == [
                db.session.execute(select(Status).filter_by(status=status))
                .scalar_one_or_none()
                .id
                for status in statuses
            ]
        )

    def has_category(self, *args):
        """
        Check if the current category of the object matches any of the given category values.
        """
        return any(
            self.category_id
            == [
                db.session.execute(
                    select(Category).filter(Category.category.in_(category))
                )
                .scalar_one_or_none()
                .id
                for category in args
            ]
        )

    def has_region(self, *args):
        """
        Check if the current region of the object matches any of the given region values.
        """
        return any(
            self.region_id
            == [
                db.session.execute(
                    select(Region).filter(Region.region.in_(region))
                ).scalar_one_or_none()
                for region in args
            ]
        )


class Staff(Base):
    """Create model for staff"""

    __tablename__ = "staffs"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    position: Mapped[str] = mapped_column(sa.Text, nullable=True)
    department: Mapped[str] = mapped_column(sa.Text, nullable=True)
    person_id: Mapped[int] = mapped_column(sa.ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="staffs")


class DocumentQuery(Query, SearchQueryMixin):
    """Class for searchable Connect table (only postgresql)"""

    pass


class Document(Base):
    """Create model for Document dates"""

    query_class = DocumentQuery

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    view: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    series: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    number: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    agency: Mapped[str] = mapped_column(sa.Text, nullable=True)
    issue: Mapped[datetime] = mapped_column(sa.Date, nullable=True)
    person_id: Mapped[int] = mapped_column(sa.ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="documents")
    search_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("series", "number")
    )


class Address(Base):
    """Create model for addresses"""

    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    view: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    region: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    address: Mapped[str] = mapped_column(sa.Text, nullable=True)
    person_id: Mapped[int] = mapped_column(sa.ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="addresses")


class Contact(Base):  # создаем общий класс телефонного номера
    """Create model for contacts"""

    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    view: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    contact: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    person_id: Mapped[int] = mapped_column(sa.ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="contacts")


class Workplace(Base):
    """Create model for workplaces"""

    __tablename__ = "workplaces"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    start_date: Mapped[datetime] = mapped_column(sa.Date, nullable=True)
    end_date: Mapped[datetime] = mapped_column(sa.Date, nullable=True)
    workplace: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    address: Mapped[str] = mapped_column(sa.Text, nullable=True)
    position: Mapped[str] = mapped_column(sa.Text, nullable=True)
    reason: Mapped[str] = mapped_column(sa.Text, nullable=True)
    person_id: Mapped[int] = mapped_column(sa.ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="workplaces")


class Affilation(Base):
    """Create model for affilations"""

    __tablename__ = "affilations"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    view: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    name: Mapped[str] = mapped_column(sa.Text, nullable=True)
    inn: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    position: Mapped[str] = mapped_column(sa.Text, nullable=True)
    deadline: Mapped[datetime] = mapped_column(
        sa.Date, default=default_time, nullable=True
    )
    person_id: Mapped[int] = mapped_column(sa.ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="affilations")


class Relation(Base):
    """Create model for relations"""

    __tablename__ = "relations"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    relation: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    relation_id: Mapped[int] = mapped_column(sa.Integer, nullable=True)
    person_id: Mapped[int] = mapped_column(sa.ForeignKey("persons.id"))


class Check(Base):
    """Create model for persons checks"""

    __tablename__ = "checks"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    workplace: Mapped[str] = mapped_column(sa.Text, nullable=True)
    document: Mapped[str] = mapped_column(sa.Text, nullable=True)
    inn: Mapped[str] = mapped_column(sa.Text, nullable=True)
    debt: Mapped[str] = mapped_column(sa.Text, nullable=True)
    bankruptcy: Mapped[str] = mapped_column(sa.Text, nullable=True)
    bki: Mapped[str] = mapped_column(sa.Text, nullable=True)
    courts: Mapped[str] = mapped_column(sa.Text, nullable=True)
    affilation: Mapped[str] = mapped_column(sa.Text, nullable=True)
    terrorist: Mapped[str] = mapped_column(sa.Text, nullable=True)
    mvd: Mapped[str] = mapped_column(sa.Text, nullable=True)
    internet: Mapped[str] = mapped_column(sa.Text, nullable=True)
    cronos: Mapped[str] = mapped_column(sa.Text, nullable=True)
    cros: Mapped[str] = mapped_column(sa.Text, nullable=True)
    addition: Mapped[str] = mapped_column(sa.Text, nullable=True)
    pfo: Mapped[bool] = mapped_column(sa.Boolean, nullable=True)
    comments: Mapped[str] = mapped_column(sa.Text, nullable=True)
    conclusion: Mapped[int] = mapped_column(sa.ForeignKey("conclusions.id"))
    officer: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    deadline: Mapped[datetime] = mapped_column(
        sa.Date, default=default_time, onupdate=default_time
    )
    person_id: Mapped[int] = mapped_column(sa.ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="checks")
    conclusions: Mapped["Conclusion"] = relationship(back_populates="checks")


class Robot(Base):
    """Create model for robots"""

    __tablename__ = "robots"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    employee: Mapped[str] = mapped_column(sa.Text, nullable=True)
    inn: Mapped[str] = mapped_column(sa.Text, nullable=True)
    bankruptcy: Mapped[str] = mapped_column(sa.Text, nullable=True)
    bki: Mapped[str] = mapped_column(sa.Text, nullable=True)
    courts: Mapped[str] = mapped_column(sa.Text, nullable=True)
    terrorist: Mapped[str] = mapped_column(sa.Text, nullable=True)
    mvd: Mapped[str] = mapped_column(sa.Text, nullable=True)
    deadline: Mapped[datetime] = mapped_column(
        sa.Date, default=default_time, nullable=True
    )
    person_id: Mapped[int] = mapped_column(sa.ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="robots")


class Conclusion(Base):
    __tablename__ = "conclusions"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    conclusion: Mapped[str] = mapped_column(sa.String(255))
    checks: Mapped[List["Check"]] = relationship(back_populates="conclusions")

    def get_id(self, conclusion):
        return (
            db.session.execute(
                select(Conclusion).filter(Conclusion.conclusion == conclusion)
            )
            .scalar_one_or_none()
            .id
        )


class Poligraf(Base):  # модель данных результаты ПФО
    """Create model for poligraf"""

    __tablename__ = "poligrafs"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    theme: Mapped[str] = mapped_column(sa.String(255))
    results: Mapped[str] = mapped_column(sa.Text)
    officer: Mapped[str] = mapped_column(sa.String(255))
    deadline: Mapped[datetime] = mapped_column(sa.Date, default=default_time)
    person_id: Mapped[int] = mapped_column(sa.ForeignKey("persons.id"))


class Investigation(Base):
    """Create model for ivestigation"""

    __tablename__ = "investigations"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    theme: Mapped[str] = mapped_column(sa.String(255))
    info: Mapped[str] = mapped_column(sa.Text)
    officer: Mapped[str] = mapped_column(sa.String(255))
    deadline: Mapped[datetime] = mapped_column(sa.Date, default=default_time)
    person_id: Mapped[int] = mapped_column(sa.ForeignKey("persons.id"))


class Inquiry(Base):
    """Create model for persons inquiries"""

    __tablename__ = "inquiries"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    info: Mapped[str] = mapped_column(sa.Text, nullable=True)
    initiator: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    source: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    officer: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    deadline: Mapped[datetime] = mapped_column(
        sa.Date, default=default_time, nullable=True
    )
    person_id: Mapped[int] = mapped_column(sa.ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="inquiries")


class ConnectQuery(Query, SearchQueryMixin):
    """Class for searchable Connect table (only postgresql)"""

    pass


class Connect(Base):
    """Create model for persons connects"""

    query_class = ConnectQuery

    __tablename__ = "connects"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    company: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    city: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    fullname: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    phone: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    adding: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    mobile: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    mail: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    comment: Mapped[str] = mapped_column(sa.Text, nullable=True)
    data: Mapped[datetime] = mapped_column(
        sa.Date, default=default_time, onupdate=default_time, nullable=True
    )
    search_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("company", "fullname", "mobile", "phone")
    )


db.configure_mappers()  # very important!
