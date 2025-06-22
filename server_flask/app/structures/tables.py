"""SQLAlchemy models."""

from __future__ import annotations

from datetime import date, datetime  # noqa: TC003

from flask import current_app
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
    exc,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    scoped_session,
    sessionmaker,
)
from werkzeug.security import generate_password_hash

from config import Config

from .classes import Regions, Roles

try:
    engine = create_engine(Config.DATABASE_URI)
    db_session = scoped_session(
        sessionmaker(bind=engine, autoflush=False, autocommit=False),
    )
except exc.OperationalError:
    current_app.logger.exception("Database connection error")


class Base(DeclarativeBase):
    """Base class for models."""

    def to_dict(self) -> dict:
        """Convert model to dict."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Users(Base):
    """User model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fullname: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    passhash: Mapped[str] = mapped_column(
        String(255),
        default=generate_password_hash(Config.DEFAULT_PASSWORD),
        nullable=True,
    )
    pswd_create: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        nullable=True,
    )
    change_pswd: Mapped[bool] = mapped_column(Boolean(), default=True)
    blocked: Mapped[bool] = mapped_column(Boolean(), default=False)
    deleted: Mapped[bool] = mapped_column(Boolean(), default=False)
    attempt: Mapped[int] = mapped_column(Integer(), default=0)
    role: Mapped[str] = mapped_column(String(), default=Roles.guest.value)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        nullable=True,
    )
    region: Mapped[str] = mapped_column(String(255), default=Regions.main.value)


class Phones(Base):
    """Phone model."""

    __tablename__ = "phones"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organization: Mapped[str] = mapped_column(String(255), nullable=False)
    fullname: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(255), nullable=True)
    mobile: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    comments: Mapped[str] = mapped_column(Text, nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )


class Persons(Base):
    """Person model."""

    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    surname: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    firstname: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    patronymic: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    birthplace: Mapped[str] = mapped_column(Text, nullable=True)
    citizenship: Mapped[str] = mapped_column(String(255), nullable=True)
    dual: Mapped[str] = mapped_column(String(255), nullable=True)
    snils: Mapped[str] = mapped_column(String(11), nullable=True)
    inn: Mapped[str] = mapped_column(String(12), nullable=True)
    marital: Mapped[str] = mapped_column(String(255), nullable=True)
    addition: Mapped[str] = mapped_column(Text, nullable=True)
    destination: Mapped[str] = mapped_column(Text, nullable=True)
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
    )
    educations: Mapped[list[Educations]] = relationship(
        back_populates="person",
        cascade="all, delete",
    )
    staffs: Mapped[list[Staffs]] = relationship(
        back_populates="person",
        cascade="all, delete",
    )
    addresses: Mapped[list[Addresses]] = relationship(
        back_populates="person",
        cascade="all, delete",
    )
    documents: Mapped[list[Documents]] = relationship(
        back_populates="person",
        cascade="all, delete",
    )
    contacts: Mapped[list[Contacts]] = relationship(
        back_populates="person",
        cascade="all, delete",
    )
    workplaces: Mapped[list[Workplaces]] = relationship(
        back_populates="person",
        cascade="all, delete",
    )
    affilations: Mapped[list[Affilations]] = relationship(
        back_populates="person",
        cascade="all, delete",
    )
    checks: Mapped[list[Checks]] = relationship(
        back_populates="person",
        cascade="all, delete",
    )
    poligrafs: Mapped[list[Poligrafs]] = relationship(
        back_populates="person",
        cascade="all, delete",
    )
    investigations: Mapped[list[Investigations]] = relationship(
        back_populates="person",
        cascade="all, delete",
    )
    inquiries: Mapped[list[Inquiries]] = relationship(
        back_populates="person",
        cascade="all, delete",
    )


