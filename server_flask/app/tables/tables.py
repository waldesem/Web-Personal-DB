"""SQLAlchemy models."""

from __future__ import annotations

from datetime import date, datetime  # noqa: TC003

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash

from app import db
from app.classes.classes import Regions, Roles
from config import Config


class Users(db.Model):
    """User model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    fullname: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    passhash: Mapped[str] = mapped_column(
        String(255),
        default=generate_password_hash(Config.DEFAULT_PASSWORD),
    )
    pswd_create: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    change_pswd: Mapped[bool] = mapped_column(Boolean(), default=True)
    blocked: Mapped[bool] = mapped_column(Boolean(), default=False)
    deleted: Mapped[bool] = mapped_column(Boolean(), default=False)
    attempt: Mapped[int] = mapped_column(Integer(), default=0)
    role: Mapped[str] = mapped_column(String(), default=Roles.guest.value)
    region: Mapped[str] = mapped_column(String(255), default=Regions.main.value)


class Persons(db.Model):
    """Person model."""

    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    surname: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    firstname: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    patronymic: Mapped[str] = mapped_column(String(255), index=True)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    birthplace: Mapped[str] = mapped_column(Text)
    citizenship: Mapped[str] = mapped_column(String(255))
    dual: Mapped[str] = mapped_column(String(255))
    snils: Mapped[str] = mapped_column(String(11))
    inn: Mapped[str] = mapped_column(String(12))
    marital: Mapped[str] = mapped_column(String(255))
    addition: Mapped[str] = mapped_column(Text)
    destination: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    region: Mapped[str] = mapped_column(String(255), default=Regions.main.value)
    editable: Mapped[bool] = mapped_column(Boolean(), default=False)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    previous: Mapped[list[Previous]] = relationship(
        back_populates="person",
        cascade="all, delete",
        lazy="dynamic",
    )
    educations: Mapped[list[Educations]] = relationship(
        back_populates="person",
        cascade="all, delete",
        lazy="dynamic",
    )
    staffs: Mapped[list[Staffs]] = relationship(
        back_populates="person",
        cascade="all, delete",
        lazy="dynamic",
    )
    addresses: Mapped[list[Addresses]] = relationship(
        back_populates="person",
        cascade="all, delete",
        lazy="dynamic",
    )
    documents: Mapped[list[Documents]] = relationship(
        back_populates="person",
        cascade="all, delete",
        lazy="dynamic",
    )
    contacts: Mapped[list[Contacts]] = relationship(
        back_populates="person",
        cascade="all, delete",
        lazy="dynamic",
    )
    workplaces: Mapped[list[Workplaces]] = relationship(
        back_populates="person",
        cascade="all, delete",
        lazy="dynamic",
    )
    affilations: Mapped[list[Affilations]] = relationship(
        back_populates="person",
        cascade="all, delete",
        lazy="dynamic",
    )
    checks: Mapped[list[Checks]] = relationship(
        back_populates="person",
        cascade="all, delete",
        lazy="dynamic",
    )
    poligrafs: Mapped[list[Poligrafs]] = relationship(
        back_populates="person",
        cascade="all, delete",
        lazy="dynamic",
    )
    investigations: Mapped[list[Investigations]] = relationship(
        back_populates="person",
        cascade="all, delete",
        lazy="dynamic",
    )
    inquiries: Mapped[list[Inquiries]] = relationship(
        back_populates="person",
        cascade="all, delete",
        lazy="dynamic",
    )


class Previous(db.Model):
    """Previous model."""

    __tablename__ = "previous"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    surname: Mapped[str] = mapped_column(String(255))
    firstname: Mapped[str] = mapped_column(String(255))
    patronymic: Mapped[str] = mapped_column(String(255))
    changed: Mapped[str] = mapped_column(String(255))
    reason: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), index=True)
    person: Mapped[Persons] = relationship(back_populates="previous")


class Educations(db.Model):
    """Education model."""

    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    view: Mapped[str] = mapped_column(String(255))
    institution: Mapped[str] = mapped_column(Text)
    finished: Mapped[int] = mapped_column(Integer)
    specialty: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), index=True)
    person: Mapped[Persons] = relationship(back_populates="educations")


class Staffs(db.Model):
    """Staff model."""

    __tablename__ = "staffs"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    position: Mapped[str] = mapped_column(Text)
    department: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), index=True)
    person: Mapped[Persons] = relationship(back_populates="staffs")


class Documents(db.Model):
    """Document model."""

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    view: Mapped[str] = mapped_column(String(255), default="Паспорт")
    series: Mapped[str] = mapped_column(String(255))
    digits: Mapped[str] = mapped_column(String(255))
    agency: Mapped[str] = mapped_column(Text)
    issue: Mapped[datetime] = mapped_column(Date)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), index=True)
    person: Mapped[Persons] = relationship(back_populates="documents")


class Addresses(db.Model):
    """Address model."""

    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    view: Mapped[str] = mapped_column(String(255))
    addresses: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), index=True)
    person: Mapped[Persons] = relationship(back_populates="addresses")


class Contacts(db.Model):
    """Create model for contacts."""

    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    view: Mapped[str] = mapped_column(String(255))
    contact: Mapped[str] = mapped_column(String(255))
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), index=True)
    person: Mapped[Persons] = relationship(back_populates="contacts")


class Workplaces(db.Model):
    """Workplace model."""

    __tablename__ = "workplaces"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    now_work: Mapped[bool] = mapped_column(Boolean, default=False)
    starts: Mapped[datetime | None] = mapped_column(Date)
    finished: Mapped[datetime | None] = mapped_column(Date)
    workplace: Mapped[str] = mapped_column(String(255))
    addresses: Mapped[str] = mapped_column(Text)
    position: Mapped[str] = mapped_column(Text)
    reason: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), index=True)
    person: Mapped[Persons] = relationship(back_populates="workplaces")


class Affilations(db.Model):
    """Affiliation model."""

    __tablename__ = "affilations"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    view: Mapped[str] = mapped_column(String(255))
    organization: Mapped[str] = mapped_column(Text)
    inn: Mapped[str] = mapped_column(String(255))
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), index=True)
    person: Mapped[Persons] = relationship(back_populates="affilations")


class Checks(db.Model):
    """Check model."""

    __tablename__ = "checks"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    workplace: Mapped[str] = mapped_column(Text)
    document: Mapped[str] = mapped_column(Text)
    inn: Mapped[str] = mapped_column(Text)
    debt: Mapped[str] = mapped_column(Text)
    bankruptcy: Mapped[str] = mapped_column(Text)
    bki: Mapped[str] = mapped_column(Text)
    courts: Mapped[str] = mapped_column(Text)
    affilation: Mapped[str] = mapped_column(Text)
    terrorist: Mapped[str] = mapped_column(Text)
    mvd: Mapped[str] = mapped_column(Text)
    internet: Mapped[str] = mapped_column(Text)
    cronos: Mapped[str] = mapped_column(Text)
    cros: Mapped[str] = mapped_column(Text)
    addition: Mapped[str] = mapped_column(Text)
    comment: Mapped[str] = mapped_column(Text)
    conclusion: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), index=True)
    person: Mapped[Persons] = relationship(back_populates="checks")


class Poligrafs(db.Model):
    """Poligraf model."""

    __tablename__ = "poligrafs"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    theme: Mapped[str] = mapped_column(String(255))
    results: Mapped[str] = mapped_column(Text)
    conclusion: Mapped[str] = mapped_column(String(255))
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), index=True)
    person: Mapped[Persons] = relationship(back_populates="poligrafs")


class Investigations(db.Model):
    """Investigation model."""

    __tablename__ = "investigations"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    theme: Mapped[str] = mapped_column(String(255))
    info: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), index=True)
    person: Mapped[Persons] = relationship(back_populates="investigations")


class Inquiries(db.Model):
    """Inquiry model."""

    __tablename__ = "inquiries"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    info: Mapped[str] = mapped_column(Text)
    initiator: Mapped[str] = mapped_column(String(255))
    origins: Mapped[str] = mapped_column(String(255))
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), index=True)
    person: Mapped[Persons] = relationship(back_populates="inquiries")
