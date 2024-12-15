"""PyDantic models."""

from __future__ import annotations

import os
import platform
import re
import unicodedata
from datetime import date  # noqa: TC003
from typing import Any, Literal

from pydantic import BaseModel, Field, validator

from .classes import Conclusions, Regions, Roles  # noqa: TC001


class Login(BaseModel):
    """Pydantic model for login form."""

    username: str
    password: str
    new_pswd: str | None


class Search(BaseModel):
    """Pydantic model for search form."""

    search: str | None


class Region(BaseModel):
    """Pydantic model for region form."""

    region: Regions

    class Config:
        """Pydantic config."""

        use_enum_values = True


class Info(BaseModel):
    """Pydantic model for info form."""

    start: date
    end: date
    region: Regions | None

    class Config:
        """Pydantic config."""

        use_enum_values = True


class UserActions(BaseModel):
    """Pydantic model for user actions form."""

    item: Literal["drop", "block", "delete"] | Roles | Regions

    class Config:
        """Pydantic config."""

        use_enum_values = True


class Model(BaseModel):
    """Pydantic model for model form."""

    id: int | str | None = None

    class Config:
        """Pydantic config."""

        use_enum_values = True


class User(Model):
    """Pydantic model for user form."""

    fullname: str
    username: str
    email: str | None = ""


class Person(Model):
    """Pydantic model for person form."""

    __modelname__ = "persons"

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

    view: str
    institution: str
    finished: str | int = ""
    specialty: str | None = ""


class Staff(Model):
    """Pydantic model for staff form."""

    __modelname__ = "staffs"

    position: str
    department: str | None = ""


class Document(Model):
    """Pydantic model for document form."""

    __modelname__ = "documents"

    view: str
    series: str | None = ""
    digits: str
    agency: str | None = ""
    issue: date


class Address(Model):
    """Pydantic model for address form."""

    __modelname__ = "addresses"

    view: str
    addresses: str


class Contact(Model):
    """Pydantic model for contact form."""

    __modelname__ = "contacts"

    view: str
    contact: str


class Workplace(Model):
    """Pydantic model for workplace form."""

    __modelname__ = "workplaces"

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

    view: str
    organization: str
    inn: str | None = ""


class Relation(Model):
    """Pydantic model for relation form."""

    __modelname__ = "relations"

    type: str
    right_id: int | str


class Check(Model):
    """Pydantic model for check form."""

    __modelname__ = "checks"

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

    theme: str
    results: str


class Investigation(Model):
    """Pydantic model for investigation form."""

    __modelname__ = "investigations"

    theme: str
    info: str


class Inquiry(Model):
    """Pydantic model for inquiry form."""

    __modelname__ = "inquiries"

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


class AnketaSchemaJson(BaseModel):
    """Pydantic model for anketa schema."""

    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    mid_name: str = Field(default="", alias="midName")
    birthday: date
    birthplace: str | None = ""
    citizen: str | None = ""
    additional: str = Field(default="", alias="additionalCitizenship")
    marital_status: str = Field(default="", alias="maritalStatus")
    inn: str | None = ""
    snils: str | None = ""
    position_name: str = Field(default="", alias="positionName")
    department: str | None = ""
    passport_serial: str = Field(default="", alias="passportSerial")
    passport_number: str = Field(default="", alias="passportNumber")
    passport_issue: date = Field(default=None, alias="passportIssueDate")
    passport_issued: str = Field(default="", alias="passportIssuedBy")
    valid_address: str = Field(default="", alias="validAddress")
    reg_address: str = Field(default="", alias="regAddress")
    email: str | None = ""
    contact_phone: str = Field(default="", alias="contactPhone")
    education: list[EducationJson] = []
    experience: list[ExperienceJson] = []
    name_was_changed: list[NameWasChangedJson] = []
    organizations: list[OrganizationsJson] = []
    related_organizations: list[RelatedPersonsOrganizationsJson] = []
    state_organizations: list[StateOrganizationsJson] = []
    public_organizations: list[PublicOfficeOrganizationsJson] = []

    @validator("last_name", "first_name", "mid_name")
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
