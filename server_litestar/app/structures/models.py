"""PyDantic models."""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Annotated, Literal, Self

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

from app.structures.classes import Conclusions, Decisions, Roles

email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
name_pattern = r"^[А-яЁёIV\-\s\.\,\'\(\)]*$"


def check_tz(v: datetime) -> datetime:
    """Check ts."""
    return v if v.tzinfo else v.replace(tzinfo=UTC)


class AuthResponse(BaseModel):
    """Tokens."""

    message: Literal["success", "denied", "updated", "delete"]
    access_token: str | None = None
    refresh_token: str | None = None


class AuthLogin(BaseModel):
    """Pydantic model for login form."""

    model_config = ConfigDict(str_max_length=255, regex_engine="python-re")

    username: Annotated[str, AfterValidator(lambda v: v.lower())]
    password: str


class UpdateLogin(AuthLogin):
    """Pydantic model for login form."""

    new_pswd: Annotated[
        str,
        Field(pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,16}$"),
    ]

    @model_validator(mode="after")
    def check_password(self) -> Self:
        """Check passwords combinations."""
        if self.password == self.new_pswd:
            raise ValidationError
        return self


class UserForm(BaseModel):
    """Pydantic model for user form."""

    model_config = ConfigDict(
        use_enum_values=True,
        str_strip_whitespace=True,
        str_max_length=255,
    )

    fullname: str
    username: Annotated[str, AfterValidator(lambda v: v.lower())]
    email: Annotated[str, Field(pattern=email_pattern)]
    role: Annotated[Roles, Field(Roles.guest.value)]


class Session(UserForm):
    """Pydantic model for session."""

    id: int


class User(Session):
    """Pydantic model for user form."""

    pswd_create: Annotated[datetime, AfterValidator(check_tz)]
    change_pswd: bool
    blocked: bool
    deleted: bool
    attempt: int
    created_at: Annotated[datetime, AfterValidator(check_tz)]
    updated_at: Annotated[datetime, AfterValidator(check_tz)]


class Actions(BaseModel):
    """Pydantic model for user actions form."""

    model_config = ConfigDict(use_enum_values=True)

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


class IdModel(BaseModel):
    """ItemModel schema."""

    id: int


class DateIdModel(IdModel):
    """DateIdModel schema."""

    created_at: Annotated[datetime, AfterValidator(check_tz)]
    updated_at: Annotated[datetime, AfterValidator(check_tz)]


class PersonIn(BaseModel):
    """Person schema."""

    model_config = ConfigDict(str_strip_whitespace=True)

    surname: Annotated[
        str,
        Field(pattern=name_pattern),
        AfterValidator(lambda v: v.upper()),
    ]
    firstname: Annotated[
        str,
        Field(pattern=name_pattern),
        AfterValidator(lambda v: v.upper()),
    ]
    patronymic: Annotated[
        str | None,
        Field(default=None),
        AfterValidator(lambda v: v.upper() if v else None),
    ]
    birthday: date
    birthplace: Annotated[str | None, Field(None, max_length=255)]
    citizenship: Annotated[str | None, Field(default=None, max_length=255)]
    dual: Annotated[str | None, Field(default=None, max_length=255)]
    snils: str | None = None
    inn: str | None = None
    marital: Annotated[str | None, Field(default=None, max_length=255)]
    addition: str | None = None
    destination: str | None = None
    editable: bool | None = True

    @field_validator("inn", mode="after")
    @classmethod
    def validate_inn(cls, inn: str | None) -> str | None:
        """Check inn."""
        try:
            from rust_module import validate_inn  # ty:ignore[unresolved-import]

            return validate_inn(inn)
        except ImportError:
            from app.utilities.utils import validate_inn

            return validate_inn(inn)

    @field_validator("snils", mode="after")
    @classmethod
    def validate_snils(cls, snils: str | None) -> str | None:
        """Check snils."""
        try:
            from rust_module import validate_snils  # ty:ignore[unresolved-import]

            return validate_snils(snils)
        except ImportError:
            from app.utilities.utils import validate_snils

            return validate_snils(snils)


class PersonOut(PersonIn, DateIdModel):
    """Person schema."""

    addition: str | None = None
    destination: str | None = None
    editable: bool
    user_id: int

    @classmethod
    def validate_inn(cls, inn: str | None) -> str | None:
        """Check inn."""
        return inn

    @classmethod
    def validate_snils(cls, snils: str | None) -> str | None:
        """Check snils."""
        return snils


class PersonResponse(BaseModel):
    """Person exists response."""

    person_id: int | None
    exists: bool


class Candidates(BaseModel):
    """Pydantic model for candidates."""

    id: int
    surname: str
    firstname: str
    patronymic: str | None
    birthday: date
    editable: bool
    updated_at: datetime
    username: str
    total: int


class PrevIn(BaseModel):
    """Previous in schema."""

    model_config = ConfigDict(str_strip_whitespace=True)

    surname: str = Field(max_length=255)
    firstname: Annotated[str | None, Field(default=None, max_length=255)]
    patronymic: Annotated[str | None, Field(default=None, max_length=255)]
    changed: Annotated[
        str | None,
        Field(default=None, max_length=4),
        BeforeValidator(str),
    ]
    reason: str | None = None
    item: Literal["previous"]


