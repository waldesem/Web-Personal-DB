"""PyDantic models."""

from __future__ import annotations

from datetime import date, datetime  # noqa: TC003
from typing import Any, Literal

from pydantic import BaseModel, Field, validator

from app.classes.classes import Conclusions, Decisions, Roles


class Model(BaseModel):
    """Base Pydantic model."""

    id: int | None
    created: datetime | str | None

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


class ResumeModel(BaseModel):
    """MOdel for resume creation return."""

    person_id: int | None
    exists: bool


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


class Auth(BaseModel):
    """Pydantic model for auth."""

    message: str
    access_token: str | None


class Token(BaseModel):
    """JWT payloads."""

    id: int
    fullname: str
    username: str
    email: str
    role: Roles
    exp: datetime
    jti: str

    class Config:
        """Pydantic config."""

        use_enum_values = True


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

    pswd_create: datetime
    change_pswd: bool
    blocked: bool
    deleted: bool
    attempt: int


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

    @validator("surname", "firstname", "patronymic")
    @classmethod
    def check_names(cls, v: str) -> str:
        """Check names."""
        return v.upper() if v else ""


class PersonOut(Model):
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
    editable: bool
    user_id: int


class Candidates(Model):
    """Pydantic model for candidate."""

    fullname: str
    birthday: date
    editable: bool
    username: str
    total: int


class Prev(Model):
    """Previous schema."""

    surname: str | None = Field(alias="lastNameBeforeChange")
    firstname: str | None = Field(alias="firstNameBeforeChange")
    patronymic: str | None = Field(default="", alias="midNameBeforeChange")
    changed: str | int | None = Field(default="", alias="yearOfChange")
    reason: str | None = ""


class Education(Model):
    """Educations schema."""

    view: str | None = Field(default="", alias="educationType")
    institution: str = Field(default="", alias="institutionName")
    finished: str | int | None = Field(default="", alias="endYear")
    specialty: str | None = ""


class Staff(Model):
    """Staffs schema."""

    position: str
    department: str | None = ""


class Document(Model):
    """Documents schema."""

    view: str
    series: str | None = ""
    digits: str
    agency: str | None = ""
    issue: date | None


class Address(Model):
    """Addresses schema."""

    view: str
    addresses: str


class Contact(Model):
    """Contacts schema."""

    view: str
    contact: str


class Workplace(Model):
    """Workplaces schema."""

    now_work: bool | None = Field(default=False, alias="currentJob")
    starts: date | None = Field(alias="beginDate")
    finished: date | None = Field(default=None, alias="endDate")
    workplace: str | None = Field(alias="name")
    addresses: str | None = ""
    position: str
    reason: str | None = Field(default="", alias="fireReason")


class Affilation(Model):
    """Affilations schema."""

    view: str | None = ""
    organization: str | None = Field(default="", alias="name")
    inn: str | None = ""


class Check(Model):
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


class Poligraf(Model):
    """Poligraf schema."""

    theme: str
    results: str | None
    conclusion: Decisions


class Investigation(Model):
    """Investigations schema."""

    theme: str
    info: str


class Inquiry(Model):
    """Inquiries schema."""

    info: str
    initiator: str
    origins: str | None = ""


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
