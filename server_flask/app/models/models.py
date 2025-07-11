"""PyDantic models."""

from __future__ import annotations

from datetime import date, datetime  # noqa: TC003
from typing import Literal

from pydantic import BaseModel, Field, validator

from app.utils.utilities import Conclusions, Decisions, Regions, Roles


class ModelIn(BaseModel):
    """Base Pydantic model."""

    id: int | str | None = None

    class Config:
        """Pydantic config."""

        use_enum_values = True
        anystr_strip_whitespace = True
        allow_population_by_field_name = True


class ModelOut(ModelIn):
    """Pydantic model for outs."""

    created: datetime

    class Config:
        """Pydantic config."""

        orm_mode = True


class BaseResponse(BaseModel):
    """Pydantic model for Base Response."""

    message: str


class Index(BaseModel):
    """Pydantic model for pagination."""

    page: int
    per_page: int
    search: str | None = None


class PersonExists(BaseModel):
    """Person Exists."""

    person_id: int | None
    exists: bool


class Token(ModelIn):
    """Pydantic model for JWT."""

    fullname: str
    username: str
    email: str
    region: Regions
    role: Roles
    exp: datetime
    jti: str


class Region(ModelIn):
    """Pydantic model for region select form."""

    region: Regions


class UserActions(ModelIn):
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
        return v.lower()


class UserIn(ModelIn):
    """Pydantic model for user form."""

    fullname: str
    username: str
    email: str | None = ""
    region: Regions = Regions.main.name
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


class UserOut(UserIn, ModelOut):
    """Pydantic model for user form."""

    pswd_create: datetime
    change_pswd: bool
    blocked: bool
    deleted: bool
    attempt: int


class PersonIn(ModelIn):
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
    region: None | Regions
    editable: bool = False

    @validator("surname", "firstname", "patronymic")
    @classmethod
    def check_names(cls, v: str) -> str:
        """Check names."""
        return v.upper() if v else ""


class PersonOut(PersonIn, ModelOut):
    """Pydantic model for person."""

    user_id: int | None


class Candidates(ModelOut):
    """Pydantic model for candidate."""

    fullname: str
    birthday: date
    region: Regions
    editable: bool
    username: str
    total: int


class PrevIn(ModelIn):
    """Pydantic model for previous form."""

    __modelname__ = "previous"

    surname: str = Field(alias="lastNameBeforeChange")
    firstname: str = Field(alias="firstNameBeforeChange")
    patronymic: str = Field(default="", alias="midNameBeforeChange")
    changed: str | int = Field(default="", alias="yearOfChange")
    reason: str | None = ""

    @validator("surname", "firstname", "patronymic")
    @classmethod
    def check_names(cls, v: str) -> str:
        """Check names."""
        return v.upper() if v else ""


class PrevOut(PrevIn, ModelOut):
    """Pydantic model for previous form."""

    __modelname__ = "previous"


class EducationIn(ModelIn):
    """Pydantic model for education form."""

    __modelname__ = "educations"

    view: str = Field(default="", alias="educationType")
    institution: str = Field(default="", alias="institutionName")
    finished: str | int = Field(default="", alias="endYear")
    specialty: str | None = ""


class EducationOut(EducationIn, ModelOut):
    """Pydantic model for previous form."""

    __modelname__ = "educations"


class StaffIn(ModelIn):
    """Pydantic model for staff form."""

    __modelname__ = "staffs"

    position: str
    department: str | None = ""


class StaffOut(StaffIn, ModelOut):
    """Pydantic model for staff form."""

    __modelname__ = "staffs"


class DocumentIn(ModelIn):
    """Pydantic model for document form."""

    __modelname__ = "documents"

    view: str
    series: str | None = ""
    digits: str
    agency: str | None = ""
    issue: date


class DocumentOut(DocumentIn, ModelOut):
    """Pydantic model for document form."""

    __modelname__ = "documents"


class AddressIn(ModelIn):
    """Pydantic model for address form."""

    __modelname__ = "addresses"

    view: str
    addresses: str


class AddressOut(AddressIn, ModelOut):
    """Pydantic model for address form."""

    __modelname__ = "addresses"


class ContactIn(ModelIn):
    """Pydantic model for contact form."""

    __modelname__ = "contacts"

    view: str
    contact: str


class ContactOut(ContactIn, ModelOut):
    """Pydantic model for contact form."""

    __modelname__ = "contacts"


class WorkplaceIn(ModelIn):
    """Pydantic model for workplace form."""

    __modelname__ = "workplaces"

    now_work: bool = Field(default=False, alias="currentJob")
    starts: date = Field(alias="beginDate")
    finished: date = Field(default=None, alias="endDate")
    workplace: str | None = ""
    addresses: str | None = ""
    position: str | None = ""
    reason: str = Field(default="", alias="fireReason")


class WorkplaceOut(WorkplaceIn, ModelOut):
    """Pydantic model for workplace form."""

    __modelname__ = "workplaces"


class AffilationIn(ModelIn):
    """Pydantic model for affilation form."""

    __modelname__ = "affilations"

    view: str | None = ""
    organization: str = Field(default="", alias="name")
    inn: str | None = ""


class AffilationOut(AffilationIn, ModelOut):
    """Pydantic model for affilation form."""

    __modelname__ = "affilations"


class CheckIn(ModelIn):
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


class CheckOut(CheckIn, ModelOut):
    """Pydantic model for check form."""

    __modelname__ = "checks"


class PoligrafIn(ModelIn):
    """Pydantic model for poligraf form."""

    __modelname__ = "poligrafs"

    theme: str
    results: str
    conclusion: Decisions


class PoligrafOut(PoligrafIn, ModelOut):
    """Pydantic model for poligraf form."""

    __modelname__ = "poligrafs"


class InvestigationIn(ModelIn):
    """Pydantic model for investigation form."""

    __modelname__ = "investigations"

    theme: str
    info: str


class InvestigationOut(InvestigationIn, ModelOut):
    """Pydantic model for investigation form."""

    __modelname__ = "investigations"


class InquiryIn(ModelIn):
    """Pydantic model for inquiry form."""

    __modelname__ = "inquiries"

    info: str
    initiator: str
    origins: str | None = ""


class InquiryOut(InquiryIn, ModelOut):
    """Pydantic model for inquiries form."""

    __modelname__ = "inquiries"


class AnketaJson(PersonIn):
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
    education: list[EducationIn] = []
    experience: list[WorkplaceIn] = []
    name_was_changed: list[PrevIn] = Field(
        default=[],
        alias="nameWasChanged",
    )
    organizations: list[AffilationIn] = []
    related_organizations: list[AffilationIn] = Field(
        default=[],
        alias="relatedPersonsOrganizations",
    )
    state_organizations: list[AffilationIn] = Field(
        default=[],
        alias="stateOrganizations",
    )
    public_organizations: list[AffilationIn] = Field(
        default=[],
        alias="publicOfficeOrganizations",
    )
