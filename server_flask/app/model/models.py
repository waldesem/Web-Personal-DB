from datetime import date
from typing import Optional, Union

from pydantic import BaseModel, validator

from .classes import Regions, Conclusions, Roles


class Login(BaseModel):
    username: str
    password: str
    new_pswd: Optional[str]


class MainModel(BaseModel):
    id: Optional[str | int]

    class Config:
        use_enum_values = True


class User(MainModel):
    fullname: str
    username: str
    email: Optional[str]
    region: Optional[Regions]
    role: Optional[Roles]


class Person(MainModel):
    __tablename__ = "persons"

    surname: str
    firstname: str
    patronymic: Optional[str]
    birthday: date
    birthplace: Optional[str]
    citizenship: Optional[str]
    dual: Optional[str]
    snils: Optional[str]
    inn: Optional[str]
    marital: Optional[str]
    addition: Optional[str]
    destination: Optional[str]
    region: Optional[Regions]
    editable: Optional[bool] = False
    user_id: Optional[str | int]

    @validator("surname", "firstname", "patronymic")
    def check_names(cls, v):
        return v.upper().strip() if v else None


class Prev(MainModel):
    __tablename__ = "previous"

    surname: Optional[str]
    firstname: Optional[str]
    patronymic: Optional[str]
    changed: Optional[str]
    reason: Optional[str]

    @validator("surname", "firstname", "patronymic")
    def check_names(cls, v):
        return v.upper().strip() if v else None


class Education(MainModel):
    __tablename__ = "educations"
    
    view: Optional[str]
    institution: Optional[str]
    finished: Union[str, int]
    specialty: Optional[str]


class Staff(MainModel):
    __tablename__ = "staffs"

    position: str
    department: str = "Прямое подчинение"


class Document(MainModel):
    __tablename__ = "documents"

    view: Optional[str]
    series: Optional[str]
    digits: Optional[str]
    agency: Optional[str]
    issue: Optional[date]


class Address(MainModel):
    __tablename__ = "addresses"

    view: Optional[str]
    addresses: Optional[str]


class Contact(MainModel):
    __tablename__ = "contacts"

    view: Optional[str]
    contact: Optional[str]


class Workplace(MainModel):
    __tablename__ = "workplaces"

    now_work: Optional[bool] = False
    starts: Optional[date]
    finished: Optional[date]
    workplace: Optional[str]
    addresses: Optional[str]
    position: Optional[str]
    reason: Optional[str]


class Affilation(MainModel):
    __tablename__ = "affilations"
    
    view: Optional[str]
    organization: str
    inn: Optional[str]


class Relation(MainModel):
    __tablename__ = "relations"

    type: str
    right_id: Union[int, str]


class Check(MainModel):
    __tablename__ = "checks"

    workplace: Optional[str]
    document: Optional[str]
    inn: Optional[str]
    debt: Optional[str]
    bankruptcy: Optional[str]
    bki: Optional[str]
    courts: Optional[str]
    affilation: Optional[str]
    terrorist: Optional[str]
    mvd: Optional[str]
    internet: Optional[str]
    cronos: Optional[str]
    cros: Optional[str]
    addition: Optional[str]
    comment: Optional[str]
    conclusion: Conclusions


class Poligraf(MainModel):
    __tablename__ = "poligrafs"

    theme: str
    results: str


class Investigation(MainModel):
    __tablename__ = "investigations"

    theme: str
    info: str


class Inquiry(MainModel):
    __tablename__ = "inquiries"

    info: str
    initiator: str
    origins: Optional[str]


models_tables = {
    cls.__tablename__: cls
    for cls in MainModel.__subclasses__()
    if hasattr(cls, "__tablename__")
}


class NameWasChangedJson(BaseModel):
    firstNameBeforeChange: Optional[str]
    lastNameBeforeChange: Optional[str]
    midNameBeforeChange: Optional[str]
    yearOfChange: Union[str, int]
    reason: Optional[str]


class EducationJson(BaseModel):
    educationType: Optional[str]
    institutionName: Optional[str]
    endYear: Union[str, int]
    specialty: Optional[str]


class ExperienceJson(BaseModel):
    beginDate: Optional[date]
    endDate: Optional[date]
    currentJob: Optional[bool]
    name: Optional[str]
    address: Optional[str]
    position: Optional[str]
    fireReason: Optional[str]


class OrganizationsJson(BaseModel):
    name: Optional[str]
    inn: Optional[str]


class RelatedPersonsOrganizationsJson(BaseModel):
    name: Optional[str]
    inn: Optional[str]


class StateOrganizationsJson(BaseModel):
    name: Optional[str]


class PublicOfficeOrganizationsJson(BaseModel):
    name: Optional[str]


class AnketaSchemaJson(BaseModel):
    lastName: str
    firstName: str
    midName: Optional[str]
    birthday: date
    birthplace: Optional[str]
    citizen: Optional[str]
    additionalCitizenship: Optional[str]
    maritalStatus: Optional[str]
    inn: Optional[str]
    snils: Optional[str]
    positionName: Optional[str]
    department: Optional[str]
    passportSerial: Optional[str]
    passportNumber: Optional[str]
    passportIssueDate: Optional[date]
    passportIssuedBy: Optional[str]
    validAddress: Optional[str]
    regAddress: Optional[str]
    email: Optional[str]
    contactPhone: Optional[str]
    education: Optional[list[EducationJson]] = []
    experience: Optional[list[ExperienceJson]] = []
    nameWasChanged: Optional[list[NameWasChangedJson]] = []
    organizations: Optional[list[OrganizationsJson]] = []
    relatedPersonsOrganizations: Optional[list[RelatedPersonsOrganizationsJson]] = []
    stateOrganizations: Optional[list[StateOrganizationsJson]] = []
    publicOfficeOrganizations: Optional[list[PublicOfficeOrganizationsJson]] = []

    @validator("lastName", "firstName", "midName")
    def check_names(cls, v):
        return v.upper().strip() if v else None
