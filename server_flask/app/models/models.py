"""PyDantic models."""

from __future__ import annotations

from datetime import date, datetime  # noqa: TC003
from typing import Any, Literal

from pydantic import BaseModel, Field, validator

from app.classes.classes import Conclusions, Decisions, Roles


class Model(BaseModel):
    """Base Pydantic model."""

    class Config:
        """Pydantic config."""

        allow_population_by_field_name = True
        anystr_strip_whitespace = True
        orm_mode = True
        use_enum_values = True


class Result(BaseModel):
    """Result Model."""

    data: tuple[Any, int] = Field(ge=100, le=999)


class BaseResponse(BaseModel):
    """Base model for response."""

    message: str


class ResumeResponse(BaseModel):
    """MOdel for resume creation return."""

    person_id: int | None
    exists: bool


class AuthResponse(BaseModel):
    """Pydantic model for auth."""

    message: str | None
    access_token: str | None
    refresh_token: str | None


class Login(BaseModel):
    """Pydantic model for login form."""

    username: str
    password: str
    new_pswd: str | None

    @validator("username")
    @classmethod
    def username_check(cls, v: str) -> str:
        """Check username."""
        return v.lower()


class Token(BaseModel):
    """JWT payloads."""

    id: int
    fullname: str
    username: str
    email: str
    role: Roles
    exp: datetime

    class Config:
        """Pydantic config."""

        use_enum_values = True


class Refresh(BaseModel):
    """Refresh token payload."""

    id: int
    exp: datetime


class UserForm(BaseModel):
    """Pydantic model for user form."""

    fullname: str
    username: str
    email: str
    role: Roles = Roles.guest.value

    @validator("username")
    @classmethod
    def username_check(cls, v: str) -> str:
        """Check username."""
        return v.lower()

    @validator("fullname")
    @classmethod
    def fullname_check(cls, v: str) -> str:
        """Check fullname."""
        return v.upper()

    class Config:
        """Pydantic config."""

        use_enum_values = True


class User(UserForm, Model):
    """Pydantic model for user form."""

    id: int | None
    pswd_create: datetime
    change_pswd: bool
    blocked: bool
    deleted: bool
    attempt: int
    created: datetime | str | None


class UserActions(BaseModel):
    """Pydantic model for user actions form."""

    item: Literal["reset", "block", "delete"] | Roles

    class Config:
        """Pydantic config."""

        use_enum_values = True


class Index(BaseModel):
    """Pydantic model for pagination."""

    page: int
    per_page: int
    search: str | None = None


class PersonIn(Model):
    """Person schema."""

    __PATTERN = r"^[А-яЁёIV\-\s\.\,\'\(\)]*$"

    id: int | None
    surname: str = Field(alias="lastName", regex=__PATTERN)
    firstname: str = Field(alias="firstName", regex=__PATTERN)
    patronymic: str | None = Field(default="", alias="midName")
    birthday: date
    birthplace: str | None = ""
    citizenship: str | None = Field(default="", alias="citizen")
    dual: str | None = Field(default="", alias="additionalCitizenship")
    snils: str | None = ""
    inn: str | None = ""
    marital: str | None = Field(default="", alias="maritalStatus")
    addition: str | None = ""
    destination: str | None = ""
    editable: bool = False
    created: datetime | str | None

    @validator("surname", "firstname", "patronymic")
    @classmethod
    def check_names(cls, v: str) -> str:
        """Check names."""
        return v.upper() if v else ""


class PersonOut(Model):
    """Pydantic model for person."""

    id: int | None
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
    editable: bool
    created: datetime | str | None
    user_id: int


class Candidates(Model):
    """Pydantic model for candidate."""

    id: int | None
    fullname: str
    birthday: date
    editable: bool
    username: str
    total: int
    created: datetime | str | None


class Prev(Model):
    """Previous schema."""

    id: int | None
    surname: str | None = Field(alias="lastNameBeforeChange")
    firstname: str | None = Field(alias="firstNameBeforeChange")
    patronymic: str | None = Field(default="", alias="midNameBeforeChange")
    changed: str | int | None = Field(default="", alias="yearOfChange")
    reason: str | None = ""
    created: datetime | str | None


class Education(Model):
    """Educations schema."""

    id: int | None
    view: str | None = Field(default="", alias="educationType")
    institution: str = Field(default="", alias="institutionName")
    finished: str | int | None = Field(default="", alias="endYear")
    specialty: str | None = ""
    created: datetime | str | None


class Staff(Model):
    """Staffs schema."""

    id: int | None
    position: str
    department: str | None = ""
    created: datetime | str | None


class Document(Model):
    """Documents schema."""

    id: int | None
    view: str | None = Field(default="", alias="documentType")
    series: str | None = ""
    digits: str
    agency: str | None = ""
    issue: date | None
    created: datetime | str | None


class Address(Model):
    """Addresses schema."""

    id: int | None
    view: str
    address: str
    created: datetime | str | None


class Contact(Model):
    """Contacts schema."""

    id: int | None
    view: str
    contact: str
    created: datetime | str | None


class Workplace(Model):
    """Workplaces schema."""

    id: int | None
    now_work: bool | None = Field(default=False, alias="currentJob")
    starts: date | None = Field(alias="beginDate")
    finished: date | None = Field(default=None, alias="endDate")
    workplace: str | None = Field(alias="name")
    address: str | None = ""
    position: str
    reason: str | None = Field(default="", alias="fireReason")
    created: datetime | str | None


class Affilation(Model):
    """Affilations schema."""

    id: int | None
    view: str | None = Field(default="", alias="organizationType")
    organization: str | None = Field(default="", alias="name")
    inn: str | None = ""
    created: datetime | str | None


class Check(Model):
    """Checks schema."""

    id: int | None
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
    created: datetime | str | None


class Poligraf(Model):
    """Poligraf schema."""

    id: int | None
    theme: str
    results: str | None
    conclusion: Decisions
    created: datetime | str | None


class Investigation(Model):
    """Investigations schema."""

    id: int | None
    theme: str
    info: str
    created: datetime | str | None


class Inquiry(Model):
    """Inquiries schema."""

    id: int | None
    info: str
    initiator: str
    origins: str | None = ""
    created: datetime | str | None


class AnketaJson(PersonIn):
    """Candidate anketa schema."""

    position: str = Field(default="", alias="positionName")
    department: str | None = ""
    series: str | None = Field(default="", alias="passportSerial")
    digits: str = Field(default="", alias="passportNumber")
    issue: date | None = Field(default=None, alias="passportIssueDate")
    agency: str | None = Field(default="", alias="passportIssuedBy")
    valid_address: str = Field(default="", alias="validAddress")
    reg_address: str = Field(default="", alias="regAddress")
    email: str | None = ""
    contact_phone: str = Field(default="", alias="contactPhone")
    education: list[Education] = []
    experience: list[Workplace] = []
    name_was_changed: list[Prev] = Field(
        default=[],
        alias="nameWasChanged",
    )
    organizations: list[Affilation] = []
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
