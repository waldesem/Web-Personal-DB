"""PyDantic models."""

from __future__ import annotations

from datetime import date, datetime  # noqa: TC003
from typing import Literal

from pydantic import BaseModel, Field, validator

from app.utils.utilities import Conclusions, Decisions, Regions, Roles


class Index(BaseModel):
    """Pydantic model for pagination."""

    page: int
    per_page: int
    search: str | None = None


class Token(BaseModel):
    """Pydantic model for JWT."""

    id: str | int
    fullname: str
    username: str
    email: str
    region: Regions
    role: Roles
    exp: datetime
    jti: str

    class Config:
        """Pydantic config."""

        use_enum_values = True


class Region(BaseModel):
    """Pydantic model for region select form."""

    region: Regions

    class Config:
        """Pydantic config."""

        use_enum_values = True


class UserActions(BaseModel):
    """Pydantic model for user actions form."""

    item: Literal["reset", "block", "delete"] | Roles | Regions | None


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
        orm_mode = True
        allow_population_by_field_name = True


class OutputModel(BaseModel):
    """Pydantic model for outputs."""

    created: datetime


class InputUser(Model):
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


class OutputUser(InputUser, OutputModel):
    """Pydantic model for user form."""

    pswd_create: datetime
    change_pswd: bool
    blocked: bool
    deleted: bool
    attempt: int


class InputPerson(Model):
    """Pydantic model for person form."""

    __modelname__ = "input_persons"

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


class OutputPerson(InputPerson, OutputModel):
    """Pydantic model for person form."""

    __modelname__ = "output_persons"

    user_id: int


class OutputCandidate(OutputPerson):
    """Pydantic model for candidate."""

    username: str


class InputPrev(Model):
    """Pydantic model for previous form."""

    __modelname__ = "Input_previous"

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


class OutputPrev(InputPrev, OutputModel):
    """Pydantic model for previous form."""

    __modelname__ = "output_previous"


class InputEducation(Model):
    """Pydantic model for education form."""

    __modelname__ = "input_educations"

    id: int | str | None = None
    view: str = Field(default="", alias="educationType")
    institution: str = Field(default="", alias="institutionName")
    finished: str | int = Field(default="", alias="endYear")
    specialty: str | None = ""


class OutputEducation(InputEducation, OutputModel):
    """Pydantic model for previous form."""

    __modelname__ = "output_educations"


class InputStaff(Model):
    """Pydantic model for staff form."""

    __modelname__ = "input_staffs"

    id: int | str | None = None
    position: str
    department: str | None = ""


class OutputStaff(InputStaff, OutputModel):
    """Pydantic model for staff form."""

    __modelname__ = "output_staffs"


class InputDocument(Model):
    """Pydantic model for document form."""

    __modelname__ = "input_documents"

    id: int | str | None = None
    view: str
    series: str | None = ""
    digits: str
    agency: str | None = ""
    issue: date


class OutputDocument(InputDocument, OutputModel):
    """Pydantic model for document form."""

    __modelname__ = "output_documents"


class InputAddress(Model):
    """Pydantic model for address form."""

    __modelname__ = "input_addresses"

    id: int | str | None = None
    view: str
    addresses: str


class OutputOutputAddressPrev(InputAddress, OutputModel):
    """Pydantic model for address form."""

    __modelname__ = "output_addresses"


class InputContact(Model):
    """Pydantic model for contact form."""

    __modelname__ = "input_contacts"

    id: int | str | None = None
    view: str
    contact: str


class OutputContact(InputContact, OutputModel):
    """Pydantic model for contact form."""

    __modelname__ = "output_contacts"


class InputWorkplace(Model):
    """Pydantic model for workplace form."""

    __modelname__ = "input_workplaces"

    id: int | str | None = None
    now_work: bool = Field(default=False, alias="currentJob")
    starts: date = Field(alias="beginDate")
    finished: date = Field(default=None, alias="endDate")
    workplace: str | None = ""
    addresses: str | None = ""
    position: str | None = ""
    reason: str = Field(default="", alias="fireReason")


class OutputWorkplace(InputWorkplace, OutputModel):
    """Pydantic model for workplace form."""

    __modelname__ = "output_workplaces"


class InputAffilation(Model):
    """Pydantic model for affilation form."""

    __modelname__ = "input_affilations"

    id: int | str | None = None
    view: str | None = ""
    organization: str = Field(default="", alias="name")
    inn: str | None = ""


class OutputAffilation(InputAffilation, OutputModel):
    """Pydantic model for affilation form."""

    __modelname__ = "output_affilations"


class InputCheck(Model):
    """Pydantic model for check form."""

    __modelname__ = "input_checks"

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


class OutOutputCheckputPrev(InputCheck, OutputModel):
    """Pydantic model for check form."""

    __modelname__ = "output_checks"


class InputPoligraf(Model):
    """Pydantic model for poligraf form."""

    __modelname__ = "input_poligrafs"

    id: int | str | None = None
    theme: str
    results: str
    conclusion: Decisions


class OutputPoligraf(InputPoligraf, OutputModel):
    """Pydantic model for poligraf form."""

    __modelname__ = "output_poligrafs"


class InputInvestigation(Model):
    """Pydantic model for investigation form."""

    __modelname__ = "input_investigations"

    id: int | str | None = None
    theme: str
    info: str


class OutputInvestigation(InputInvestigation, OutputModel):
    """Pydantic model for investigation form."""

    __modelname__ = "output_investigations"


class InputInquiry(Model):
    """Pydantic model for inquiry form."""

    __modelname__ = "input_inquiries"

    id: int | str | None = None
    info: str
    initiator: str
    origins: str | None = ""


class OutputInquiry(InputInquiry, OutputModel):
    """Pydantic model for inquiries form."""

    __modelname__ = "output_inquiries"


class AnketaJson(InputPerson):
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
    education: list[InputEducation] = []
    experience: list[InputWorkplace] = []
    name_was_changed: list[InputPrev] = Field(
        default=[],
        alias="nameWasChanged",
    )
    organizations: list[InputAffilation] = []
    related_organizations: list[InputAffilation] = Field(
        default=[],
        alias="relatedPersonsOrganizations",
    )
    state_organizations: list[InputAffilation] = Field(
        default=[],
        alias="stateOrganizations",
    )
    public_organizations: list[InputAffilation] = Field(
        default=[],
        alias="publicOfficeOrganizations",
    )
