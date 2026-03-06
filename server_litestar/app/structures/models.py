"""PyDantic models."""

from __future__ import annotations

import re
from datetime import date, datetime  # noqa: TC003
from typing import Annotated, Literal

from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
)

from app.structures.classes import Conclusions, Decisions, Roles

email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
name_pattern = r"^[А-яЁёIV\-\s\.\,\'\(\)]*$"


class AuthResponse(BaseModel):
    """Tokens."""

    message: Literal["success", "denied", "updated", "delete"]
    access_token: str | None = None
    refresh_token: str | None = None


class AuthLogin(BaseModel):
    """Pydantic model for login form."""

    username: Annotated[str, Field(max_length=255), AfterValidator(lambda v: v.lower())]
    password: Annotated[str, Field(max_length=255)]


class UpdateLogin(AuthLogin):
    """Pydantic model for login form."""

    new_pswd: Annotated[str, Field(max_length=255)]

    @field_validator("new_pswd")
    @classmethod
    def check_pswd(cls, p: str) -> str:
        """Check password."""
        if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,16}$", p):
            return p
        raise ValidationError


class UserForm(BaseModel):
    """Pydantic model for user form."""

    fullname: Annotated[str, Field(max_length=255)]
    username: Annotated[str, Field(max_length=255), AfterValidator(lambda v: v.lower())]
    email: Annotated[str, Field(pattern=email_pattern)]
    role: Annotated[Roles, Field(Roles.guest)]

    model_config = ConfigDict(str_strip_whitespace=True, use_enum_values=True)


class Session(UserForm):
    """Pydantic model for session."""

    id: int


class User(Session):
    """Pydantic model for user form."""

    pswd_create: datetime
    change_pswd: bool
    blocked: bool
    deleted: bool
    attempt: int
    created_at: datetime
    updated_at: datetime


class Actions(BaseModel):
    """Pydantic model for user actions form."""

    item: Literal["reset", "block", "delete"] | Roles

    model_config = ConfigDict(use_enum_values=True)


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

    created_at: datetime
    updated_at: datetime


class PersonIn(BaseModel):
    """Person schema."""

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
    snils: Annotated[str | None, Field(default=None, max_length=11)]
    inn: Annotated[str | None, Field(default=None, max_length=12)]
    marital: Annotated[str | None, Field(default=None, max_length=255)]
    addition: str | None = None
    destination: str | None = None
    editable: bool | None = True

    model_config = ConfigDict(str_strip_whitespace=True)

    @field_validator("inn", mode="after")
    @classmethod
    def validate_inn(cls, inn: str) -> str:
        """Check inn."""
        c1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0, 0]
        c2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0]
        check1 = sum([int(inn[i]) * c1[i] for i in range(12)]) % 11 % 10
        check2 = sum([int(inn[i]) * c2[i] for i in range(12)]) % 11 % 10
        if check1 == int(inn[10]) and check2 == int(inn[11]):
            return inn
        raise ValidationError

    @field_validator("snils", mode="after")
    @classmethod
    def validate_snils(cls, snils: str) -> str:
        """Check snils."""
        # Получаем первые 9 цифр и контрольное число (последние 2)
        digits = [int(d) for d in snils]
        main_part = digits[:9]
        check_sum = int(snils[9:])

        # Вычисляем контрольную сумму
        sum_prod = sum(main_part[i] * (9 - i) for i in range(9))

        # Алгоритм проверки контрольного числа
        calculated_sum = 0
        if sum_prod < 100:
            calculated_sum = sum_prod
        elif sum_prod in {100, 101}:
            calculated_sum = 0
        else:
            remainder = sum_prod % 101
            calculated_sum = 0 if remainder == 100 else remainder
        if calculated_sum == check_sum:
            return snils
        raise ValidationError


class PersonOut(PersonIn, DateIdModel):
    """Person schema."""

    addition: str | None = None
    destination: str | None = None
    editable: bool


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

    surname: str = Field(max_length=255)
    firstname: Annotated[str | None, Field(default=None, max_length=255)]
    patronymic: Annotated[str | None, Field(default=None, max_length=255)]
    changed: Annotated[str | None, Field(default=None, max_length=4)]
    reason: str | None = None
    item: Literal["previous"]

    model_config = ConfigDict(str_strip_whitespace=True)


class PrevOut(PrevIn, IdModel):
    """Previous out schema."""


class EducationIn(BaseModel):
    """Education in schema."""

    view: Annotated[str | None, Field(default=None, max_length=255)]
    institution: Annotated[str, Field(max_length=255)]
    finished: Annotated[str | None, Field(default=None), BeforeValidator(str)]
    specialty: str | None = None
    item: Literal["educations"]

    model_config = ConfigDict(str_strip_whitespace=True)


class EducationOut(EducationIn, IdModel):
    """Educations schema."""


class StaffIn(BaseModel):
    """Staffs schema."""

    position: str
    department: str | None = None
    item: Literal["staffs"]

    model_config = ConfigDict(str_strip_whitespace=True)


class StaffOut(StaffIn, IdModel):
    """Staffs out schema."""


class DocumentIn(BaseModel):
    """Document in schema."""

    view: str | None = "Паспорт"
    series: str | None = None
    digits: Annotated[str, Field(max_length=12)]
    agency: Annotated[str | None, Field(default=None, max_length=255)]
    issue: date | None = None
    item: Literal["documents"]

    model_config = ConfigDict(str_strip_whitespace=True)


class DocumentOut(DocumentIn, IdModel):
    """Document out schema."""


class AddressIn(BaseModel):
    """Address in schema."""

    view: Annotated[str, Field(max_length=255)]
    address: Annotated[str, Field(max_length=255)]
    item: Literal["addresses"]

    model_config = ConfigDict(str_strip_whitespace=True)


class AddressOut(AddressIn, IdModel):
    """Address out schema."""


class ContactIn(BaseModel):
    """Contacts in schema."""

    view: Annotated[str, Field(max_length=255)]
    contact: Annotated[str, Field(max_length=255)]
    item: Literal["contacts"]

    model_config = ConfigDict(str_strip_whitespace=True)


class ContactOut(ContactIn, IdModel):
    """Contacts out schema."""


class WorkplaceIn(BaseModel):
    """Workplaces in schema."""

    now_work: bool | None = False
    starts: date | None = None
    finished: date | None = None
    workplace: Annotated[str, Field(max_length=255)]
    address: Annotated[str | None, Field(None, max_length=255)]
    position: Annotated[str, Field(max_length=255)]
    reason: str | None = None
    item: Literal["workplaces"]

    model_config = ConfigDict(str_strip_whitespace=True)


class WorkplaceOut(WorkplaceIn, IdModel):
    """Workplace out schema."""


class AffilationIn(BaseModel):
    """Affilation in schema."""

    view: Annotated[str, Field(max_length=255)]
    organization: Annotated[str, Field(max_length=255)]
    inn: Annotated[str | None, Field(None, max_length=12)]
    item: Literal["affilations"]

    model_config = ConfigDict(str_strip_whitespace=True)


class AffilationOut(AffilationIn, IdModel):
    """Affilations out schema."""


class CheckIn(DateIdModel):
    """Check in schema."""

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

    model_config = ConfigDict(use_enum_values=True)


class CheckOut(CheckIn, DateIdModel):
    """Checks out schema."""


class PoligrafIn(DateIdModel):
    """Poligraf in schema."""

    theme: str
    results: str
    conclusion: Decisions
    item: Literal["poligrafs"]

    model_config = ConfigDict(use_enum_values=True)


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
