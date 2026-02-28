"""PyDantic models."""

from __future__ import annotations

from datetime import date, datetime  # noqa: TC003
from typing import Annotated, Literal

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    computed_field,
)

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

    username: Annotated[str, Field(max_length=255), AfterValidator(lambda v: v.lower())]
    password: Annotated[str, Field(max_length=255)]
    new_pswd: Annotated[str | None, Field(None, max_length=255)]


class UserForm(Model):
    """Pydantic model for user form."""

    fullname: Annotated[str, Field(max_length=255)]
    username: Annotated[str, Field(max_length=255), AfterValidator(lambda v: v.lower())]
    email: Annotated[str, Field(pattern=email_pattern)]
    role: Annotated[Roles, Field(Roles.guest)]


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
    created_at: datetime | None
    updated_at: datetime | None


class Actions(Model):
    """Pydantic model for user actions form."""

    item: Literal["reset", "block", "delete"] | Roles


class Index(BaseModel):
    """Pydantic model for pagination."""

    page: int
    per_page: int
    search: Annotated[
        str | None,
        Field(None, max_length=255),
        AfterValidator(lambda v: v.upper().split(maxsplit=3)[:3] if v else None),
    ]


class Items(Model):
    """Pydantic model for items."""

    id: Annotated[int | None, Field(None)]
    created_at: Annotated[datetime | None, Field(None)]
    updated_at: Annotated[datetime | None, Field(None)]


class Person(Items):
    """Person schema."""

    surname: Annotated[
        str,
        Field(alias="lastName", pattern=name_pattern),
        AfterValidator(lambda v: v.upper()),
    ]
    firstname: Annotated[
        str,
        Field(alias="firstName", pattern=name_pattern),
        AfterValidator(lambda v: v.upper()),
    ]
    patronymic: Annotated[
        str | None,
        Field(default=None, alias="midName"),
        AfterValidator(lambda v: v.upper() if v else None),
    ]
    birthday: date
    birthplace: Annotated[str | None, Field(None, max_length=255)]
    citizenship: Annotated[
        str | None,
        Field(default=None, alias="citizen", max_length=255),
    ]
    dual: Annotated[
        str | None,
        Field(default=None, alias="additionalCitizenship", max_length=255),
    ]
    snils: Annotated[str | None, Field(default=None, max_length=11)]
    inn: Annotated[str | None, Field(default=None, max_length=12)]
    marital: Annotated[
        str | None,
        Field(default=None, alias="maritalStatus", max_length=255),
    ]
    addition: str | None = None
    destination: str | None = None
    editable: bool | None = True


class Candidates(Items):
    """Pydantic model for candidates."""

    surname: str
    firstname: str
    patronymic: str | None
    birthday: date
    editable: bool
    username: str
    total: int

    @computed_field
    @property
    def fullname(self) -> str:
        """Compute field."""
        return f"{self.surname} {self.firstname} {self.patronymic or ''}".rstrip()


class Prev(Items):
    """Previous schema."""

    surname: str = Field(alias="lastNameBeforeChange", max_length=255)
    firstname: Annotated[
        str | None,
        Field(default=None, alias="firstNameBeforeChange", max_length=255),
    ]
    patronymic: Annotated[
        str | None,
        Field(default=None, alias="midNameBeforeChange", max_length=255),
    ]
    changed: Annotated[
        str | None,
        Field(default=None, alias="yearOfChange", max_length=4),
    ]
    reason: str | None = None
    item: Literal["previous"] = "previous"


class Education(Items):
    """Educations schema."""

    view: Annotated[
        str | None,
        Field(default=None, alias="educationType", max_length=255),
    ]
    institution: Annotated[str, Field(alias="institutionName")]
    finished: Annotated[
        str | None,
        Field(default=None, alias="endYear"),
        BeforeValidator(lambda v: str(v)),
    ]
    specialty: str | None = None
    item: Literal["educations"] = "educations"


class Staff(Items):
    """Staffs schema."""

    position: str
    department: str | None = None
    item: Literal["staffs"]


class Document(Items):
    """Documents schema."""

    view: Annotated[str | None, Field(default="Паспорт", alias="documentType")]
    series: str | None = None
    digits: Annotated[str, Field(max_length=12)]
    agency: Annotated[str | None, Field(default=None, alias="endYear", max_length=255)]
    issue: date | None = None
    item: Literal["documents"]


class Address(Items):
    """Addresses schema."""

    view: Annotated[str, Field(max_length=255)]
    address: Annotated[str, Field(max_length=255)]
    item: Literal["addresses"]


class Contact(Items):
    """Contacts schema."""

    view: Annotated[str, Field(max_length=255)]
    contact: Annotated[str, Field(max_length=255)]
    item: Literal["contacts"]


class Workplace(Items):
    """Workplaces schema."""

    now_work: Annotated[bool | None, Field(default=False, alias="currentJob")]
    starts: Annotated[date | None, Field(alias="beginDate")]
    finished: Annotated[date | None, Field(default=None, alias="endDate")]
    workplace: Annotated[str | None, Field(default=None, alias="name")]
    address: Annotated[str | None, Field(None, max_length=255)]
    position: Annotated[str, Field(max_length=255)]
    reason: Annotated[str | None, Field(default=None, alias="fireReason")]
    item: Literal["workplaces"] = "workplaces"


class Affilation(Items):
    """Affilations schema."""

    view: Annotated[str | None, Field(default=None, alias="organizationType")]
    organization: Annotated[str, Field(alias="name")]
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


class AnketaJson(Person):
    """Candidate anketa schema."""

    email: Annotated[str | None, Field(pattern=email_pattern)]
    department: str | None = None
    position: Annotated[str, Field(alias="positionName", max_length=255)]
    series: Annotated[str | None, Field(default=None, alias="passportSerial")]
    digits: Annotated[str, Field(alias="passportNumber", max_length=12)]
    issue: Annotated[
        date | None,
        Field(default=None, alias="passportIssueDate"),
    ]
    agency: Annotated[
        str | None,
        Field(default=None, alias="passportIssuedBy", max_length=255),
    ]
    valid_address: Annotated[str, Field(alias="validAddress", max_length=255)]
    reg_address: Annotated[str, Field(alias="regAddress", max_length=255)]
    contact_phone: Annotated[str, Field(alias="contactPhone", max_length=255)]
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