class Previous(Base):
    """Previous model."""

    __tablename__ = "previous"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    surname: Mapped[str] = mapped_column(String(255), nullable=True)
    firstname: Mapped[str] = mapped_column(String(255), nullable=True)
    patronymic: Mapped[str] = mapped_column(String(255), nullable=True)
    changed: Mapped[str] = mapped_column(String(255), nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    person: Mapped[Persons] = relationship(back_populates="previous")


class Educations(Base):
    """Education model."""

    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    view: Mapped[str] = mapped_column(String(255), nullable=True)
    institution: Mapped[str] = mapped_column(Text, nullable=True)
    finished: Mapped[int] = mapped_column(Integer, nullable=True)
    specialty: Mapped[str] = mapped_column(Text, nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    person: Mapped[Persons] = relationship(back_populates="educations")


class Staffs(Base):
    """Staff model."""

    __tablename__ = "staffs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    position: Mapped[str] = mapped_column(Text, nullable=True)
    department: Mapped[str] = mapped_column(Text, nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    person: Mapped[Persons] = relationship(back_populates="staffs")


class Documents(Base):
    """Document model."""

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    view: Mapped[str] = mapped_column(String(255), nullable=True)
    series: Mapped[str] = mapped_column(String(255), nullable=True)
    digits: Mapped[str] = mapped_column(String(255), nullable=True)
    agency: Mapped[str] = mapped_column(Text, nullable=True)
    issue: Mapped[datetime] = mapped_column(Date, nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    person: Mapped[Persons] = relationship(back_populates="documents")


class Addresses(Base):
    """Address model."""

    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    view: Mapped[str] = mapped_column(String(255), nullable=True)
    addresses: Mapped[str] = mapped_column(Text, nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    person: Mapped[Persons] = relationship(back_populates="addresses")


class Contacts(Base):
    """Create model for contacts."""

    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    view: Mapped[str] = mapped_column(String(255), nullable=True)
    contact: Mapped[str] = mapped_column(String(255), nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    person: Mapped[Persons] = relationship(back_populates="contacts")


class Workplaces(Base):
    """Workplace model."""

    __tablename__ = "workplaces"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    now_work: Mapped[bool] = mapped_column(Boolean, nullable=True)
    starts: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    finished: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    workplace: Mapped[str] = mapped_column(String(255), nullable=True)
    addresses: Mapped[str] = mapped_column(Text, nullable=True)
    position: Mapped[str] = mapped_column(Text, nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    person: Mapped[Persons] = relationship(back_populates="workplaces")


class Affilations(Base):
    """Affiliation model."""

    __tablename__ = "affilations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    view: Mapped[str] = mapped_column(String(255), nullable=True)
    organization: Mapped[str] = mapped_column(Text, nullable=True)
    inn: Mapped[str] = mapped_column(String(255), nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    person: Mapped[Persons] = relationship(back_populates="affilations")


class Checks(Base):
    """Check model."""

    __tablename__ = "checks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
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
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    conclusion: Mapped[str] = mapped_column(Text, nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    person: Mapped[Persons] = relationship(back_populates="checks")


class Poligrafs(Base):
    """Poligraf model."""

    __tablename__ = "poligrafs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    theme: Mapped[str] = mapped_column(String(255), nullable=True)
    results: Mapped[str] = mapped_column(Text, nullable=True)
    conclusion: Mapped[str] = mapped_column(String(255), nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    person: Mapped[Persons] = relationship(back_populates="poligrafs")


class Investigations(Base):
    """Investigation model."""

    __tablename__ = "investigations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    theme: Mapped[str] = mapped_column(String(255), nullable=True)
    info: Mapped[str] = mapped_column(Text, nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    person: Mapped[Persons] = relationship(back_populates="investigations")


class Inquiries(Base):
    """Inquiry model."""

    __tablename__ = "inquiries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    info: Mapped[str] = mapped_column(Text, nullable=True)
    initiator: Mapped[str] = mapped_column(String(255), nullable=True)
    origins: Mapped[str] = mapped_column(String(255), nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    person: Mapped[Persons] = relationship(back_populates="inquiries")


Base.metadata.create_all(bind=engine)
