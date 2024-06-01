from datetime import date, datetime
from typing import List, Optional

from config import Config
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    create_engine,
    func,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

class Base(DeclarativeBase):
    pass


class TokenBlocklist(Base):

    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    jti: Mapped[str] = mapped_column(String(36), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)


class Role(Base):

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    role: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    users: Mapped[List["User"]] = relationship(
        back_populates="roles", secondary=user_roles, lazy="dynamic"
    )


class Region(Base):

    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    region: Mapped[str] = mapped_column(String(255), nullable=False)
    persons: Mapped[List["Person"]] = relationship(back_populates="regions")
    users: Mapped[List["User"]] = relationship(back_populates="regions")

    @staticmethod
    def get_id(region):
        with Session(engine) as session:
            return session.execute(
                select(Region.id).filter(Region.region.like(region))
            ).scalar_one_or_none()


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    fullname: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True, unique=True)
    pswd_create: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, default=func.now()
    )
    pswd_change: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    blocked: Mapped[bool] = mapped_column(Boolean(), default=False)
    deleted: Mapped[bool] = mapped_column(Boolean(), default=False)
    attempt: Mapped[int] = mapped_column(Integer(), default=0, nullable=True)
    created: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[datetime] = mapped_column(DateTime, nullable=True, onupdate=func.now())
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    regions: Mapped["Region"] = relationship(back_populates="users")
    messages: Mapped[List["Message"]] = relationship(back_populates="users")
    persons: Mapped[List["Person"]] = relationship(back_populates="users")
    checks: Mapped[List["Check"]] = relationship(back_populates="users")
    poligrafs: Mapped[List["Poligraf"]] = relationship(back_populates="users")
    investigations: Mapped[List["Investigation"]] = relationship(back_populates="users")
    inquiries: Mapped[List["Inquiry"]] = relationship(back_populates="users")
    roles: Mapped[List["Role"]] = relationship(
        back_populates="users", secondary=user_roles, lazy="subquery"
    )


    @staticmethod
    def get_user(user_name):
        with Session(engine) as session:
            return session.execute(
                select(User).filter_by(username=user_name)
            ).scalar_one_or_none()


class Message(Base):

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    message: Mapped[str] = mapped_column(Text, nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    users: Mapped["User"] = relationship(back_populates="messages")


class Status(Base):

    __tablename__ = "statuses"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    status: Mapped[str] = mapped_column(String(255), nullable=True)
    persons: Mapped[List["Person"]] = relationship(back_populates="statuses")

    @staticmethod
    def get_id(status):
        with Session(engine) as session:
            return session.execute(
                select(Status.id).filter(Status.status.like(status))
            ).scalar_one_or_none()


class Person(Base):

    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    surname: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    firstname: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    patronymic: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    birthplace: Mapped[str] = mapped_column(Text, nullable=True)
    country: Mapped[str] = mapped_column(String(255), nullable=True)
    ext_country: Mapped[str] = mapped_column(String(255), nullable=True)
    snils: Mapped[str] = mapped_column(String(11), nullable=True)
    inn: Mapped[str] = mapped_column(String(12), nullable=True, index=True)
    marital: Mapped[str] = mapped_column(String(255), nullable=True)
    addition: Mapped[str] = mapped_column(Text, nullable=True)
    path: Mapped[str] = mapped_column(Text, nullable=True)
    created: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=True
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime, onupdate=func.now(), nullable=True
    )
    previous: Mapped[List["Previous"]] = relationship(
        back_populates="persons", cascade="all, delete, delete-orphan"
    )
    educations: Mapped[List["Education"]] = relationship(
        back_populates="persons", cascade="all, delete, delete-orphan"
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
    region_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("regions.id"), nullable=True
    )
    status_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("statuses.id"), nullable=True
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    statuses: Mapped["Status"] = relationship(back_populates="persons")
    regions: Mapped["Region"] = relationship(back_populates="persons")
    users: Mapped["User"] = relationship(back_populates="persons")


class Previous(Base):

    __tablename__ = "previous"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    surname: Mapped[str] = mapped_column(String(255), nullable=True)
    firstname: Mapped[str] = mapped_column(String(255), nullable=True)
    patronymic: Mapped[str] = mapped_column(String(255), nullable=True)
    date_change: Mapped[date] = mapped_column(Date, nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="previous")


