"""PyDantic models."""

from __future__ import annotations

import re
from datetime import date, datetime  # noqa: TC003
from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    PastDate,
    SkipValidation,
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


class PersonIn(BaseModel):
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
    destination: str | None = None
    editable: bool | None = True

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


class PersonOut(PersonIn):
    """Person schema."""

    id: int
    addition: str | None = None
    destination: str | None = None
    editable: bool
    protected: bool | None
    user_id: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def normalize_name(cls, v: str | None) -> str | None:
        """Normalize name."""
        return v

    @classmethod
    def check_inn(cls, inn: str | None) -> str | None:
        """Check inn."""
        return inn

    @classmethod
    def check_snils(cls, snils: str | None) -> str | None:
        """Check snils."""
        return snils


class PersonResponse(BaseModel):
    """Person exists response."""

    person_id: int


class Candidates(BaseModel):
    """Pydantic model for candidates."""

    id: Annotated[int, SkipValidation]
    surname: Annotated[str, SkipValidation]
    firstname: Annotated[str, SkipValidation]
    patronymic: Annotated[str | None, SkipValidation]
    birthday: Annotated[date, SkipValidation]
    editable: Annotated[bool, SkipValidation]
    updated_at: Annotated[datetime, SkipValidation]
    username: Annotated[str, SkipValidation]
    total: Annotated[int, SkipValidation]
