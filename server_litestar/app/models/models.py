"""PyDantic models."""

from __future__ import annotations

from datetime import date, datetime  # noqa: TC003
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.classes.classes import Conclusions, Decisions, Roles

email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
name_pattern = r"^[А-яЁёIV\-\s\.\,\'\(\)]*$"


class Model(BaseModel):
    """Base Pydantic model."""

    model_config = ConfigDict(
        validate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,
        use_enum_values=True,
    )


class Login(BaseModel):
    """Pydantic model for login form."""

    username: str
    password: str
    new_pswd: str | None

    @field_validator("username")
    @classmethod
    def username_check(cls, v: str) -> str:
        """Check username."""
        return v.lower()


class UserForm(Model):
    """Pydantic model for user form."""

    fullname: str
    username: str
    email: str = Field(pattern=email_pattern)
    role: Roles

    @field_validator("username")
    @classmethod
    def username_check(cls, v: str) -> str:
        """Check username."""
        return v.lower()


class Session(UserForm):
    """Pydantic model for session."""

    id: int


class User(UserForm):
    """Pydantic model for user form."""

    id: int | None
    passhash: str | None
    pswd_create: datetime
    change_pswd: bool
    blocked: bool
    deleted: bool
    attempt: int
    created_at: datetime | None
    updated_at: datetime | None


class Actions(Model):
    """Pydantic model for user actions form."""

    item: Literal["reset", "block", "delete"] | Roles


class Index(BaseModel):
    """Pydantic model for pagination."""

    page: int
    per_page: int
    search: str | None

    @field_validator("search")
    @classmethod
    def search_check(cls, v: str) -> list | None:
        """Check username."""
        if v:
            return v.upper().split(maxsplit=3)[:3]
        return None


class PersonIn(Model):
    """Person schema."""

    id: int | None
    surname: str = Field(alias="lastName", pattern=name_pattern)
    firstname: str = Field(alias="firstName", pattern=name_pattern)
    patronymic: str | None = Field(alias="midName")
    birthday: date
    birthplace: str | None
    citizenship: str | None = Field(alias="citizen")
    dual: str | None = Field(alias="additionalCitizenship")
    snils: str | None
    inn: str | None
    marital: str | None = Field(alias="maritalStatus")
    addition: str | None
    destination: str | None
    editable: bool | None = True

    @field_validator("surname", "firstname", "patronymic")
    @classmethod
    def check_names(cls, v: str) -> str:
        """Check names."""
        return v.upper() if v else ""


class Items(Model):
    """Pydantic model for items."""

    id: int | None
    created_at: datetime | None
    updated_at: datetime | None

    @field_validator("*")
    @classmethod
    def none_check(cls, v: str) -> str | None:
        """Check username."""
        return None if v == "" else v

class PersonOut(Items):
    """Pydantic model for person."""

    surname: str
    firstname: str
    patronymic: str | None
    birthday: date
    birthplace: str | None
    citizenship: str | None
    dual: str | None
    snils: str | None
    inn: str | None
    marital: str | None
    addition: str | None
    destination: str | None
    editable: bool = False
    user_id: int


class Candidates(PersonOut):
    """Pydantic model for candidates."""

    username: str
    total: int


class Prev(Items):
    """Previous schema."""

    surname: str | None = Field(alias="lastNameBeforeChange")
    firstname: str | None = Field(alias="firstNameBeforeChange")
    patronymic: str | None = Field(alias="midNameBeforeChange")
    changed: str | None = Field(alias="yearOfChange")
    reason: str | None
    item: Literal["previous"]


class Education(Items):
    """Educations schema."""

    view: str | None = Field(alias="educationType")
    institution: str = Field(alias="institutionName")
    finished: str | None = Field(alias="endYear")
    specialty: str | None
    item: Literal["educations"]


class Staff(Items):
    """Staffs schema."""

    position: str
    department: str | None
    item: Literal["staffs"]


class Document(Items):
    """Documents schema."""

    view: str | None = Field(alias="documentType")
    series: str | None
    digits: str
    agency: str | None
    issue: date | None
    item: Literal["documents"]


class Address(Items):
    """Addresses schema."""

    view: str
    address: str
    item: Literal["addresses"]


class Contact(Items):
    """Contacts schema."""

    view: str
    contact: str
    item: Literal["contacts"]


class Workplace(Items):
    """Workplaces schema."""

    now_work: bool | None = Field(default=False, alias="currentJob")
    starts: date | None = Field(alias="beginDate")
    finished: date | None = Field(default=None, alias="endDate")
    workplace: str | None = Field(alias="name")
    address: str | None
    position: str
    reason: str | None = Field(alias="fireReason")
    item: Literal["workplaces"]


class Affilation(Items):
    """Affilations schema."""

    view: str | None = Field(alias="organizationType")
    organization: str | None = Field(alias="name")
    inn: str | None
    item: Literal["affilations"]


class Check(Items):
    """Checks schema."""

    workplace: str | None
    document: str | None
    inn: str | None
    debt: str | None
    bankruptcy: str | None
    bki: str | None
    courts: str | None
    affilation: str | None
    terrorist: str | None
    mvd: str | None
    internet: str | None
    cronos: str | None
    cros: str | None
    addition: str | None
    comment: str | None
    conclusion: Conclusions
    item: Literal["checks"]


class Poligraf(Items):
    """Poligraf schema."""

    theme: str
    results: str | None
    conclusion: Decisions
    item: Literal["poligrafs"]


class Investigation(Items):
    """Investigations schema."""

    theme: str
    info: str
    item: Literal["investigations"]


class Inquiry(Items):
    """Inquiries schema."""

    info: str
    initiator: str
    item: Literal["inquiries"]


class AnketaJson(PersonIn):
    """Candidate anketa schema."""

    email: str | None = Field(pattern=email_pattern)
    department: str | None
    position: str = Field(alias="positionName")
    series: str | None = Field(alias="passportSerial")
    digits: str = Field(alias="passportNumber")
    issue: date | None = Field(default=None, alias="passportIssueDate")
    agency: str | None = Field(alias="passportIssuedBy")
    valid_address: str = Field(alias="validAddress")
    reg_address: str = Field(alias="regAddress")
    contact_phone: str = Field(alias="contactPhone")
    education: list[Education] = []
    experience: list[Workplace] = []
    organizations: list[Affilation] = []
    name_was_changed: list[Prev] = Field(
        default=[],
        alias="nameWasChanged",
    )
    related_organizations: list[Affilation] = Field(
        default=[],
        alias="relatedPersonsOrganizations",
    )
    state_organizations: list[Affilation] = Field(
        default=[],
        alias="stateOrganizations",
    )
    public_organizations: list[Affilation] = Field(
        default=[],
        alias="publicOfficeOrganizations",
    )


ItemType = Annotated[
    Address
    | Affilation
    | Check
    | Contact
    | Document
    | Education
    | Inquiry
    | Investigation
    | Prev
    | Poligraf
    | Staff
    | Workplace,
    Field(discriminator="item"),
]


class ItemModel(BaseModel):
    """Base model for item."""

    item: ItemType


class ItemsModel(BaseModel):
    """Base model for items list."""

    item: list[ItemType]
