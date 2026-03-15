"""PyDantic models."""

from __future__ import annotations

from datetime import date, datetime  # noqa: TC003
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
)

from app.classes.classes import Conclusions, Decisions


class IdModel(BaseModel):
    """ItemModel schema."""

    id: int


class DateIdModel(IdModel):
    """DateIdModel schema."""

    created_at: datetime
    updated_at: datetime


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
        BeforeValidator(lambda v: None if isinstance(v, str) else v),
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
