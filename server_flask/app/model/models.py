"""PyDantic models."""

from __future__ import annotations

from datetime import date  # noqa: TC003
from typing import Literal

from pydantic import BaseModel, Field, validator

from .classes import Conclusions, Decisions, Regions, Roles


class Login(BaseModel):
    """Pydantic model for login form."""

    username: str
    password: str
    new_pswd: str | None

    @validator("username")
    @classmethod
    def username_check(cls, v: str) -> str:
        """Check username."""
        return v.strip().lower()


class Model(BaseModel):
    """Base Pydantic model."""

    class Config:
        """Pydantic config."""

        use_enum_values = True
        allow_population_by_field_name = True


class Phone(Model):
    """Pydantic model for phone form."""

    __modelname__ = "phones"

    id: int | str | None = None
    organization: str
    fullname: str | None = ""
    phone: str | None = ""
    mobile: str | None = ""
    email: str | None = ""
    comments: str | None = ""

    @validator("organization", "fullname")
    @classmethod
    def name_check(cls, v: str) -> str:
        """Check name."""
        return v.strip().upper()


class Region(Model):
    """Pydantic model for region select form."""

    region: Regions


class User(Model):
    """Pydantic model for user form."""

    id: int | str | None = None
    fullname: str
    username: str
    email: str | None = ""
    region: Regions = Regions.main.name
    role: Roles = Roles.guest.value

    @validator("username")
    @classmethod
    def username_check(cls, v: str) -> str:
        """Check username."""
        return v.strip().lower()

    @validator("fullname")
    @classmethod
    def fullname_check(cls, v: str) -> str:
        """Check fullname."""
        return v.strip().upper()


class UserActions(Model):
    """Pydantic model for user actions form."""

    item: Literal["reset", "block", "delete"] | Roles | Regions | None


class Person(Model):
    """Pydantic model for person form."""

    __modelname__ = "persons"

    __PATTERN = r"^[А-яЁёIV\-\s\.\,\'\(\)]*$"

    id: int | str | None = None
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
    region: None | Regions
    editable: bool = False

    @validator("surname", "firstname", "patronymic")
    @classmethod
    def check_names(cls, v: str) -> str:
        """Check names."""
        return v.upper().strip() if v else ""


class Items(BaseModel):
    """Base Pydantic model for items."""

    items: Literal[
        "previous",
        "educations",
        "addresses",
        "affilations",
        "staffs",
        "workplaces",
        "contacts",
        "documents",
        "checks",
        "poligrafs",
        "inquiries",
        "investigations",
    ]


class Prev(Model):
    """Pydantic model for previous form."""

    __modelname__ = "previous"

    id: int | str | None = None
    surname: str = Field(default="", alias="lastNameBeforeChange")
    firstname: str = Field(alias="firstNameBeforeChange")
    patronymic: str = Field(default="", alias="midNameBeforeChange")
    changed: str | int = Field(default="", alias="yearOfChange")
    reason: str | None = ""

    @validator("surname", "firstname", "patronymic")
    @classmethod
    def check_names(cls, v: str) -> str:
        """Check names."""
        return v.upper().strip() if v else ""


class Education(Model):
    """Pydantic model for education form."""

    __modelname__ = "educations"

    id: int | str | None = None
    view: str = Field(default="", alias="educationType")
    institution: str = Field(default="", alias="institutionName")
    finished: str | int = Field(default="", alias="endYear")
    specialty: str | None = ""


class Staff(Model):
    """Pydantic model for staff form."""

    __modelname__ = "staffs"

    id: int | str | None = None
    position: str
    department: str | None = ""


class Document(Model):
    """Pydantic model for document form."""

    __modelname__ = "documents"

    id: int | str | None = None
    view: str
    series: str | None = ""
    digits: str
    agency: str | None = ""
    issue: date


class Address(Model):
    """Pydantic model for address form."""

    __modelname__ = "addresses"

    id: int | str | None = None
    view: str
    addresses: str


class Contact(Model):
    """Pydantic model for contact form."""

    __modelname__ = "contacts"

    id: int | str | None = None
    view: str
    contact: str


class Workplace(Model):
    """Pydantic model for workplace form."""

    __modelname__ = "workplaces"

    id: int | str | None = None
    now_work: bool = Field(default=False, alias="currentJob")
    starts: date = Field(alias="beginDate")
    finished: date = Field(default=None, alias="endDate")
    workplace: str | None = ""
    addresses: str | None = ""
    position: str | None = ""
    reason: str = Field(default="", alias="fireReason")


class Affilation(Model):
    """Pydantic model for affilation form."""

    __modelname__ = "affilations"

    id: int | str | None = None
    view: str | None = ""
    organization: str = Field(default="", alias="name")
    inn: str | None = ""


class Check(Model):
    """Pydantic model for check form."""

    __modelname__ = "checks"

    id: int | str | None = None
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

    __modelname__ = "poligrafs"

    id: int | str | None = None
    theme: str
    results: str
    conclusion: Decisions


class Investigation(Model):
    """Pydantic model for investigation form."""

    __modelname__ = "investigations"

    id: int | str | None = None
    theme: str
    info: str


class Inquiry(Model):
    """Pydantic model for inquiry form."""

    __modelname__ = "inquiries"

    id: int | str | None = None
    info: str
    initiator: str
    origins: str | None = ""


class AnketaJson(Person):
    """Pydantic model for anketa schema."""

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
