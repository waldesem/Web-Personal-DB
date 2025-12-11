"""PyDantic models."""

from __future__ import annotations

import re
from datetime import date, datetime  # noqa: TC003
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from app.classes.classes import Conclusions, Decisions, Roles

email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

Items = Literal[
    "addresses",
    "affilations",
    "checks",
    "contacts",
    "documents",
    "educations",
    "inquiries",
    "investigations",
    "previous",
    "poligrafs",
    "staffs",
    "workplaces",
]


class Model(BaseModel):
    """Base Pydantic model."""

    model_config = ConfigDict(
        validate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,
        use_enum_values=True,
    )


class Reply(BaseModel):
    """Base model for response."""

    message: str


class ResumeResponse(BaseModel):
    """MOdel for resume creation return."""

    person_id: int | None
    exists: bool


class AuthResponse(BaseModel):
    """Pydantic model for auth."""

    message: str | None
    access_token: str | None = None
    refresh_token: str | None = None


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


class UserActions(Model):
    """Pydantic model for user actions form."""

    item: Literal["reset", "block", "delete"] | Roles


class Index(BaseModel):
    """Pydantic model for pagination."""

    page: int
    per_page: int
    search: str | None = None

    @field_validator("search")
    @classmethod
    def search_check(cls, v: str) -> str | None:
        """Check username."""
        if v:
            return v.upper().split(maxsplit=3)[:3]
        return None


class PersonIn(Model):
    """Person schema."""

    id: int | None = None
    surname: str = Field(alias="lastName", pattern=r"^[А-яЁёIV\-\s\.\,\'\(\)]*$")
    firstname: str = Field(alias="firstName", pattern=r"^[А-яЁёIV\-\s\.\,\'\(\)]*$")
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
    editable: bool = False
    created: datetime | str | None = None

    @field_validator("surname", "firstname", "patronymic")
    @classmethod
    def check_names(cls, v: str) -> str:
        """Check names."""
        return v.upper() if v else ""


class PersonOut(Model):
    """Pydantic model for person."""

    id: int | None = None
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
    created: datetime | str | None = None
    user_id: int


class Candidates(PersonOut):
    """Pydantic model for candidates."""

    username: str
    total: int


class Prev(Model):
    """Previous schema."""

    __modelname__ = "previous"

    id: int | None = None
    surname: str | None = Field(alias="lastNameBeforeChange")
    firstname: str | None = Field(alias="firstNameBeforeChange")
    patronymic: str | None = Field(default="", alias="midNameBeforeChange")
    changed: str | int | None = Field(default="", alias="yearOfChange")
    reason: str | None = ""
    created: datetime | str | None = None


class Education(Model):
    """Educations schema."""

    __modelname__ = "educations"

    id: int | None = None
    view: str | None = Field(default="", alias="educationType")
    institution: str = Field(default="", alias="institutionName")
    finished: str | int | None = Field(default="", alias="endYear")
    specialty: str | None = ""
    created: datetime | str | None = None


class Staff(Model):
    """Staffs schema."""

    __modelname__ = "staffs"

    id: int | None = None
    position: str
    department: str | None = ""
    created: datetime | str | None = None


class Document(Model):
    """Documents schema."""

    __modelname__ = "documents"

    id: int | None = None
    view: str | None = Field(default="", alias="documentType")
    series: str | None = ""
    digits: str
    agency: str | None = ""
    issue: date | None
    created: datetime | str | None = None


class Address(Model):
    """Addresses schema."""

    __modelname__ = "addresses"

    id: int | None = None
    view: str
    address: str
    created: datetime | str | None = None


class Contact(Model):
    """Contacts schema."""

    __modelname__ = "contacts"

    id: int | None = None
    view: str
    contact: str
    created: datetime | str | None = None

    @field_validator("contact")
    @classmethod
    def check_contact(cls, v: str, values: dict) -> str:
        """Check contact."""
        if values.get("view") == "Электронная почта":
            if re.findall(email_pattern, v):
                return v
            msg = "Неправильный формат электронной почты"
            raise ValidationError(msg)
        return v


class Workplace(Model):
    """Workplaces schema."""

    __modelname__ = "workplaces"

    id: int | None = None
    now_work: bool | None = Field(default=False, alias="currentJob")
    starts: date | None = Field(alias="beginDate")
    finished: date | None = Field(default=None, alias="endDate")
    workplace: str | None = Field(alias="name")
    address: str | None = ""
    position: str
    reason: str | None = Field(default="", alias="fireReason")
    created: datetime | str | None = None


class Affilation(Model):
    """Affilations schema."""

    __modelname__ = "affilations"

    id: int | None = None
    view: str | None = Field(default="", alias="organizationType")
    organization: str | None = Field(default="", alias="name")
    inn: str | None = ""
    created: datetime | str | None = None


class Check(Model):
    """Checks schema."""

    __modelname__ = "checks"

    id: int | None = None
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
    created: datetime | str | None = None


class Poligraf(Model):
    """Poligraf schema."""

    __modelname__ = "poligrafs"

    id: int | None = None
    theme: str
    results: str | None
    conclusion: Decisions
    created: datetime | str | None = None


class Investigation(Model):
    """Investigations schema."""

    __modelname__ = "investigations"

    id: int | None = None
    theme: str
    info: str
    created: datetime | str | None = None


class Inquiry(Model):
    """Inquiries schema."""

    __modelname__ = "inquiries"

    id: int | None = None
    info: str
    initiator: str
    origins: str | None = ""
    created: datetime | str | None = None


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


models: dict[Items, Model] = {
    model.__modelname__: model
    for model in Model.__subclasses__()
    if "__modelname__" in model.__dict__
}
