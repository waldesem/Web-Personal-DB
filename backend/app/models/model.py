from datetime import date, datetime
from typing import List, Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
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
    select,
)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

make_searchable(db.metadata)


def default_time():
    return datetime.now()


user_roles = db.Table(
    "user_roles",
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)


class Role(db.Model):

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    role: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    users: Mapped[List["User"]] = relationship(
        back_populates="roles", secondary=user_roles, lazy="dynamic"
    )


class User(db.Model):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    fullname: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(LargeBinary, nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    pswd_create: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, default=default_time
    )
    pswd_change: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    blocked: Mapped[bool] = mapped_column(Boolean(), default=False)
    deleted: Mapped[bool] = mapped_column(Boolean(), default=False)
    attempt: Mapped[int] = mapped_column(Integer(), default=0, nullable=True)
    messages: Mapped[List["Message"]] = relationship(back_populates="users")
    persons: Mapped[List["Person"]] = relationship(back_populates="users")
    roles: Mapped[List["Role"]] = relationship(
        back_populates="users", secondary=user_roles, lazy="dynamic"
    )
    search_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("fullname", "username", "email")
    )

    @staticmethod
    def get_user(user_name):
        return db.session.execute(
            select(User).filter_by(username=user_name)
        ).scalar_one_or_none()


class Message(db.Model):

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    message: Mapped[str] = mapped_column(Text, nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime, default=default_time, nullable=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    users: Mapped["User"] = relationship(back_populates="messages")


class Status(db.Model):

    __tablename__ = "statuses"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    status: Mapped[str] = mapped_column(String(255), nullable=True)
    persons: Mapped[List["Person"]] = relationship(back_populates="statuses")

    @staticmethod
    def get_id(status):
        return db.session.execute(
            select(Status.id).filter(Status.status.like(status))
        ).scalar_one_or_none()


class Region(db.Model):

    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    region: Mapped[str] = mapped_column(String(255), nullable=False)
    persons: Mapped[List["Person"]] = relationship(back_populates="regions")

    @staticmethod
    def get_id(region):
        return db.session.execute(
            select(Region.id).filter(Region.region.like(region))
        ).scalar_one_or_none()


class Person(db.Model):

    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    region_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("regions.id"), nullable=True
    )
    status_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("statuses.id"), nullable=True
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    surname: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    firstname: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    patronymic: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    previous: Mapped[str] = mapped_column(Text, nullable=True, index=True)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    birthplace: Mapped[str] = mapped_column(Text, nullable=True)
    country: Mapped[str] = mapped_column(String(255), nullable=True)
    ext_country: Mapped[str] = mapped_column(String(255), nullable=True)
    snils: Mapped[str] = mapped_column(String(11), nullable=True)
    inn: Mapped[str] = mapped_column(String(12), nullable=True, index=True)
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
    statuses: Mapped["Status"] = relationship(back_populates="persons")
    regions: Mapped["Region"] = relationship(back_populates="persons")
    users: Mapped["User"] = relationship(back_populates="persons")
    search_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("previous", "surname", "firstname", "patronymic")
    )


class Staff(db.Model):

    __tablename__ = "staffs"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    position: Mapped[str] = mapped_column(Text, nullable=True)
    department: Mapped[str] = mapped_column(Text, nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="staffs")


class Document(db.Model):

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


class Address(db.Model):

    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    view: Mapped[str] = mapped_column(String(255), nullable=True)
    region: Mapped[str] = mapped_column(String(255), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="addresses")


class Contact(db.Model):
    """Create model for contacts"""

    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    view: Mapped[str] = mapped_column(String(255), nullable=True)
    contact: Mapped[str] = mapped_column(String(255), nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="contacts")


class Workplace(db.Model):

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


class Affilation(db.Model):

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


class Relation(db.Model):

    __tablename__ = "relations"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    relation: Mapped[str] = mapped_column(String(255), nullable=True)
    relation_id: Mapped[int] = mapped_column(Integer, nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="relations")


class Check(db.Model):

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
    conclusion_id: Mapped[int] = mapped_column(
        ForeignKey("conclusions.id"), nullable=True
    )
    officer: Mapped[str] = mapped_column(String(255), nullable=True)
    deadline: Mapped[datetime] = mapped_column(
        Date, default=default_time, onupdate=default_time, nullable=True
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="checks")
    conclusions: Mapped["Conclusion"] = relationship(back_populates="checks")


class Robot(db.Model):

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


class Conclusion(db.Model):

    __tablename__ = "conclusions"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    conclusion: Mapped[str] = mapped_column(String(255), nullable=True)
    checks: Mapped[List["Check"]] = relationship(back_populates="conclusions")

    @staticmethod
    def get_id(conclusion):
        return db.session.execute(
            select(Conclusion.id).filter(Conclusion.conclusion.ilike(conclusion))
        ).scalar_one_or_none()


class Poligraf(db.Model):

    __tablename__ = "poligrafs"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    theme: Mapped[str] = mapped_column(String(255), nullable=True)
    results: Mapped[str] = mapped_column(Text, nullable=True)
    officer: Mapped[str] = mapped_column(String(255), nullable=True)
    deadline: Mapped[datetime] = mapped_column(
        Date, default=default_time, nullable=True
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="poligrafs")


class Investigation(db.Model):

    __tablename__ = "investigations"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    theme: Mapped[str] = mapped_column(String(255), nullable=True)
    info: Mapped[str] = mapped_column(Text, nullable=True)
    officer: Mapped[str] = mapped_column(String(255), nullable=True)
    deadline: Mapped[datetime] = mapped_column(
        Date, default=default_time, nullable=True
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="investigations")


class Inquiry(db.Model):

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


class Connect(db.Model):

    __tablename__ = "connects"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    company: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    city: Mapped[str] = mapped_column(String(255), nullable=True)
    fullname: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    adding: Mapped[str] = mapped_column(String(255), nullable=True)
    mobile: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    mail: Mapped[str] = mapped_column(String(255), nullable=True)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    data: Mapped[datetime] = mapped_column(
        Date, default=default_time, onupdate=default_time, nullable=True
    )
    search_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("company", "fullname")
    )
