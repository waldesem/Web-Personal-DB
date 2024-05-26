from datetime import date, datetime
from typing import Optional

from pydantic import ConfigDict
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

from ..config import settings


class TokenBlocklist(SQLModel, table=True):

    __tablename__ = "token_blocklist"

    id: int | None = Field(default=None, primary_key=True)
    jti: str
    created_at: datetime


class UserRole(SQLModel, table=True):
    __tablename__ = "user_roles"

    user_id: int = Field(default=None, primary_key=True, foreign_key="users.id")
    role_id: int = Field(default=None, primary_key=True, foreign_key="roles.id")


class Role(SQLModel, table=True):

    __tablename__ = "roles"

    id: int | None = Field(default=None, primary_key=True, unique=True)
    role: str = Field(unique=True, max_length=255)
    users: list["User"] = Relationship(back_populates="roles", link_model=UserRole)


class Region(SQLModel, table=True):

    __tablename__ = "regions"

    id: int | None = Field(default=None, primary_key=True, unique=True)
    region: str = Field(unique=True, max_length=255)
    users: list["User"] = Relationship(back_populates="regions")
    persons: list["Person"] = Relationship(back_populates="regions")

    @staticmethod
    def get_id(region):
        with Session(engine) as session:
            return session.exec(
                select(Region.id).filter(Region.region.like(region))
            ).one_or_none()


