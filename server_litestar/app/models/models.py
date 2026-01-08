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
    new_pswd: str | None = None

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
    role: Roles = Roles.guest.value

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
    pswd_create: datetime
    change_pswd: bool
    blocked: bool
    deleted: bool
    attempt: int
    created: datetime | str | None


class Actions(Model):
    """Pydantic model for user actions form."""

    item: Literal["reset", "block", "delete"] | Roles


class Index(BaseModel):
    """Pydantic model for pagination."""

    page: int
    per_page: int
    search: str | None = None

    @field_validator("search")
    @classmethod
    def search_check(cls, v: str) -> list | None:
        """Check username."""
        if v:
            return v.upper().split(maxsplit=3)[:3]
        return None


class PersonIn(Model):
    """Person schema."""

    id: int | None = None
    surname: str = Field(alias="lastName", pattern=name_pattern)
    firstname: str = Field(alias="firstName", pattern=name_pattern)
    patronymic: str | None = Field(default="", alias="midName")
    birthday: date = None
    birthplace: str | None = ""
    citizenship: str | None = Field(default="", alias="citizen")
    dual: str | None = Field(default="", alias="additionalCitizenship")
    snils: str | None = ""
    inn: str | None = ""
    marital: str | None = Field(default="", alias="maritalStatus")
    addition: str | None = ""
    destination: str | None = ""
    editable: bool = True

    @field_validator("surname", "firstname", "patronymic")
    @classmethod
    def check_names(cls, v: str) -> str:
        """Check names."""
        return v.upper() if v else ""


class Items(Model):
    """Pydantic model for items."""

    id: int | None = None
    created: datetime | str | None = None


class PersonOut(Items):
    """Pydantic model for person."""

    surname: str
    firstname: str
    patronymic: str | None = ""
    birthday: date
    birthplace: str | None = ""
    citizenship: str | None = ""
    dual: str | None = ""
    snils: str | None = ""
    inn: str | None = ""
    marital: str | None = ""
    addition: str | None = ""
    destination: str | None = ""
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
    patronymic: str | None = Field(default="", alias="midNameBeforeChange")
    changed: str | int | None = Field(default="", alias="yearOfChange")
    reason: str | None = ""
    item: Literal["previous"] = None


class Education(Items):
    """Educations schema."""

    view: str | None = Field(default="", alias="educationType")
    institution: str = Field(default="", alias="institutionName")
    finished: str | int | None = Field(default="", alias="endYear")
    specialty: str | None = ""
    item: Literal["educations"] = None


class Staff(Items):
    """Staffs schema."""

    position: str
    department: str | None = ""
    item: Literal["staffs"] = None


class Document(Items):
    """Documents schema."""

    view: str | None = Field(default="", alias="documentType")
    series: str | None = ""
    digits: str
    agency: str | None = ""
    issue: date | None
    item: Literal["documents"] = None


class Address(Items):
    """Addresses schema."""

    view: str
    address: str
    item: Literal["addresses"] = None


class Contact(Items):
    """Contacts schema."""

    view: str
    contact: str
    item: Literal["contacts"] = None


class Workplace(Items):
    """Workplaces schema."""

    now_work: bool | None = Field(default=False, alias="currentJob")
    starts: date | None = Field(alias="beginDate")
    finished: date | None = Field(default=None, alias="endDate")
    workplace: str | None = Field(alias="name")
    address: str | None = ""
    position: str
    reason: str | None = Field(default="", alias="fireReason")
    item: Literal["workplaces"] = None


class Affilation(Items):
    """Affilations schema."""

    view: str | None = Field(default="", alias="organizationType")
    organization: str | None = Field(default="", alias="name")
    inn: str | None = ""
    item: Literal["affilations"] = None


class Check(Items):
    """Checks schema."""

    workplace: str | None = ""
    document: str | None = ""
    inn: str | None = ""
    debt: str | None = ""
    bankruptcy: str | None = ""
    bki: str | None = ""
    courts: str | None = ""
    affilation: str | None = ""
    terrorist: str | None = ""
    mvd: str | None = ""
    internet: str | None = ""
    cronos: str | None = ""
    cros: str | None = ""
    addition: str | None = ""
    comment: str | None = ""
    conclusion: Conclusions
    item: Literal["checks"] = None


class Poligraf(Items):
    """Poligraf schema."""

    theme: str
    results: str | None
    conclusion: Decisions
    item: Literal["poligrafs"] = None


class Investigation(Items):
    """Investigations schema."""

    theme: str
    info: str
    item: Literal["investigations"] = None


class Inquiry(Items):
    """Inquiries schema."""

    info: str
    initiator: str
    origins: str | None = ""
    item: Literal["inquiries"] = None


class AnketaJson(PersonIn):
    """Candidate anketa schema."""

    email: str | None = Field(pattern=email_pattern)
    department: str | None = ""
    position: str = Field(default="", alias="positionName")
    series: str | None = Field(default="", alias="passportSerial")
    digits: str = Field(default="", alias="passportNumber")
    issue: date | None = Field(default=None, alias="passportIssueDate")
    agency: str | None = Field(default="", alias="passportIssuedBy")
    valid_address: str = Field(default="", alias="validAddress")
    reg_address: str = Field(default="", alias="regAddress")
    contact_phone: str = Field(default="", alias="contactPhone")
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
