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

from app.classes.classes import Conclusions, Decisions, Roles

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
    created_at: datetime | None
    updated_at: datetime | None


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


class Share(BaseModel):
    """Pydantic model for Share."""

    id: Annotated[int | None, Field(None)]
    created_at: Annotated[datetime | None, Field(None)]
    updated_at: Annotated[datetime | None, Field(None)]

    model_config = ConfigDict(
        validate_by_name=True,
        str_strip_whitespace=True,
        use_enum_values=True,
    )


class Person(Share):
    """Person schema."""

    surname: Annotated[
        str,
        Field(validation_alias="lastName", pattern=name_pattern),
        AfterValidator(lambda v: v.upper()),
    ]
    firstname: Annotated[
        str,
        Field(validation_alias="firstName", pattern=name_pattern),
        AfterValidator(lambda v: v.upper()),
    ]
    patronymic: Annotated[
        str | None,
        Field(default=None, validation_alias="midName"),
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
    addition: str | None = None
    destination: str | None = None
    editable: bool | None = True

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


class Candidates(Share):
    """Pydantic model for candidates."""

    surname: str
    firstname: str
    patronymic: str | None
    birthday: date
    editable: bool
    username: str
    total: int


class Prev(Share):
    """Previous schema."""

    surname: str = Field(validation_alias="lastNameBeforeChange", max_length=255)
    firstname: Annotated[
        str | None,
        Field(default=None, validation_alias="firstNameBeforeChange", max_length=255),
    ]
    patronymic: Annotated[
        str | None,
        Field(default=None, validation_alias="midNameBeforeChange", max_length=255),
    ]
    changed: Annotated[
        str | None,
        Field(default=None, validation_alias="yearOfChange", max_length=4),
    ]
    reason: str | None = None
    item: Literal["previous"] = "previous"


class Education(Share):
    """Educations schema."""

    view: Annotated[
        str | None,
        Field(default=None, validation_alias="educationType", max_length=255),
    ]
    institution: Annotated[str, Field(validation_alias="institutionName")]
    finished: Annotated[
        str | None,
        Field(default=None, validation_alias="endYear"),
        BeforeValidator(str),
    ]
    specialty: str | None = None
    item: Literal["educations"] = "educations"


class Staff(Share):
    """Staffs schema."""

    position: str
    department: str | None = None
    item: Literal["staffs"]


class Document(Share):
    """Documents schema."""

    view: Annotated[
        str | None,
        Field(default="Паспорт", validation_alias="documentType"),
    ]
    series: str | None = None
    digits: Annotated[str, Field(max_length=12)]
    agency: Annotated[
        str | None,
        Field(default=None, validation_alias="endYear", max_length=255),
    ]
    issue: date | None = None
    item: Literal["documents"]


class Address(Share):
    """Addresses schema."""

    view: Annotated[str, Field(max_length=255)]
    address: Annotated[str, Field(max_length=255)]
    item: Literal["addresses"]


class Contact(Share):
    """Contacts schema."""

    view: Annotated[str, Field(max_length=255)]
    contact: Annotated[str, Field(max_length=255)]
    item: Literal["contacts"]


class Workplace(Share):
    """Workplaces schema."""

    now_work: Annotated[
        bool | None,
        Field(default=False, validation_alias="currentJob"),
    ]
    starts: Annotated[date | None, Field(validation_alias="beginDate")]
    finished: Annotated[date | None, Field(default=None, validation_alias="endDate")]
    workplace: Annotated[str | None, Field(default=None, validation_alias="name")]
    address: Annotated[str | None, Field(None, max_length=255)]
    position: Annotated[str, Field(max_length=255)]
    reason: Annotated[str | None, Field(default=None, validation_alias="fireReason")]
    item: Literal["workplaces"] = "workplaces"


class Affilation(Share):
    """Affilations schema."""

    view: Annotated[
        str | None,
        Field(default=None, validation_alias="organizationType"),
    ]
    organization: Annotated[str, Field(validation_alias="name")]
    inn: str | None = None
    item: Literal["affilations"] = "affilations"


class Check(Share):
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


class Poligraf(Share):
    """Poligraf schema."""

    theme: str
    results: str
    conclusion: Decisions
    item: Literal["poligrafs"]


class Investigation(Share):
    """Investigations schema."""

    theme: str
    info: str
    item: Literal["investigations"]


class Inquiry(Share):
    """Inquiries schema."""

    info: str
    initiator: str
    item: Literal["inquiries"]


class AnketaJson(Person):
    """Candidate anketa schema."""

    email: Annotated[str | None, Field(pattern=email_pattern)]
    department: str | None = None
    position: Annotated[str, Field(validation_alias="positionName", max_length=255)]
    series: Annotated[
        str | None,
        Field(default=None, validation_alias="passportSerial"),
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
        str,
        Field(validation_alias="validAddress", max_length=255),
    ]
    reg_address: Annotated[str, Field(validation_alias="regAddress", max_length=255)]
    contact_phone: Annotated[
        str,
        Field(validation_alias="contactPhone", max_length=255),
    ]
    education: Annotated[list[Education], Field([])]
    experience: Annotated[list[Workplace], Field([])]
    organizations: Annotated[list[Affilation], Field([])]
    name_was_changed: Annotated[
        list[Prev],
        Field(
            default=[],
            validation_alias="nameWasChanged",
        ),
    ]
    related_organizations: Annotated[
        list[Affilation],
        Field(
            default=[],
            validation_alias="relatedPersonsOrganizations",
        ),
    ]
    state_organizations: Annotated[
        list[Affilation],
        Field(
            default=[],
            validation_alias="stateOrganizations",
        ),
    ]
    public_organizations: Annotated[
        list[Affilation],
        Field(
            default=[],
            validation_alias="publicOfficeOrganizations",
        ),
    ]


ItemModel = Annotated[
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
    | Workplace,
    Field(discriminator="item"),
]