class Education(Base):
    """Nested schema for AnketaSchemaApi"""

    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    view: Mapped[str] = mapped_column(String(255), nullable=True)
    name: Mapped[str] = mapped_column(Text, nullable=True)
    end: Mapped[int] = mapped_column(Integer, nullable=True)
    specialty: Mapped[str] = mapped_column(Text, nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="educations")


class Staff(Base):

    __tablename__ = "staffs"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    position: Mapped[str] = mapped_column(Text, nullable=True)
    department: Mapped[str] = mapped_column(Text, nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="staffs")


class Document(Base):

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


class Address(Base):

    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    view: Mapped[str] = mapped_column(String(255), nullable=True)
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

    __tablename__ = "workplaces"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    now_work: Mapped[bool] = mapped_column(Boolean, nullable=True)
    start_date: Mapped[datetime] = mapped_column(Date, nullable=True)
    end_date: Mapped[datetime] = mapped_column(Date, nullable=True)
    workplace: Mapped[str] = mapped_column(String(255), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    position: Mapped[str] = mapped_column(Text, nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="workplaces")


class Affilation(Base):

    __tablename__ = "affilations"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    view: Mapped[str] = mapped_column(String(255), nullable=True)
    name: Mapped[str] = mapped_column(Text, nullable=True)
    inn: Mapped[str] = mapped_column(String(255), nullable=True)
    position: Mapped[str] = mapped_column(Text, nullable=True)
    deadline: Mapped[datetime] = mapped_column(Date, default=func.now(), nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="affilations")


class Relation(Base):

    __tablename__ = "relations"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    relation: Mapped[str] = mapped_column(String(255), nullable=True)
    relation_id: Mapped[int] = mapped_column(Integer, nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="relations")


class Check(Base):

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
    deadline: Mapped[datetime] = mapped_column(
        Date, default=func.now(), onupdate=func.now(), nullable=True
    )
    conclusion_id: Mapped[int] = mapped_column(
        ForeignKey("conclusions.id"), nullable=True
    )
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    conclusions: Mapped["Conclusion"] = relationship(back_populates="checks")
    persons: Mapped[List["Person"]] = relationship(back_populates="checks")
    users: Mapped["User"] = relationship(back_populates="checks")


class Robot(Base):

    __tablename__ = "robots"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    employee: Mapped[str] = mapped_column(Text, nullable=True)
    inn: Mapped[str] = mapped_column(Text, nullable=True)
    debt: Mapped[str] = mapped_column(Text, nullable=True)
    bankruptcy: Mapped[str] = mapped_column(Text, nullable=True)
    bki: Mapped[str] = mapped_column(Text, nullable=True)
    courts: Mapped[str] = mapped_column(Text, nullable=True)
    terrorist: Mapped[str] = mapped_column(Text, nullable=True)
    mvd: Mapped[str] = mapped_column(Text, nullable=True)
    deadline: Mapped[datetime] = mapped_column(Date, default=func.now(), nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="robots")


class Conclusion(Base):

    __tablename__ = "conclusions"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    conclusion: Mapped[str] = mapped_column(String(255), nullable=True)
    checks: Mapped[List["Check"]] = relationship(back_populates="conclusions")

    @staticmethod
    def get_id(conclusion):
        with Session(engine) as session:
            return session.execute(
                select(Conclusion.id).filter(Conclusion.conclusion.ilike(conclusion))
            ).scalar_one_or_none()


class Poligraf(Base):

    __tablename__ = "poligrafs"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    theme: Mapped[str] = mapped_column(String(255), nullable=True)
    results: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    deadline: Mapped[datetime] = mapped_column(Date, default=func.now(), nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="poligrafs")
    users: Mapped["User"] = relationship(back_populates="poligrafs")


class Investigation(Base):

    __tablename__ = "investigations"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    theme: Mapped[str] = mapped_column(String(255), nullable=True)
    info: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    deadline: Mapped[datetime] = mapped_column(Date, default=func.now(), nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="investigations")
    users: Mapped["User"] = relationship(back_populates="investigations")


class Inquiry(Base):

    __tablename__ = "inquiries"

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    info: Mapped[str] = mapped_column(Text, nullable=True)
    initiator: Mapped[str] = mapped_column(String(255), nullable=True)
    source: Mapped[str] = mapped_column(String(255), nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    deadline: Mapped[datetime] = mapped_column(Date, default=func.now(), nullable=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    persons: Mapped[List["Person"]] = relationship(back_populates="inquiries")
    users: Mapped["User"] = relationship(back_populates="inquiries")


class Connect(Base):

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
        DateTime, default=func.now(), onupdate=func.now(), nullable=True
    )
