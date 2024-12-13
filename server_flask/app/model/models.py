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

    id: int | str | None

    class Config:
        """Pydantic config."""

        use_enum_values = True


class User(Model):
    """Pydantic model for user form."""

    fullname: str
    username: str
    email: str | None


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
    region: Regions | None = ""
    editable: bool | None = False
    user_id: str | int

    @validator("surname", "firstname", "patronymic")
    @classmethod
    def check_names(cls, v: str) -> str | None:
        """Check names."""
        return v.upper().strip() if v else None


class Prev(Model):
    """Pydantic model for previous form."""

    __modelname__ = "previous"

    surname: str
    firstname: str
    patronymic: str | None = ""
    changed: str | None = ""
    reason: str | None = ""

    @validator("surname", "firstname", "patronymic")
    @classmethod
    def check_names(cls, v: str) -> str | None:
        """Check names."""
        return v.upper().strip() if v else None


class Education(Model):
    """Pydantic model for education form."""

    __modelname__ = "educations"

    view: str
    institution: str
    finished: str | int | None = ""
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
    issue: date | None = None


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

    now_work: bool | None = False
    starts: date | None
    finished: date | None
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

    first_name: str | None = Field(alias="firstNameBeforeChange")
    last_name: str | None = Field(default="", alias="lastNameBeforeChange")
    mid_name: str | None = Field(default="", alias="midNameBeforeChange")
    year_change: str | int = Field(default="", alias="yearOfChange")
    reason: str | None = ""


class EducationJson(BaseModel):
    """Pydantic model for education item."""

    education_type: str | None = Field(default="", alias="educationType")
    institution_name: str | None = Field(default="", alias="institutionName")
    end_year: str | int | None = Field(default="", alias="endYear")
    specialty: str | None = ""


class ExperienceJson(BaseModel):
    """Pydantic model for experience item."""

    begin_date: date | None = Field(alias="beginDate")
    end_date: date | None = Field(alias="endDate")
    current_job: bool | None = Field(default=False, alias="currentJob")
    name: str | None = ""
    address: str | None = ""
    position: str | None = ""
    fire_reason: str | None = Field(default="", alias="fireReason")


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
    mid_name: str | None = Field(default="", alias="midName")
    birthday: date
    birthplace: str | None = ""
    citizen: str | None = ""
    additional: str | None = Field(default="", alias="additionalCitizenship")
    marital_status: str | None = Field(default="", alias="maritalStatus")
    inn: str | None = ""
    snils: str | None = ""
    position_name: str | None = Field(default="", alias="positionName")
    department: str | None = ""
    passport_serial: str | None = Field(default="", alias="passportSerial")
    passport_number: str | None = Field(default="", alias="passportNumber")
    passport_issue: date | None = Field(default=None, alias="passportIssueDate")
    passport_issued: str | None = Field(default="", alias="passportIssuedBy")
    valid_address: str | None = Field(default="", alias="validAddress")
    reg_address: str | None = Field(default="", alias="regAddress")
    email: str | None = ""
    contact_phone: str | None = Field(default="", alias="contactPhone")
    education: list[EducationJson] | None = []
    experience: list[ExperienceJson] | None = []
    name_was_changed: list[NameWasChangedJson] | None = []
    organizations: list[OrganizationsJson] | None = []
    related_organizations: list[RelatedPersonsOrganizationsJson] | None = []
    state_organizations: list[StateOrganizationsJson] | None = []
    public_organizations: list[PublicOfficeOrganizationsJson] | None = []

    @validator("last_name", "first_name", "mid_name")
    @classmethod
    def check_names(cls, v: str) -> str | None:
        """Check names."""
        return v.upper().strip() if v else None


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
