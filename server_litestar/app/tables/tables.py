"""SQLAlchemy models."""

from datetime import UTC, datetime

from advanced_alchemy.types import DateTimeUTC
from litestar.plugins.sqlalchemy import (
    BigIntAuditBase,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
    async_autocommit_before_send_handler,
)
from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.classes.classes import Roles
from app.utils.security import generate_password_hash
from constants import DATABASE_URI, DEFAULT_PASSWORD


class Users(BigIntAuditBase):
    """User model."""

    __tablename__ = "users"

    fullname: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    passhash: Mapped[str] = mapped_column(
        String(255),
        default=generate_password_hash(DEFAULT_PASSWORD),
    )
    pswd_create: Mapped[datetime] = mapped_column(
        DateTimeUTC(timezone=True),
        default=lambda: datetime.now(UTC),
    )
    change_pswd: Mapped[bool] = mapped_column(Boolean(), default=True)
    blocked: Mapped[bool] = mapped_column(Boolean(), default=False)
    deleted: Mapped[bool] = mapped_column(Boolean(), default=False)
    attempt: Mapped[int] = mapped_column(Integer(), default=0)
    role: Mapped[str] = mapped_column(String(), default=Roles.guest.value)
    persons: Mapped[list[Persons]] = relationship(back_populates="user")


class Persons(BigIntAuditBase):
    """Person model."""

    __tablename__ = "persons"

    surname: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    firstname: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    patronymic: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    birthday: Mapped[Date] = mapped_column(Date, nullable=False)
    birthplace: Mapped[str] = mapped_column(Text, nullable=True)
    citizenship: Mapped[str] = mapped_column(String(255), nullable=True)
    dual: Mapped[str] = mapped_column(String(255), nullable=True)
    snils: Mapped[str] = mapped_column(String(255), nullable=True)
    inn: Mapped[str] = mapped_column(String(255), nullable=True)
    marital: Mapped[str] = mapped_column(String(255), nullable=True)
    addition: Mapped[str] = mapped_column(Text, nullable=True)
    destination: Mapped[str] = mapped_column(Text, nullable=True)
    editable: Mapped[bool] = mapped_column(Boolean(), default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[Users] = relationship(back_populates="persons")
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


class Previous(BigIntAuditBase):
    """Previous model."""

    __tablename__ = "previous"

    surname: Mapped[str] = mapped_column(String(255))
    firstname: Mapped[str] = mapped_column(String(255))
    patronymic: Mapped[str] = mapped_column(String(255))
    changed: Mapped[str] = mapped_column(String(255))
    reason: Mapped[str] = mapped_column(Text)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="previous")


class Educations(BigIntAuditBase):
    """Education model."""

    __tablename__ = "educations"

    view: Mapped[str] = mapped_column(String(255))
    institution: Mapped[str] = mapped_column(Text)
    finished: Mapped[int] = mapped_column(Integer)
    specialty: Mapped[str] = mapped_column(Text)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="educations")


class Staffs(BigIntAuditBase):
    """Staff model."""

    __tablename__ = "staffs"

    position: Mapped[str] = mapped_column(Text)
    department: Mapped[str] = mapped_column(Text, nullable=True)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="staffs")


class Documents(BigIntAuditBase):
    """Document model."""

    __tablename__ = "documents"

    view: Mapped[str] = mapped_column(String(255), default="Паспорт")
    series: Mapped[str] = mapped_column(String(255), nullable=True)
    digits: Mapped[str] = mapped_column(String(255))
    agency: Mapped[str] = mapped_column(Text, nullable=True)
    issue: Mapped[Date] = mapped_column(Date)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="documents")


class Addresses(BigIntAuditBase):
    """Address model."""

    __tablename__ = "addresses"

    view: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(Text)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="addresses")


class Contacts(BigIntAuditBase):
    """Create model for contacts."""

    __tablename__ = "contacts"

    view: Mapped[str] = mapped_column(String(255))
    contact: Mapped[str] = mapped_column(String(255))
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="contacts")


class Workplaces(BigIntAuditBase):
    """Workplace model."""

    __tablename__ = "workplaces"

    now_work: Mapped[bool | None] = mapped_column(Boolean, default=False)
    starts: Mapped[Date | None] = mapped_column(Date)
    finished: Mapped[Date | None] = mapped_column(Date)
    workplace: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(Text, nullable=True)
    position: Mapped[str] = mapped_column(Text)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="workplaces")


class Affilations(BigIntAuditBase):
    """Affiliation model."""

    __tablename__ = "affilations"

    view: Mapped[str] = mapped_column(String(255))
    organization: Mapped[str] = mapped_column(Text)
    inn: Mapped[str] = mapped_column(String(255), nullable=True)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="affilations")


class Checks(BigIntAuditBase):
    """Check model."""

    __tablename__ = "checks"

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
    conclusion: Mapped[str] = mapped_column(Text, nullable=False)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="checks")


class Poligrafs(BigIntAuditBase):
    """Poligraf model."""

    __tablename__ = "poligrafs"

    theme: Mapped[str] = mapped_column(String(255))
    results: Mapped[str] = mapped_column(Text)
    conclusion: Mapped[str] = mapped_column(String(255))
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="poligrafs")


class Investigations(BigIntAuditBase):
    """Investigation model."""

    __tablename__ = "investigations"

    theme: Mapped[str] = mapped_column(String(255))
    info: Mapped[str] = mapped_column(Text)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="investigations")


class Inquiries(BigIntAuditBase):
    """Inquiry model."""

    __tablename__ = "inquiries"

    info: Mapped[str] = mapped_column(Text)
    initiator: Mapped[str] = mapped_column(String(255))
    origins: Mapped[str] = mapped_column(String(255), nullable=True)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="inquiries")


config = SQLAlchemyAsyncConfig(
    before_send_handler=async_autocommit_before_send_handler,
    connection_string=DATABASE_URI,
    create_all=True,
    metadata=BigIntAuditBase.metadata,
)
alchemy_plugin = SQLAlchemyInitPlugin(config=config)
