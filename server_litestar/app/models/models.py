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
    email: Annotated[str, Field(pattern=email_pattern)]
    role: Roles = Roles.guest

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
    passhash: str | None = None
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
    patronymic: str | None = Field(default=None, alias="midName")
    birthday: date
    birthplace: str | None = None
    citizenship: str | None = Field(default=None, alias="citizen")
    dual: str | None = Field(default=None, alias="additionalCitizenship")
    snils: str | None = Field(default=None, max_length=11)
    inn: str | None = Field(default=None, max_length=12)
    marital: str | None = Field(default=None, alias="maritalStatus")
    addition: str | None = None
    destination: str | None = None
    editable: bool | None = True

    @field_validator("surname", "firstname", "patronymic")
    @classmethod
    def check_names(cls, v: str) -> str:
        """Check names."""
        return v.upper() if v else ""


class Items(Model):
    """Pydantic model for items."""

    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @field_validator("*")
    @classmethod
    def none_check(cls, v: str) -> str | None:
        """Check username."""
        return None if v == "" else v


class PersonOut(Items):
    """Pydantic model for person."""

    surname: str
    firstname: str
    patronymic: str | None = None
    birthday: date
    birthplace: str | None = None
    citizenship: str | None = None
    dual: str | None = None
    snils: str | None = None
    inn: str | None = None
    marital: str | None = None
    addition: str | None = None
    destination: str | None = None
    editable: bool = False


class Candidates(PersonOut):
    """Pydantic model for candidates."""

    username: str
    total: int


class Prev(Items):
    """Previous schema."""

    surname: str = Field(alias="lastNameBeforeChange")
    firstname: str | None = Field(default=None, alias="firstNameBeforeChange")
    patronymic: str | None = Field(default=None, alias="midNameBeforeChange")
    changed: str | None = Field(default=None, alias="yearOfChange", max_length=4)
    reason: str | None = None
    item: Literal["previous"] = "previous"


class Education(Items):
    """Educations schema."""

    view: str | None = Field(default=None, alias="educationType")
    institution: str = Field(alias="institutionName")
    finished: str | int | None = Field(default=None, alias="endYear")
    specialty: str | None = None
    item: Literal["educations"] = "educations"


class Staff(Items):
    """Staffs schema."""

    position: str
    department: str | None = None
    item: Literal["staffs"]


class Document(Items):
    """Documents schema."""

    view: str | None = Field(default="Паспорт", alias="documentType")
    series: str | None = None
    digits: str
    agency: str | None = None
    issue: date | None = None
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
    workplace: str | None = Field(default=None, alias="name")
    address: str | None = None
    position: str
    reason: str | None = Field(default=None, alias="fireReason")
    item: Literal["workplaces"] = "workplaces"


class Affilation(Items):
    """Affilations schema."""

    view: str | None = Field(default=None, alias="organizationType")
    organization: str = Field(alias="name")
    inn: str | None = None
    item: Literal["affilations"] = "affilations"


class Check(Items):
    """Checks schema."""

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
    comment: str | None = None
    conclusion: Conclusions
    item: Literal["checks"]


class Poligraf(Items):
    """Poligraf schema."""

    theme: str
    results: str
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
    department: str | None = None
    position: str = Field(alias="positionName")
    series: str | None = Field(default=None, alias="passportSerial")
    digits: str = Field(alias="passportNumber")
    issue: date | None = Field(default=None, alias="passportIssueDate")
    agency: str | None = Field(default=None, alias="passportIssuedBy")
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


class ItemModel(BaseModel):
    """Base model for item."""

    item: (
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
        | Workplace
    ) = Field(discriminator="item")


class ItemsModel(BaseModel):
    """Base model for items list."""

    items: list[ItemModel]
