from datetime import date, datetime
from typing import Optional

import bcrypt
from pydantic import ConfigDict
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship, create_engine, select, SQLModel, Session
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType

from ..config import Config
from .classes import Roles, Regions, Statuses, Conclusions


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


class User(SQLModel, table=True):
    
    __tablename__ = "users"
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    id: int | None = Field(default=None, primary_key=True, unique=True)
    fullname: str = Field(max_length=255)
    username: str = Field(unique=True, max_length=255)
    password: bytes | None = None
    email: str | None = Field(unique=True, max_length=255)
    region_id: int | None = Field(default=None, foreign_key="regions.id")
    pswd_create: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    change_pswd: Optional[bool] = Field(default=True)
    last_login: datetime | None = None
    blocked: bool = Field(default=False)
    deleted: bool = Field(default=False)
    attempt: int = Field(default=0)
    regions: "Region" = Relationship(back_populates="users")
    messages: list["Message"] = Relationship(back_populates="users")
    persons: list["Person"] = Relationship(back_populates="users")
    checks: list["Check"] = Relationship(back_populates="users")
    poligrafs: list["Poligraf"] = Relationship(back_populates="users")
    investigations: list["Investigation"] = Relationship(back_populates="users")
    inquiries: list["Inquiry"] = Relationship(back_populates="users")
    roles: list["Role"] = Relationship(back_populates="users", link_model=UserRole)
    search_vector: TSVectorType = Field(sa_column=Column(TSVectorType("fullname", "username")))

    @staticmethod
    def get_user(user_name):
        with Session(engine) as session:
            return session.exec(
                select(User).filter_by(username=user_name)
            ).one_or_none()


