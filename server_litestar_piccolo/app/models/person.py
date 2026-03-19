"""PyDantic models."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime  # noqa: TC003
from typing import Annotated, TypedDict

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    PastDate,
    field_validator,
)

try:
    from check_sum import validate_inn, validate_snils  # ty:ignore[unresolved-import]

except ImportError:
    from app.utilities.utils import validate_inn, validate_snils


class Index(BaseModel):
    """Schema for query params."""

    page: int
    per_page: int
    search: Annotated[
        str | None,
        Field(None, max_length=255),
        AfterValidator(lambda v: v.upper().split(maxsplit=3)[:3] if v else None),
    ]


class Candidates(TypedDict):
    """Typed Dict for candidates."""

    id: int
    surname: str
    firstname: str
    patronymic: str | None
    birthday: date
    editable: bool
    updated_at: datetime
    username: str
    total: int


@dataclass(frozen=True)
class Person:
    """Person schema."""

    id: int
    surname: str
    firstname: str
    patronymic: str | None
    birthday: date
    birthplace: str | None
    citizenship: str | None
    dual: str | None
    snils: str | None
    inn: str | None
    marital: str | None
    addition: str | None
    destination: str
    editable: bool
    protected: bool
    deleted: bool
    user_id: int
    created_at: datetime
    updated_at: datetime


class PersonForm(BaseModel):
    """Person schema."""

    model_config = ConfigDict(str_strip_whitespace=True)

    surname: Annotated[str, Field(max_length=255)]
    firstname: Annotated[str, Field(max_length=255)]
    patronymic: Annotated[str | None, Field(default=None, max_length=255)]
    birthday: PastDate
    birthplace: Annotated[str | None, Field(None, max_length=255)]
    citizenship: Annotated[str | None, Field(default=None, max_length=255)]
    dual: Annotated[str | None, Field(default=None, max_length=255)]
    snils: str | None = None
    inn: str | None = None
    marital: Annotated[str | None, Field(default=None, max_length=255)]
    addition: str | None = None

    @field_validator("surname", "firstname", "patronymic")
    @classmethod
    def normalize_name(cls, v: str | None) -> str | None:
        """Normalize name."""
        return v.upper() if v and re.match(r"^[А-яЁёIV\-\s\.\,\'\(\)]*$", v) else None

    @field_validator("inn", mode="after")
    @classmethod
    def check_inn(cls, inn: str | None) -> str | None:
        """Check inn."""
        return validate_inn(inn)

    @field_validator("snils", mode="after")
    @classmethod
    def check_snils(cls, snils: str | None) -> str | None:
        """Check snils."""
        return validate_snils(snils)


@dataclass
class PersonResponse:
    """Person exists response."""

    person_id: int
