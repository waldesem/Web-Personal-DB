from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from ..models.model import (
    Person,
    Connect,
    Role,
    User,
    Previous,
    Staff,
    Document,
    Address,
    Contact,
    Education,
    Workplace,
    Relation,
    Affilation,
    Check,
    Robot,
    Poligraf,
    Investigation,
    Inquiry,
)


class LoginSchema(BaseModel):
    username: str
    password: str
    new_pswd: Optional[str] = None


class TokenSchema(BaseModel):
    access_token: str = Field(default="")
    refresh_token: str = Field(default="")


class UserWithRoles(BaseModel):
    user: User
    roles: list[Role]


class SchemaPersonsInput(BaseModel):
    surname: str | None
    firstname: str | None
    patronymic: str | None
    birthday: str | None


class SchemaPersons(BaseModel):
    persons: list[Person]
    has_next: bool


class SchemaConnections(BaseModel):
    contacts: list[Connect]
    has_next: bool
    names: list[str]
    companies: list[str]
    cities: list[str]


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


class Models(Enum):
    previous = Previous
    staff = Staff
    document = Document
    address = Address
    contact = Contact
    education = Education
    workplace = Workplace
    relation = Relation
    affilation = Affilation
    check = Check
    robot = Robot
    poligraf = Poligraf
    investigation = Investigation
    inquiry = Inquiry


"""Schemas for API endpoints"""


class NameWasChangedApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    firstNameBeforeChange: Optional[str]
    lastNameBeforeChange: Optional[str]
    midNameBeforeChange: Optional[str]
    yearOfChange: Optional[int]
    reason: Optional[str]


class EducationApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    educationType: str
    institutionName: Optional[str]
    endYear: Optional[int]
    specialty: Optional[str]


class ExperienceApi(BaseModel):
    """Nested schema for AnketaSchemaApi"""

    beginDate: Optional[int]
    endDate: Optional[int]
    currentJob: Optional[bool]
    name: Optional[str]
    address: Optional[str]
    position: Optional[str]
    fireReason: Optional[str]


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