class Message(SQLModel, table=True):

    __tablename__ = "messages"

    id: int | None = Field(default=None, primary_key=True, unique=True)
    message: str
    created: Optional[datetime] = Field(
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


class Person(SQLModel, table=True):

    __tablename__ = "persons"

    id: int | None = Field(default=None, primary_key=True, unique=True)
    region_id: int | None = Field(default=None, foreign_key="regions.id")
    status_id: int | None = Field(default=None, foreign_key="statuses.id")
    user_id: int | None = Field(default=None, foreign_key="users.id")
    surname: str = Field(max_length=255, index=True)
    firstname: str = Field(max_length=255, index=True)
    patronymic: str = Field(max_length=255, index=True)
    birthday: date = Field(index=True)
    birthplace: str | None = None
    country: str | None = Field(max_length=255)
    ext_country: str | None = Field(max_length=255)
    snils: str | None = Field(max_length=11, index=True)
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
    statuses: Status = Relationship(back_populates="persons")
    regions: "Region" = Relationship(back_populates="persons")
    users: "User" = Relationship(back_populates="persons")
    

class Previous(SQLModel, table=True):

    __tablename__ = "previous"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    surname: str = Field(max_length=255)
    firstname: str = Field(max_length=255)
    patronymic: str = Field(max_length=255)
    date_change: date | None = None
    reason: str | None = None
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: list["Person"] = Relationship(back_populates="previous")


class Education(SQLModel, table=True):
    """Nested schema for AnketaSchemaApi"""

    __tablename__ = "educations"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    view: str = Field(max_length=255)
    name: str = Field(nullable=True)
    end: int | None = None
    specialty: str | None = None
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: list["Person"] = Relationship(back_populates="educations")


class Staff(SQLModel, table=True):

    __tablename__ = "staffs"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    position: str = Field(nullable=True)
    department: str = Field(nullable=True)
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: list["Person"] = Relationship(back_populates="staffs")


class Document(SQLModel, table=True):

    __tablename__ = "documents"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    view: str = Field(max_length=255)
    series: str = Field(max_length=255)
    number: str = Field(max_length=255)
    agency: str = Field(nullable=True)
    issue: date | None = None
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: list["Person"] = Relationship(back_populates="documents")


class Address(SQLModel, table=True):

    __tablename__ = "addresses"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    view: str = Field(max_length=255)
    address: str = Field(nullable=True)
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: list["Person"] = Relationship(back_populates="addresses")


class Contact(SQLModel, table=True):
    """Create model for contacts"""

    __tablename__ = "contacts"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    view: str = Field(max_length=255)
    contact: str = Field(max_length=255)
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: list["Person"] = Relationship(back_populates="contacts")


class Workplace(SQLModel, table=True):

    __tablename__ = "workplaces"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    now_work: bool | None = None
    start_date: date | None = None
    end_date: date | None = None
    workplace: str = Field(max_length=255)
    address: str = Field(nullable=True)
    position: str = Field(nullable=True)
    reason: str = Field(nullable=True)
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: list["Person"] = Relationship(back_populates="workplaces")


class Affilation(SQLModel, table=True):

    __tablename__ = "affilations"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    view: str = Field(max_length=255)
    name: str = Field(nullable=True)
    inn: str = Field(max_length=255)
    position: str = Field(nullable=True)
    deadline: datetime | None = None
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: list["Person"] = Relationship(back_populates="affilations")


class Relation(SQLModel, table=True):

    __tablename__ = "relations"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    relation: str = Field(max_length=255)
    relation_id: int | None = None
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: list["Person"] = Relationship(back_populates="relations")


class Check(SQLModel, table=True):

    __tablename__ = "checks"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    workplace: str = Field(nullable=True)
    document: str = Field(nullable=True)
    inn: str = Field(nullable=True)
    debt: str = Field(nullable=True)
    bankruptcy: str = Field(nullable=True)
    bki: str = Field(nullable=True)
    courts: str = Field(nullable=True)
    affilation: str = Field(nullable=True)
    terrorist: str = Field(nullable=True)
    mvd: str = Field(nullable=True)
    internet: str = Field(nullable=True)
    cronos: str = Field(nullable=True)
    cros: str = Field(nullable=True)
    addition: str = Field(nullable=True)
    pfo: bool | None = None
    comments: str = Field(nullable=True)
    deadline: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    conclusion_id: int | None = Field(default=None, foreign_key="conclusions.id")
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    user_id: int | None = Field(default=None, foreign_key="users.id")
    persons: list["Person"] = Relationship(back_populates="checks")
    users: User = Relationship(back_populates="checks")
    conclusions: list["Conclusion"] = Relationship(back_populates="checks")


class Robot(SQLModel, table=True):

    __tablename__ = "robots"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    employee: str = Field(nullable=True)
    inn: str = Field(nullable=True)
    debt: str = Field(nullable=True)
    bankruptcy: str = Field(nullable=True)
    bki: str = Field(nullable=True)
    courts: str = Field(nullable=True)
    terrorist: str = Field(nullable=True)
    mvd: str = Field(nullable=True)
    deadline: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: list["Person"] = Relationship(back_populates="robots")


class Conclusion(SQLModel, table=True):

    __tablename__ = "conclusions"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    conclusion: str = Field(max_length=255)
    checks: list["Check"] = Relationship(back_populates="conclusions")

    @staticmethod
    def get_id(conclusion):
        with Session(engine) as session:
            return session.execute(
                select(Conclusion.id).filter(Conclusion.conclusion == conclusion)
            ).scalar_one_or_none()


class Poligraf(SQLModel, table=True):

    __tablename__ = "poligrafs"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    theme: str = Field(max_length=255)
    results: str = Field(nullable=True)
    user_id: int | None = Field(foreign_key="users.id")
    deadline: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: list["Person"] = Relationship(back_populates="poligrafs")
    users: User = Relationship(back_populates="poligrafs")


class Investigation(SQLModel, table=True):

    __tablename__ = "investigations"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    theme: str = Field(max_length=255)
    info: str = Field(nullable=True)
    user_id: int | None = Field(foreign_key="users.id")
    deadline: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: list["Person"] = Relationship(back_populates="investigations")
    users: User = Relationship(back_populates="investigations")


class Inquiry(SQLModel, table=True):

    __tablename__ = "inquiries"

    id: int | None = Field(default=None, primary_key=True, nullable=False, unique=True)
    info: str = Field(nullable=True)
    initiator: str = Field(max_length=255)
    source: str = Field(max_length=255)
    user_id: int | None = Field(foreign_key="users.id")
    deadline: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    person_id: int | None = Field(default=None, foreign_key="persons.id")
    persons: list["Person"] = Relationship(back_populates="inquiries")
    users: User = Relationship(back_populates="inquiries")


class Connect(SQLModel, table=True):

    __tablename__ = "connects"

    id: int | None = Field(default=None, primary_key=True, unique=True)
    name: str = Field(index=True, max_length=255)
    company: str | None = Field(index=True, max_length=255)
    city: str | None = Field(max_length=255)
    fullname: str = Field(max_length=255)
    phone: str | None = Field(index=True, max_length=255)
    adding: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True)), default=func.now()
    )
    mobile: str | None = Field(max_length=255)
    mail: str | None = Field(max_length=255)
    comment: str | None = None
    data: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

make_searchable(SQLModel.metadata)

SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    for item in [
        [Region(region=reg.value) for reg in Regions],
        [Status(status=item.value) for item in Statuses],
        [Conclusion(conclusion=item.value) for item in Conclusions],
        [Role(role=actor.value) for actor in Roles],
    ]:
        session.add_all(item)
    session.commit()

    superadmin = User(
        fullname="Администратор",
        username="superadmin",
        email="admin@example.com",
        password=bcrypt.hashpw(
            Config.DEFAULT_PASSWORD.encode("utf-8"),
            salt=bcrypt.gensalt(),
        ),
    )
    superadmin.roles.append(
        session.exec(
            select(Role).filter_by(role=Roles.admin.value)
        ).one_or_none()
    )
    session.add(superadmin)
    session.commit()

    print("Database initialized and filled")