class PrevOut(PrevIn, IdModel):
    """Previous out schema."""


class EducationIn(BaseModel):
    """Education in schema."""

    model_config = ConfigDict(str_strip_whitespace=True)

    view: Annotated[str | None, Field(default=None, max_length=255)]
    institution: Annotated[str, Field(max_length=255)]
    finished: Annotated[str | None, Field(default=None), BeforeValidator(str)]
    specialty: str | None = None
    item: Literal["educations"]


class EducationOut(EducationIn, IdModel):
    """Educations schema."""


class StaffIn(BaseModel):
    """Staffs schema."""

    model_config = ConfigDict(str_strip_whitespace=True)

    position: str
    department: str | None = None
    item: Literal["staffs"]


class StaffOut(StaffIn, IdModel):
    """Staffs out schema."""


class DocumentIn(BaseModel):
    """Document in schema."""

    model_config = ConfigDict(str_strip_whitespace=True)

    view: str | None = "Паспорт"
    series: str | None = None
    digits: Annotated[str, Field(max_length=12)]
    agency: Annotated[str | None, Field(default=None, max_length=255)]
    issue: date | None = None
    item: Literal["documents"]


class DocumentOut(DocumentIn, IdModel):
    """Document out schema."""


class AddressIn(BaseModel):
    """Address in schema."""

    model_config = ConfigDict(str_strip_whitespace=True, str_max_length=255)

    view: str
    address: str
    item: Literal["addresses"]


class AddressOut(AddressIn, IdModel):
    """Address out schema."""


class ContactIn(BaseModel):
    """Contacts in schema."""

    model_config = ConfigDict(str_strip_whitespace=True, str_max_length=255)

    view: str
    contact: str
    item: Literal["contacts"]


class ContactOut(ContactIn, IdModel):
    """Contacts out schema."""


class WorkplaceIn(BaseModel):
    """Workplaces in schema."""

    model_config = ConfigDict(str_strip_whitespace=True)

    now_work: Annotated[bool | None, BeforeValidator(bool)]
    starts: date | None = None
    finished: Annotated[
        date | None | str,
        AfterValidator(lambda v: None if isinstance(v, str) else v),
    ]
    workplace: Annotated[str, Field(max_length=255)]
    address: Annotated[str | None, Field(None, max_length=255)]
    position: Annotated[str, Field(max_length=255)]
    reason: str | None = None
    item: Literal["workplaces"]


class WorkplaceOut(WorkplaceIn, IdModel):
    """Workplace out schema."""


class AffilationIn(BaseModel):
    """Affilation in schema."""

    model_config = ConfigDict(str_strip_whitespace=True)

    view: Annotated[str, Field(max_length=255)]
    organization: Annotated[str, Field(max_length=255)]
    inn: Annotated[str | None, Field(None, max_length=12)]
    item: Literal["affilations"]


class AffilationOut(AffilationIn, IdModel):
    """Affilations out schema."""


class CheckIn(DateIdModel):
    """Check in schema."""

    model_config = ConfigDict(use_enum_values=True)

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
    person_id: int | None = None
    item: Literal["checks"]


class CheckOut(CheckIn, DateIdModel):
    """Checks out schema."""


class PoligrafIn(DateIdModel):
    """Poligraf in schema."""

    model_config = ConfigDict(use_enum_values=True)

    theme: str
    results: str
    conclusion: Decisions
    item: Literal["poligrafs"]


class PoligrafOut(PoligrafIn, DateIdModel):
    """Poligraf out schema."""


class InvestigationIn(BaseModel):
    """Investigations in schema."""

    theme: str
    info: str
    item: Literal["investigations"]


class InvestigationOut(InvestigationIn, DateIdModel):
    """Investigation out schema."""


class InquiryIn(BaseModel):
    """Inquiries in schema."""

    info: str
    initiator: str
    item: Literal["inquiries"]


class InquiryOut(InquiryIn, DateIdModel):
    """Inquiries out schema."""


ItemTypeIn = Annotated[
    AddressIn
    | AffilationIn
    | CheckIn
    | ContactIn
    | DocumentIn
    | EducationIn
    | InquiryIn
    | InvestigationIn
    | PrevIn
    | PoligrafIn
    | StaffIn
    | WorkplaceIn,
    Field(discriminator="item"),
]


class ItemModelIn(BaseModel):
    """Validation class."""

    item: ItemTypeIn


ItemTypeOut = Annotated[
    AddressOut
    | AffilationOut
    | CheckOut
    | ContactOut
    | DocumentOut
    | EducationOut
    | InquiryOut
    | InvestigationOut
    | PrevOut
    | PoligrafOut
    | StaffOut
    | WorkplaceOut,
    Field(discriminator="item"),
]


class ItemModelOut(BaseModel):
    """Validation class."""

    item: ItemTypeOut


