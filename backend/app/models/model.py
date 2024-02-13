from datetime import date, datetime
from typing import List

from sqlalchemy import select
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    LargeBinary,
    Date,
    DateTime,
    Text,
    Boolean,
)

from .. import db
from ..models.classes import Statuses


make_searchable(db.metadata)


def default_time():
    return datetime.now()


class Base(db.Model):
    __abstract__ = True


user_groups = db.Table(
    "user_groups",
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)


user_roles = db.Table(
    "user_roles",
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)


class Group(Base):
    """Create model for groups"""

    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    group: Mapped[str] = mapped_column(String(255), unique=True)
    users: Mapped[List["User"]] = relationship(
        back_populates="groups", secondary=user_groups, lazy="dynamic"
    )


class Role(Base):
    """Create model for roles"""

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    role: Mapped[str] = mapped_column(String(255), unique=True)
    users: Mapped[List["User"]] = relationship(
        back_populates="roles", secondary=user_roles, lazy="dynamic"
    )


class User(Base):
    """Create model for users"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    fullname: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(LargeBinary)
    email: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    pswd_create: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, default=default_time
    )
    pswd_change: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    blocked: Mapped[bool] = mapped_column(Boolean(), default=False)
    deleted: Mapped[bool] = mapped_column(Boolean(), default=False)
    attempt: Mapped[int] = mapped_column(Integer(), default=0)
    messages: Mapped[List["Message"]] = relationship(back_populates="users")
    persons: Mapped[List["Person"]] = relationship(back_populates="users")
    roles: Mapped[List["Role"]] = relationship(
        back_populates="users", secondary=user_roles, lazy="dynamic"
    )
    groups: Mapped[List["Group"]] = relationship(
        back_populates="users", secondary=user_groups, lazy="dynamic"
    )
    search_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("fullname", "username", "email")
    )

    @staticmethod
    def get_user(user_name):
        return db.session.execute(
            select(User).filter_by(username=user_name)
        ).scalar_one_or_none()


class Message(Base):
    """Create model for messages"""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    title: Mapped[str] = mapped_column(String(255))
    message: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(255), default=Statuses.new.name)
    created: Mapped[datetime] = mapped_column(DateTime, default=default_time)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    users: Mapped["User"] = relationship(back_populates="messages")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    category: Mapped[str] = mapped_column(String(255))
    persons: Mapped[List["Person"]] = relationship(back_populates="categories")

    @staticmethod
    def get_id(category):
        return db.session.execute(
            select(Category.id).filter(Category.category == category)
        ).scalar_one_or_none()


class Status(Base):
    __tablename__ = "statuses"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    status: Mapped[str] = mapped_column(String(255))
    persons: Mapped[List["Person"]] = relationship(back_populates="statuses")

    @staticmethod
    def get_id(status):
        return db.session.execute(
            select(Status.id).filter(Status.status == status)
        ).scalar_one_or_none()


class Region(Base):
    """Create model for regions"""

    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    region: Mapped[str] = mapped_column(String(255))
    persons: Mapped[List["Person"]] = relationship(back_populates="regions")

    @staticmethod
    def get_id(region):
        return db.session.execute(
            select(Region.id).filter(Region.region == region)
        ).scalar_one_or_none()


class Person(Base):
    """Create model for persons dates"""

    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"), nullable=True)
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    fullname: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    previous: Mapped[str] = mapped_column(Text, nullable=True)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    birthplace: Mapped[str] = mapped_column(Text, nullable=True)
    country: Mapped[str] = mapped_column(String(255), nullable=True)
    ext_country: Mapped[str] = mapped_column(String(255), nullable=True)
    snils: Mapped[str] = mapped_column(String(11), nullable=True)
    inn: Mapped[str] = mapped_column(String(12), nullable=True)
    education: Mapped[str] = mapped_column(Text, nullable=True)
    marital: Mapped[str] = mapped_column(String(255), nullable=True)
    addition: Mapped[str] = mapped_column(Text, nullable=True)
    path: Mapped[str] = mapped_column(Text, nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime, default=default_time, nullable=True
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime, onupdate=default_time, nullable=True
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
    search_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType(
            "previous",
            "fullname",
            "inn",
            "snils",
        )
    )
    categories: Mapped["Category"] = relationship(back_populates="persons")
    statuses: Mapped["Status"] = relationship(back_populates="persons")
    regions: Mapped["Region"] = relationship(back_populates="persons")
    users: Mapped["User"] = relationship(back_populates="persons")

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

    @staticmethod
    def has_category(*args):
        """
        Check if the current category of the object matches any of the given category values.
        """
        return any(
            Person.category_id
            == [
                db.session.execute(
                    select(Category).filter(Category.category.in_(category))
                )
                .scalar_one_or_none()
                .id
                for category in args
            ]
        )

    @staticmethod
    def has_region(*args):
        """
        Check if the current region of the object matches any of the given region values.
        """
        return any(
            Person.region_id
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
    position: Mapped[str] = mapped_column(Text, nullable=True)
    department: Mapped[str] = mapped_column(Text, nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="staffs")


class Document(Base):
    """Create model for Document dates"""

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    view: Mapped[str] = mapped_column(String(255), nullable=True)
    series: Mapped[str] = mapped_column(String(255), nullable=True)
    number: Mapped[str] = mapped_column(String(255), nullable=True)
    agency: Mapped[str] = mapped_column(Text, nullable=True)
    issue: Mapped[datetime] = mapped_column(Date, nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
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
    view: Mapped[str] = mapped_column(String(255), nullable=True)
    region: Mapped[str] = mapped_column(String(255), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="addresses")


class Contact(Base):
    """Create model for contacts"""

    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    view: Mapped[str] = mapped_column(String(255), nullable=True)
    contact: Mapped[str] = mapped_column(String(255), nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="contacts")


class Workplace(Base):
    """Create model for workplaces"""

    __tablename__ = "workplaces"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    start_date: Mapped[datetime] = mapped_column(Date, nullable=True)
    end_date: Mapped[datetime] = mapped_column(Date, nullable=True)
    workplace: Mapped[str] = mapped_column(String(255), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    position: Mapped[str] = mapped_column(Text, nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="workplaces")


class Affilation(Base):
    """Create model for affilations"""

    __tablename__ = "affilations"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    view: Mapped[str] = mapped_column(String(255), nullable=True)
    name: Mapped[str] = mapped_column(Text, nullable=True)
    inn: Mapped[str] = mapped_column(String(255), nullable=True)
    position: Mapped[str] = mapped_column(Text, nullable=True)
    deadline: Mapped[datetime] = mapped_column(
        Date, default=default_time, nullable=True
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="affilations")


class Relation(Base):
    """Create model for relations"""

    __tablename__ = "relations"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    relation: Mapped[str] = mapped_column(String(255), nullable=True)
    relation_id: Mapped[int] = mapped_column(Integer, nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="relations")


class Check(Base):
    """Create model for persons checks"""

    __tablename__ = "checks"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    workplace: Mapped[str] = mapped_column(Text, nullable=True)
    document: Mapped[str] = mapped_column(Text, nullable=True)
    inn: Mapped[str] = mapped_column(Text, nullable=True)
    debt: Mapped[str] = mapped_column(Text, nullable=True)
    bankruptcy: Mapped[str] = mapped_column(Text, nullable=True)
    bki: Mapped[str] = mapped_column(Text, nullable=True)
    courts: Mapped[str] = mapped_column(Text, nullable=True)
    affilation: Mapped[str] = mapped_column(Text, nullable=True)
    terrorist: Mapped[str] = mapped_column(Text, nullable=True)
    mvd: Mapped[str] = mapped_column(Text, nullable=True)
    internet: Mapped[str] = mapped_column(Text, nullable=True)
    cronos: Mapped[str] = mapped_column(Text, nullable=True)
    cros: Mapped[str] = mapped_column(Text, nullable=True)
    addition: Mapped[str] = mapped_column(Text, nullable=True)
    pfo: Mapped[bool] = mapped_column(Boolean, nullable=True)
    comments: Mapped[str] = mapped_column(Text, nullable=True)
    conclusion_id: Mapped[int] = mapped_column(ForeignKey("conclusions.id"))
    officer: Mapped[str] = mapped_column(String(255), nullable=True)
    deadline: Mapped[datetime] = mapped_column(
        Date, default=default_time, onupdate=default_time
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="checks")
    conclusions: Mapped["Conclusion"] = relationship(back_populates="checks")


class Robot(Base):
    """Create model for robots"""

    __tablename__ = "robots"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    employee: Mapped[str] = mapped_column(Text, nullable=True)
    inn: Mapped[str] = mapped_column(Text, nullable=True)
    bankruptcy: Mapped[str] = mapped_column(Text, nullable=True)
    bki: Mapped[str] = mapped_column(Text, nullable=True)
    courts: Mapped[str] = mapped_column(Text, nullable=True)
    terrorist: Mapped[str] = mapped_column(Text, nullable=True)
    mvd: Mapped[str] = mapped_column(Text, nullable=True)
    deadline: Mapped[datetime] = mapped_column(
        Date, default=default_time, nullable=True
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="robots")


class Conclusion(Base):
    __tablename__ = "conclusions"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    conclusion: Mapped[str] = mapped_column(String(255))
    checks: Mapped[List["Check"]] = relationship(back_populates="conclusions")

    @staticmethod
    def get_id(conclusion):
        return (
            db.session.execute(
                select(Conclusion.id).filter(Conclusion.conclusion.ilike(conclusion))
            )
            .scalar_one_or_none()
        )


class Poligraf(Base):  # модель данных результаты ПФО
    """Create model for poligraf"""

    __tablename__ = "poligrafs"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    theme: Mapped[str] = mapped_column(String(255))
    results: Mapped[str] = mapped_column(Text)
    officer: Mapped[str] = mapped_column(String(255))
    deadline: Mapped[datetime] = mapped_column(Date, default=default_time)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="poligrafs")


class Investigation(Base):
    """Create model for ivestigation"""

    __tablename__ = "investigations"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    theme: Mapped[str] = mapped_column(String(255))
    info: Mapped[str] = mapped_column(Text)
    officer: Mapped[str] = mapped_column(String(255))
    deadline: Mapped[datetime] = mapped_column(Date, default=default_time)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="investigations")


class Inquiry(Base):
    """Create model for persons inquiries"""

    __tablename__ = "inquiries"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    info: Mapped[str] = mapped_column(Text, nullable=True)
    initiator: Mapped[str] = mapped_column(String(255), nullable=True)
    source: Mapped[str] = mapped_column(String(255), nullable=True)
    officer: Mapped[str] = mapped_column(String(255), nullable=True)
    deadline: Mapped[datetime] = mapped_column(
        Date, default=default_time, nullable=True
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="inquiries")


class Connect(Base):
    """Create model for persons connects"""

    __tablename__ = "connects"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    company: Mapped[str] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(255), nullable=True)
    fullname: Mapped[str] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(255), nullable=True)
    adding: Mapped[str] = mapped_column(String(255), nullable=True)
    mobile: Mapped[str] = mapped_column(String(255), nullable=True)
    mail: Mapped[str] = mapped_column(String(255), nullable=True)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    data: Mapped[datetime] = mapped_column(
        Date, default=default_time, onupdate=default_time, nullable=True
    )
    search_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("company", "fullname", "mobile", "phone")
    )
