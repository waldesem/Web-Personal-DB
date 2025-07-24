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

    person_id: int
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


class Token(BaseModel):
    """Pydantic model for JWT."""

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
    """Pydantic model for person form."""

    __PATTERN = r"^[А-яЁёIV\-\s\.\,\'\(\)]*$"

    surname: str = Field(alias="lastName", regex=__PATTERN)
    firstname: str = Field(alias="firstName", regex=__PATTERN)
    patronymic: str = Field(default="", alias="midName")
    birthday: date
    birthplace: str | None = ""
    citizenship: str = Field(default="", alias="citizen")
    dual: str = Field(default="", alias="additionalCitizenship")
    snils: str | None = ""
    inn: str | None = ""
    marital: str = Field(default="", alias="maritalStatus")
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
    """Pydantic model for previous form."""

    surname: str = Field(alias="lastNameBeforeChange")
    firstname: str = Field(alias="firstNameBeforeChange")
    patronymic: str = Field(default="", alias="midNameBeforeChange")
    changed: str | int = Field(default="", alias="yearOfChange")
    reason: str | None = ""


class Education(Model):
    """Pydantic model for education form."""

    view: str = Field(default="", alias="educationType")
    institution: str = Field(default="", alias="institutionName")
    finished: str | int = Field(default="", alias="endYear")
    specialty: str | None = ""


class Staff(Model):
    """Pydantic model for staff form."""

    position: str
    department: str | None = ""


class Document(Model):
    """Pydantic model for document form."""

    view: str
    series: str | None = ""
    digits: str
    agency: str | None = ""
    issue: date


class Address(Model):
    """Pydantic model for address form."""

    view: str
    addresses: str


class Contact(Model):
    """Pydantic model for contact form."""

    view: str
    contact: str


class Workplace(Model):
    """Pydantic model for workplace form."""

    now_work: bool = Field(default=False, alias="currentJob")
    starts: date = Field(alias="beginDate")
    finished: date = Field(default=None, alias="endDate")
    workplace: str | None = ""
    addresses: str | None = ""
    position: str | None = ""
    reason: str = Field(default="", alias="fireReason")


class Affilation(Model):
    """Pydantic model for affilation form."""

    view: str | None = ""
    organization: str = Field(default="", alias="name")
    inn: str | None = ""


class Check(Model):
    """Pydantic model for check form."""

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
    """Pydantic model for poligraf form."""

    theme: str
    results: str
    conclusion: Decisions


class Investigation(Model):
    """Pydantic model for investigation form."""

    theme: str
    info: str


class Inquiry(Model):
    """Pydantic model for inquiry form."""

    info: str
    initiator: str
    origins: str | None = ""


class AnketaJson(PersonIn):
    """Schema for uploadig candidate anketa."""

    position: str = Field(default="", alias="positionName")
    department: str | None = ""
    series: str = Field(default="", alias="passportSerial")
    digits: str = Field(default="", alias="passportNumber")
    issue: date = Field(default=None, alias="passportIssueDate")
    agency: str = Field(default="", alias="passportIssuedBy")
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