class ItemsOutModels(BaseModel):
    """Validation class."""

    staffs: list[StaffOut]
    educations: list[EducationOut]
    workplaces: list[WorkplaceOut]
    documents: list[DocumentOut]
    addresses: list[AddressOut]
    contacts: list[ContactOut]
    affilations: list[AffilationOut]
    previous: list[PrevOut]
    checks: list[CheckOut]
    poligrafs: list[PoligrafOut]
    investigations: list[InvestigationOut]
    inquiries: list[InquiryOut]


class EducationJson(BaseModel):
    """Education json model."""

    view: Annotated[str, Field(validation_alias="educationType", max_length=255)]
    institution: Annotated[
        str,
        Field(validation_alias="institutionName", max_length=255),
    ]
    finished: Annotated[
        str | None,
        Field(default=None, validation_alias="endYear", max_length=4),
        BeforeValidator(str),
    ]
    specialty: Annotated[
        str | None,
        Field(None, validation_alias="educationType", max_length=255),
    ]


class PrevJson(BaseModel):
    """Previous in schema."""

    surname: str = Field(max_length=255)
    firstname: Annotated[str | None, Field(default=None, max_length=255)]
    patronymic: Annotated[str | None, Field(default=None, max_length=255)]
    changed: Annotated[str | None, Field(default=None, max_length=4)]
    reason: str | None = None


class WorkplaceJson(BaseModel):
    """Workplaces json model."""

    now_work: Annotated[bool, Field(default=False, validation_alias="currentJob")]
    starts: Annotated[date, Field(validation_alias="beginDate")]
    finished: Annotated[date | None, Field(default=None, validation_alias="endDate")]
    workplace: Annotated[str, Field(validation_alias="name", max_length=255)]
    address: Annotated[str | None, Field(None, max_length=255)]
    position: Annotated[str, Field(max_length=255)]
    reason: Annotated[str | None, Field(default=None, validation_alias="fireReason")]


class AffilationJson(BaseModel):
    """Affilation json model."""

    view: Annotated[
        str | None,
        Field(default=None, validation_alias="organizationType", max_length=255),
    ]
    organization: Annotated[str, Field(validation_alias="name", max_length=255)]
    inn: Annotated[str | None, Field(None, max_length=12)]


class AnketaJson(BaseModel):
    """Candidate anketa schema."""

    surname: Annotated[
        str,
        Field(validation_alias="lastName", pattern=name_pattern, max_length=255),
        AfterValidator(lambda v: v.upper()),
    ]
    firstname: Annotated[
        str,
        Field(validation_alias="firstName", pattern=name_pattern, max_length=255),
        AfterValidator(lambda v: v.upper()),
    ]
    patronymic: Annotated[
        str | None,
        Field(default=None, validation_alias="midName", max_length=255),
        AfterValidator(lambda v: v.upper() if v else None),
    ]
    birthday: date
    birthplace: Annotated[str | None, Field(None, max_length=255)]
    citizenship: Annotated[
        str | None,
        Field(default=None, validation_alias="citizen", max_length=255),
    ]
    dual: Annotated[
        str | None,
        Field(default=None, validation_alias="additionalCitizenship", max_length=255),
    ]
    snils: Annotated[str | None, Field(default=None, max_length=11)]
    inn: Annotated[str | None, Field(default=None, max_length=12)]
    marital: Annotated[
        str | None,
        Field(default=None, validation_alias="maritalStatus", max_length=255),
    ]
    email: Annotated[str | None, Field(pattern=email_pattern)]
    department: str | None = None
    position: Annotated[str, Field(validation_alias="positionName", max_length=255)]
    series: Annotated[
        str | None,
        Field(default=None, validation_alias="passportSerial", max_length=12),
    ]
    digits: Annotated[str, Field(validation_alias="passportNumber", max_length=12)]
    issue: Annotated[
        date | None,
        Field(default=None, validation_alias="passportIssueDate"),
    ]
    agency: Annotated[
        str | None,
        Field(default=None, validation_alias="passportIssuedBy", max_length=255),
    ]
    valid_address: Annotated[
        str | None,
        Field(None, validation_alias="validAddress", max_length=255),
    ]
    reg_address: Annotated[
        str | None,
        Field(None, validation_alias="regAddress", max_length=255),
    ]
    contact_phone: Annotated[
        str | None,
        Field(None, validation_alias="contactPhone", max_length=255),
    ]
    education: Annotated[list[EducationJson], Field([])]
    experience: Annotated[list[WorkplaceJson], Field([])]
    name_was_changed: Annotated[
        list[PrevJson],
        Field(
            default=[],
            validation_alias="nameWasChanged",
        ),
    ]
    organizations: Annotated[list[AffilationJson], Field([])]
    related_organizations: Annotated[
        list[AffilationJson],
        Field(
            default=[],
            validation_alias="relatedPersonsOrganizations",
        ),
    ]
    state_organizations: Annotated[
        list[AffilationJson],
        Field(
            default=[],
            validation_alias="stateOrganizations",
        ),
    ]
    public_organizations: Annotated[
        list[AffilationJson],
        Field(
            default=[],
            validation_alias="publicOfficeOrganizations",
        ),
    ]
