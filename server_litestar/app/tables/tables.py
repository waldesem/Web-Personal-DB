"""SQLAlchemy models."""

from litestar.plugins.sqlalchemy import (
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
    async_autocommit_before_send_handler,
    base,
)
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

from app.classes.classes import Roles
from app.utils.security import generate_password_hash
from constants import DATABASE_URI, DEFAULT_PASSWORD


class Users(base.UUIDAuditBase):
    """User model."""

    __tablename__ = "users"

    fullname: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    passhash: Mapped[str] = mapped_column(
        String(255),
        default=generate_password_hash(DEFAULT_PASSWORD),
    )
    pswd_create: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    change_pswd: Mapped[bool] = mapped_column(Boolean(), default=True)
    blocked: Mapped[bool] = mapped_column(Boolean(), default=False)
    deleted: Mapped[bool] = mapped_column(Boolean(), default=False)
    attempt: Mapped[int] = mapped_column(Integer(), default=0)
    role: Mapped[str] = mapped_column(String(), default=Roles.guest.value)


class Persons(base.UUIDAuditBase):
    """Person model."""

    __tablename__ = "persons"

    surname: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    firstname: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    patronymic: Mapped[str] = mapped_column(String(255), index=True)
    birthday: Mapped[Date] = mapped_column(Date, nullable=False)
    birthplace: Mapped[str] = mapped_column(Text)
    citizenship: Mapped[str] = mapped_column(String(255))
    dual: Mapped[str] = mapped_column(String(255))
    snils: Mapped[str] = mapped_column(String(255))
    inn: Mapped[str] = mapped_column(String(255))
    marital: Mapped[str] = mapped_column(String(255))
    addition: Mapped[str] = mapped_column(Text)
    destination: Mapped[str] = mapped_column(Text)
    editable: Mapped[bool] = mapped_column(Boolean(), default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
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


class Previous(base.UUIDAuditBase):
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


class Educations(base.UUIDAuditBase):
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


class Staffs(base.UUIDAuditBase):
    """Staff model."""

    __tablename__ = "staffs"

    position: Mapped[str] = mapped_column(Text)
    department: Mapped[str] = mapped_column(Text)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="staffs")


class Documents(base.UUIDAuditBase):
    """Document model."""

    __tablename__ = "documents"

    view: Mapped[str] = mapped_column(String(255), default="Паспорт")
    series: Mapped[str] = mapped_column(String(255))
    digits: Mapped[str] = mapped_column(String(255))
    agency: Mapped[str] = mapped_column(Text)
    issue: Mapped[DateTime] = mapped_column(Date)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="documents")


class Addresses(base.UUIDAuditBase):
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


class Contacts(base.UUIDAuditBase):
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


class Workplaces(base.UUIDAuditBase):
    """Workplace model."""

    __tablename__ = "workplaces"

    now_work: Mapped[bool] = mapped_column(Boolean, default=False)
    starts: Mapped[DateTime | None] = mapped_column(Date)
    finished: Mapped[DateTime | None] = mapped_column(Date)
    workplace: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(Text)
    position: Mapped[str] = mapped_column(Text)
    reason: Mapped[str] = mapped_column(Text)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="workplaces")


class Affilations(base.UUIDAuditBase):
    """Affiliation model."""

    __tablename__ = "affilations"

    view: Mapped[str] = mapped_column(String(255))
    organization: Mapped[str] = mapped_column(Text)
    inn: Mapped[str] = mapped_column(String(255))
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="affilations")


class Checks(base.UUIDAuditBase):
    """Check model."""

    __tablename__ = "checks"

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
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="checks")


class Poligrafs(base.UUIDAuditBase):
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


class Investigations(base.UUIDAuditBase):
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


class Inquiries(base.UUIDAuditBase):
    """Inquiry model."""

    __tablename__ = "inquiries"

    info: Mapped[str] = mapped_column(Text)
    initiator: Mapped[str] = mapped_column(String(255))
    origins: Mapped[str] = mapped_column(String(255))
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"),
        index=True,
        nullable=False,
    )
    person: Mapped[Persons] = relationship(back_populates="inquiries")


config = SQLAlchemyAsyncConfig(
    before_send_handler=async_autocommit_before_send_handler,
    connection_string=DATABASE_URI,
    # create_all=True,  # noqa: ERA001
    metadata=base.UUIDAuditBase.metadata,
)
alchemy_plugin = SQLAlchemyInitPlugin(config=config)
