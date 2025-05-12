"""PyDantic models."""

from __future__ import annotations

import os
import platform
import re
import unicodedata
from datetime import date  # noqa: TC003
from typing import Any, Literal

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

class Search(BaseModel):
    """Pydantic model for person search form."""

    search: str = ""
    pagination: int = 10
    editable: bool = False


class Model(BaseModel):
    """Base Pydantic model."""

    class Config:
        """Pydantic config."""

        use_enum_values = True



class User(Model):
    """Pydantic model for user form."""

    id: int | str | None = None
    fullname: str
    username: str
    email: str | None = ""
    region: str = Regions.main.name
    role: str = Roles.user.value

    @validator("username")
    @classmethod
    def username_check(cls, v: str) -> str:
        """Check username."""
        return v.strip().lower()


class UserActions(Model):
    """Pydantic model for user actions form."""

    item: Literal["reset", "block", "delete"] | Roles | Regions | None


class Region(Model):
    """Pydantic model for region select form."""

    region: Regions


class Person(Model):
    """Pydantic model for person form."""

    __modelname__ = "persons"

    id: int | str | None = None
    surname: str = Field(regex=r"^[А-яЁё][А-яЁёIV\-\s\.\,\'\(\)]*[А-яЁё\s]$")  # noqa: RUF001
    firstname: str = Field(regex=r"^[А-яЁё][А-яЁёIV\-\s\.\,\'\(\)]*[А-яЁё\s]$")  # noqa: RUF001
    patronymic: str | None = Field(
        regex=r"^$|^[А-яЁё][А-яЁёIV\-\s\.\,\'\(\)]*[А-яЁё\s]$",  # noqa: RUF001
        default="",
    )
    birthday: date
    birthplace: str | None = ""
    citizenship: str | None = ""
    dual: str | None = ""
    snils: str | None = ""
    inn: str | None = ""
    marital: str | None = ""
    addition: str | None = ""
    destination: str | None = ""
    region: Regions = ""
    editable: bool = False
    user_id: str | int = None

    @validator("surname", "firstname", "patronymic")
    @classmethod
    def check_names(cls, v: str) -> str:
        """Check names."""
        return v.upper().strip() if v else ""


class Prev(Model):
    """Pydantic model for previous form."""

    __modelname__ = "previous"

    id: int | str | None = None
    surname: str
    firstname: str | None = ""
    patronymic: str | None = ""
    changed: str | None = ""
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
    view: str
    institution: str
    finished: str | int = ""
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
    now_work: bool = False
    starts: date
    finished: date
    workplace: str
    addresses: str | None = ""
    position: str
    reason: str | None = ""


class Affilation(Model):
    """Pydantic model for affilation form."""

    __modelname__ = "affilations"

    id: int | str | None = None
    view: str
    organization: str
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


class NameWasChangedJson(BaseModel):
    """Pydantic model for name was changed item."""

    first_name: str = Field(alias="firstNameBeforeChange")
    last_name: str = Field(default="", alias="lastNameBeforeChange")
    mid_name: str = Field(default="", alias="midNameBeforeChange")
    year_change: str | int = Field(default="", alias="yearOfChange")
    reason: str | None = ""


class EducationJson(BaseModel):
    """Pydantic model for education item."""

    education_type: str = Field(default="", alias="educationType")
    institution_name: str = Field(default="", alias="institutionName")
    end_year: str | int = Field(default="", alias="endYear")
    specialty: str | None = ""


class ExperienceJson(BaseModel):
    """Pydantic model for experience item."""

    begin_date: date = Field(alias="beginDate")
    end_date: date = Field(default=None, alias="endDate")
    current_job: bool = Field(default=False, alias="currentJob")
    name: str | None = ""
    address: str | None = ""
    position: str | None = ""
    fire_reason: str = Field(default="", alias="fireReason")


class OrganizationsJson(BaseModel):
    """Pydantic model for organizations item."""

    name: str | None = ""
    inn: str | None = ""


class RelatedPersonsOrganizationsJson(BaseModel):
    """Pydantic model for related persons organizations item."""

    name: str | None = ""
    inn: str | None = ""


class StateOrganizationsJson(BaseModel):
    """Pydantic model for state organizations item."""

    name: str | None = ""


class PublicOfficeOrganizationsJson(BaseModel):
    """Pydantic model for public office organizations item."""

    name: str | None = ""


class AnketaJson(BaseModel):
    """Pydantic model for anketa schema."""

    surname: str = Field(alias="lastName")
    firstname: str = Field(alias="firstName")
    patronymic: str = Field(default="", alias="midName")
    birthday: date
    birthplace: str | None = ""
    citizen: str | None = ""
    dual: str = Field(default="", alias="additionalCitizenship")
    marital: str = Field(default="", alias="maritalStatus")
    inn: str | None = ""
    snils: str | None = ""
    position_name: str = Field(default="", alias="positionName")
    department: str | None = ""
    series: str = Field(default="", alias="passportSerial")
    digits: str = Field(default="", alias="passportNumber")
    issue: date = Field(default=None, alias="passportIssueDate")
    agency: str = Field(default="", alias="passportIssuedBy")
    valid_address: str = Field(default="", alias="validAddress")
    reg_address: str = Field(default="", alias="regAddress")
    email: str | None = ""
    contact_phone: str = Field(default="", alias="contactPhone")
    education: list[EducationJson] = []
    experience: list[ExperienceJson] = []
    name_was_changed: list[NameWasChangedJson] = Field(
        default=[],
        alias="nameWasChanged",
    )
    organizations: list[OrganizationsJson] = []
    related_organizations: list[RelatedPersonsOrganizationsJson] = Field(
        default=[],
        alias="relatedPersonsOrganizations",
    )
    state_organizations: list[StateOrganizationsJson] = Field(
        default=[],
        alias="stateOrganizations",
    )
    public_organizations: list[PublicOfficeOrganizationsJson] = Field(
        default=[],
        alias="publicOfficeOrganizations",
    )

    @validator("surname", "firstname", "patronymic")
    @classmethod
    def check_names(cls, v: str) -> str:
        """Check names."""
        return v.upper().strip() if v else ""


class File(BaseModel):
    """Pydantic model for file."""

    file: Any
    filename: str

    @validator("filename")
    @classmethod
    def check_filename(cls, v: str) -> str:
        """Check filename for valid chars."""
        filename_ascii_strip_re = re.compile(r"[^A-Za-zА-ЯЁа-яё0-9_.-]")  # noqa: RUF001
        windows_device_files = (
            "CON",
            "AUX",
            "COM1",
            "COM2",
            "COM3",
            "COM4",
            "LPT1",
            "LPT2",
            "LPT3",
            "PRN",
            "NUL",
        )
        filename = unicodedata.normalize("NFKD", v)
        for sep in os.sep, os.path.altsep:
            if sep:
                filename = filename.replace(sep, " ")
        filename = str(
            filename_ascii_strip_re.sub("", "_".join(filename.split())),
        ).strip("._")
        if (
            platform.system().lower() == "windows"
            and filename
            and filename.split(".")[0].upper() in windows_device_files
        ):
            filename = f"_{filename}"
        return filename
