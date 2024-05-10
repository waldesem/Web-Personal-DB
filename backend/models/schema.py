from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from ..models.model import Person, Connect


class LoginSchema(BaseModel):

    username: str
    password: str
    new_pswd: Optional[str] = None


class TokenSchema(BaseModel):

    message: str
    access_token: str = Field(default="")
    refresh_token: str = Field(default="")


class SchemaPersons(BaseModel):
    persons: list[Person]
    has_next: bool
    has_prev: bool


class SchemaConnections(BaseModel):
    connects: list[Connect]
    has_next: bool
    has_prev: bool
    names: list[dict]
    companies: list[dict]
    cities: list[dict]


class SchemaGptInput(BaseModel):
    query: str


class SchemaGptOutput(BaseModel):
    answer: str


class ResumeSchemaApi(BaseModel):

    id: int
    surname: str
    firstname: str
    patronymic: str
    birthday: date
    birthplace: str
    snils: str
    inn: str
    series: str
    number: str
    agency: str
    issue: date
    address: str


class RobotSchema(BaseModel):
    path: str


"""Schemas for API endpoints"""

class NameWasChangedApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    surname: Optional[str] = Field(alias="firstNameBeforeChange")
    firstname: Optional[str] = Field(alias="lastNameBeforeChange")
    patronymic: Optional[str] = Field(alias="midNameBeforeChange")
    date_change: Optional[int] = Field(alias="yearOfChange")
    reason: Optional[str]


class EducationApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    view: str = Field(alias="educationType")
    name: Optional[str] = Field(alias="institutionName")
    end: Optional[int] = Field(alias="endYear")
    specialty: Optional[str]


class ExperienceApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    start_date: Optional[int] = Field(alias="beginDate")
    end_date: Optional[int] = Field(alias="endDate")
    now_work: Optional[bool] = Field(alias="currentJob")
    workplace: Optional[str] = Field(alias="name")
    address: Optional[str]
    position: Optional[str]
    reason: Optional[str] = Field(alias="fireReason")


class OrganizationsApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    name: str
    position: str
    inn: str = Field(max_length=10)


class RelatedPersonsOrganizationsApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    name: str
    position: str
    inn: str = Field(max_length=10)


class StateOrganizationsApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    name: str
    position: str


class PublicOfficeOrganizationsApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    name: str = Field(max_length=255)
    position: str = Field(max_length=255)


class AnketaSchemaApi(BaseModel):
    """Create schema for getting anketa"""

    positionName: str
    department: Optional[str]
    lastName: str = Field(max_length=255)
    firstName: str = Field(max_length=255)
    midName: Optional[str] = Field(max_length=255)
    birthday: str
    birthplace: str = Field(max_length=255)
    citizen: str = Field(max_length=255)
    additionalCitizenship: Optional[str] = Field(max_length=255)
    maritalStatus: Optional[str]
    regAddress: Optional[str]
    validAddress: str
    contactPhone: str
    email: Optional[EmailStr] 
    inn: str = Field(max_length=12)
    snils: str = Field(max_length=11)
    passportSerial: str = Field(max_length=4)
    passportNumber: str = Field(max_length=6)
    passportIssueDate: str
    passportIssuedBy: str = Field(max_length=255)
    nameWasChanged: Optional[list[NameWasChangedApi]]
    education: Optional[list[EducationApi]]
    experience: Optional[list[ExperienceApi]]
    organizations: Optional[list[OrganizationsApi]]
    relatedPersonsOrganizations: Optional[list[RelatedPersonsOrganizationsApi]]
    stateOrganizations: Optional[list[StateOrganizationsApi]]
    publicOfficeOrganizations: Optional[list[PublicOfficeOrganizationsApi]]
