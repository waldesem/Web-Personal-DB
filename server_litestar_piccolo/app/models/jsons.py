"""PyDantic models."""

from __future__ import annotations

from datetime import date  # noqa: TC003
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr, Field


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

    model_config = ConfigDict(str_strip_whitespace=True)

    now_work: Annotated[bool, Field(default=False, validation_alias="currentJob")]
    starts: Annotated[date, Field(validation_alias="beginDate")]
    finished: Annotated[date | None, Field(default=None, validation_alias="endDate")]
    workplace: Annotated[str, Field(validation_alias="name", max_length=255)]
    address: Annotated[str | None, Field(None, max_length=255)]
    position: Annotated[str, Field(max_length=255)]
    reason: Annotated[str | None, Field(default=None, validation_alias="fireReason")]


class AffilationJson(BaseModel):
    """Affilation json model."""

    model_config = ConfigDict(str_strip_whitespace=True)

    view: Annotated[
        str | None,
        Field(default=None, validation_alias="organizationType", max_length=255),
    ]
    organization: Annotated[str, Field(validation_alias="name", max_length=255)]
    inn: Annotated[str | None, Field(None, max_length=12)]


class AnketaJson(BaseModel):
    """Candidate anketa schema."""

    surname: Annotated[str, Field(validation_alias="lastName")]
    firstname: Annotated[str, Field(validation_alias="firstName")]
    patronymic: Annotated[
        str | None,
        Field(default=None, validation_alias="midName"),
    ]
    birthday: date
    birthplace: str | None = None
    citizenship: Annotated[
        str | None,
        Field(default=None, validation_alias="citizen"),
    ]
    dual: Annotated[
        str | None,
        Field(default=None, validation_alias="additionalCitizenship"),
    ]
    snils: str | None = None
    inn: str | None = None
    marital: Annotated[
        str | None,
        Field(default=None, validation_alias="maritalStatus"),
    ]
    email: EmailStr | None = None
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