class User(SQLModel, table=True):

    __tablename__ = "users"

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int | None = Field(default=None, primary_key=True, unique=True)
    fullname: str | None = Field(max_length=255, index=True)
    username: str = Field(unique=True, max_length=255, index=True)
    email: str | None = Field(unique=True, max_length=255)
    created: datetime | None = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated: datetime | None = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    password: bytes | None = None
    pswd_created: datetime | None = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    change_pswd: bool | None = Field(default=True)
    last_login: datetime | None = None
    blocked: bool | None = Field(default=False)
    deleted: bool | None = Field(default=False)
    attempt: int | None = Field(default=0)
    region_id: int | None = Field(default=None, foreign_key="regions.id")
    regions: Region | None = Relationship(back_populates="users")
    messages: list["Message"] = Relationship(back_populates="users")
    persons: list["Person"] = Relationship(back_populates="users")
    checks: list["Check"] = Relationship(back_populates="users")
    poligrafs: list["Poligraf"] = Relationship(back_populates="users")
    investigations: list["Investigation"] = Relationship(back_populates="users")
    inquiries: list["Inquiry"] = Relationship(back_populates="users")
    roles: list["Role"] = Relationship(
        back_populates="users",
        link_model=UserRole,
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class Message(SQLModel, table=True):

    __tablename__ = "messages"

    id: int | None = Field(default=None, primary_key=True, unique=True)
    message: str
    created: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    user_id: int | None = Field(foreign_key="users.id")
    users: User | None = Relationship(back_populates="messages")


class Status(SQLModel, table=True):

    __tablename__ = "statuses"

    id: int | None = Field(default=None, primary_key=True, unique=True)
    status: str = Field(unique=True, max_length=255)
    persons: list["Person"] = Relationship(back_populates="statuses")

    @staticmethod
    def get_id(status):
        with Session(engine) as session:
            return session.exec(
                select(Status.id).filter(Status.status.like(status))
            ).one_or_none()


class Person(SQLModel, table=True):

    __tablename__ = "persons"

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int | None = Field(default=None, primary_key=True, unique=True)
    surname: str = Field(max_length=255, index=True)
    firstname: str = Field(max_length=255, index=True)
    patronymic: str | None = Field(max_length=255, index=True)
    birthday: date = Field(index=True)
    birthplace: str | None = None
    country: str | None = Field(max_length=255)
    ext_country: str | None = Field(max_length=255)
    snils: str | None = Field(max_length=11)
    inn: str | None = Field(max_length=12, index=True)
    marital: str | None = None
    addition: str | None = None
    path: str | None = None
    created: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    previous: list["Previous"] = Relationship(
        back_populates="persons",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
    educations: list["Education"] = Relationship(
        back_populates="persons",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
    staffs: list["Staff"] = Relationship(
        back_populates="persons",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
    documents: list["Document"] = Relationship(
        back_populates="persons",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
    addresses: list["Address"] = Relationship(
        back_populates="persons",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
    workplaces: list["Workplace"] = Relationship(
        back_populates="persons",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
    contacts: list["Contact"] = Relationship(
        back_populates="persons",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
    affilations: list["Affilation"] = Relationship(
        back_populates="persons",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
    relations: list["Relation"] = Relationship(
        back_populates="persons",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
    checks: list["Check"] = Relationship(
        back_populates="persons",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
    robots: list["Robot"] = Relationship(
        back_populates="persons",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
    inquiries: list["Inquiry"] = Relationship(
        back_populates="persons",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
    poligrafs: list["Poligraf"] = Relationship(
        back_populates="persons",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
    investigations: list["Investigation"] = Relationship(
        back_populates="persons",
        sa_relationship_kwargs={"cascade": "all,delete,delete-orphan"},
    )
    region_id: int | None = Field(default=None, foreign_key="regions.id")
    regions: Region = Relationship(back_populates="persons")
    status_id: int | None = Field(default=None, foreign_key="statuses.id")
    statuses: Status = Relationship(back_populates="persons")
    user_id: int | None = Field(default=None, foreign_key="users.id")
    users: User = Relationship(back_populates="persons")


class Previous(SQLModel, table=True):

    __tablename__ = "previous"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    surname: str | None = Field(max_length=255)
    firstname: str | None = Field(max_length=255)
    patronymic: str | None = Field(max_length=255)
    date_change: date | None = None
    reason: str | None = None
    created: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: Person | None = Relationship(back_populates="previous")


class Education(SQLModel, table=True):
    """Nested schema for AnketaSchemaApi"""

    __tablename__ = "educations"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    view: str = Field(max_length=255)
    name: str | None = Field(nullable=True)
    end: int | None = None
    specialty: str | None = None
    created: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: Person | None = Relationship(back_populates="educations")


class Staff(SQLModel, table=True):

    __tablename__ = "staffs"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    position: str = Field(nullable=True)
    department: str | None = Field(nullable=True)
    created: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: Person | None = Relationship(back_populates="staffs")


class Document(SQLModel, table=True):

    __tablename__ = "documents"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    view: str = Field(max_length=255)
    series: str | None = Field(max_length=255)
    number: str = Field(max_length=255)
    agency: str | None = Field(nullable=True)
    issue: date | None = None
    created: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: Person | None = Relationship(back_populates="documents")


class Address(SQLModel, table=True):

    __tablename__ = "addresses"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    view: str | None = Field(max_length=255)
    address: str = Field(nullable=True)
    created: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: Person | None = Relationship(back_populates="addresses")


class Contact(SQLModel, table=True):
    """Create model for contacts"""

    __tablename__ = "contacts"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    view: str = Field(max_length=255)
    contact: str = Field(max_length=255)
    created: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: Person | None = Relationship(back_populates="contacts")


class Workplace(SQLModel, table=True):

    __tablename__ = "workplaces"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    now_work: bool | None = Field(default=False)
    start_date: date | None = None
    end_date: date | None = None
    workplace: str = Field(max_length=255)
    address: str | None = Field(nullable=True)
    position: str | None = Field(nullable=True)
    reason: str | None = Field(nullable=True)
    created: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: Person | None = Relationship(back_populates="workplaces")


class Affilation(SQLModel, table=True):

    __tablename__ = "affilations"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    view: str | None = Field(max_length=255)
    name: str = Field(nullable=True)
    inn: str | None = Field(max_length=255)
    position: str | None = Field(nullable=True)
    created: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: Person | None = Relationship(back_populates="affilations")


class Relation(SQLModel, table=True):

    __tablename__ = "relations"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    relation: str = Field(max_length=255)
    relation_id: int | None
    created: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: Person | None = Relationship(back_populates="relations")


class Conclusion(SQLModel, table=True):

    __tablename__ = "conclusions"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    conclusion: str = Field(max_length=255)
    checks: list["Check"] = Relationship(back_populates="conclusions")

    @staticmethod
    def get_id(conclusion):
        with Session(engine) as session:
            return session.exec(
                select(Conclusion.id).filter(Conclusion.conclusion == conclusion)
            ).one_or_none()


class Motivation(SQLModel, table=True):

    __tablename__ = "motivations"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    motivation: str = Field(max_length=255)
    checks: list["Check"] = Relationship(back_populates="motivations")

    @staticmethod
    def get_id(motivation):
        with Session(engine) as session:
            return session.exec(
                select(Motivation.id).filter(Motivation.motivation == motivation)
            ).one_or_none()
        

class Check(SQLModel, table=True):

    __tablename__ = "checks"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    workplace: str | None = None
    document: str | None = None
    inn: str | None = None
    debt: str | None = None
    bankruptcy: str | None = None
    bki: str | None = None
    courts: str | None = None
    affilation: str | None = None
    terrorist: str | None = None
    mvd: str | None = None
    internet: str | None = None
    cronos: str | None = None
    cros: str | None = None
    addition: str | None = None
    pfo: bool | None = Field(default=False)
    comments: str | None = None
    created: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    conclusion_id: int | None = Field(default=None, foreign_key="conclusions.id")
    conclusions: Conclusion | None = Relationship(back_populates="checks")
    motivation_id: int | None = Field(default=None, foreign_key="motivations.id")
    motivations: Motivation | None = Relationship(back_populates="checks")
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: Person | None = Relationship(back_populates="checks")
    user_id: int | None = Field(default=None, foreign_key="users.id")
    users: User = Relationship(back_populates="checks")


class Robot(SQLModel, table=True):

    __tablename__ = "robots"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    employee: str | None = None
    inn: str | None = None
    debt: str | None = None
    bankruptcy: str | None = None
    bki: str | None = None
    courts: str | None = None
    terrorist: str | None = None
    mvd: str | None = None
    created: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: Person | None = Relationship(back_populates="robots")


class Poligraf(SQLModel, table=True):

    __tablename__ = "poligrafs"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    theme: str
    results: str
    created: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: Person | None = Relationship(back_populates="poligrafs")
    user_id: int | None = Field(foreign_key="users.id")
    users: User = Relationship(back_populates="poligrafs")


class Investigation(SQLModel, table=True):

    __tablename__ = "investigations"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    theme: str
    info: str
    created: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: Person | None = Relationship(back_populates="investigations")
    user_id: int | None = Field(foreign_key="users.id")
    users: User = Relationship(back_populates="investigations")


class Inquiry(SQLModel, table=True):

    __tablename__ = "inquiries"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    info: str
    initiator: str
    source: str
    created: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: Person | None = Relationship(back_populates="inquiries")
    user_id: int | None = Field(foreign_key="users.id")
    users: User = Relationship(back_populates="inquiries")


class Connect(SQLModel, table=True):

    __tablename__ = "connects"

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int | None = Field(default=None, primary_key=True, unique=True)
    name: str | None = Field(max_length=255)
    company: str = Field(index=True, max_length=255)
    city: str | None = Field(max_length=255)
    fullname: str = Field(max_length=255, index=True)
    phone: str | None = Field(max_length=255)
    adding: str | None = Field(max_length=255)
    mobile: str | None = Field(max_length=255)
    mail: str | None = Field(max_length=255)
    comment: str | None = None
    created: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )

engine = create_engine(settings.sqlalchemy_database_uri)
