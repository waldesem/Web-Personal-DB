from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

"""Schemas for API endpoints"""


class NameWasChangedApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    firstNameBeforeChange: Optional[str] = None
    lastNameBeforeChange: Optional[str] = None
    midNameBeforeChange: Optional[str] = None
    yearOfChange: Optional[int] = None
    reason: Optional[str] = None


class EducationApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    educationType: Optional[str] = None
    institutionName: Optional[str] = None
    endYear: Optional[int] = None
    specialty: Optional[str] = None


class ExperienceApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    beginDate: Optional[date] = None
    endDate: Optional[date] = None
    currentJob: Optional[bool] = None
    name: Optional[str] = None
    address: Optional[str] = None
    position: Optional[str] = None
    fireReason: Optional[str] = None


class OrganizationsApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    name: Optional[str] = None
    position: Optional[str] = None
    inn: Optional[str] = None


class RelatedPersonsOrganizationsApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    name: Optional[str] = None
    position: Optional[str] = None
    inn: Optional[str] = None


class StateOrganizationsApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    name: Optional[str] = None
    position: Optional[str] = None


class PublicOfficeOrganizationsApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    name: Optional[str] = None
    position: Optional[str] = None


class AnketaSchemaApi(BaseModel):
    """Create schema for getting anketa"""

    positionName: Optional[str] = None
    department: Optional[str] = None
    surname: str = Field(alias="lastName", max_length=255)
    firstname: str = Field(alias="firstName", max_length=255)
    patronymic: Optional[str] = Field(alias="midName", max_length=255)
    birthday: date
    birthplace: Optional[str] = Field(alias="birthplace", default=None, max_length=255)
    citizen: Optional[str] = None
    additionalCitizenship: Optional[str] = None
    maritalStatus: Optional[str] = None
    regAddress: Optional[str] = None
    validAddress: Optional[str] = None
    contactPhone: Optional[str] = None
    email: Optional[str] = None
    inn: Optional[str] = None
    snils: Optional[str] = None
    passportSerial: Optional[str] = None
    passportNumber: str = None
    passportIssueDate: Optional[date] = None
    passportIssuedBy: Optional[str] = None
    nameWasChanged: Optional[list[NameWasChangedApi]] = None
    education: Optional[list[EducationApi]] = None
    experience: Optional[list[ExperienceApi]] = None
    organizations: Optional[list[OrganizationsApi]] = None
    relatedPersonsOrganizations: Optional[list[RelatedPersonsOrganizationsApi]] = None
    stateOrganizations: Optional[list[StateOrganizationsApi]] = None
    publicOfficeOrganizations: Optional[list[PublicOfficeOrganizationsApi]] = None
