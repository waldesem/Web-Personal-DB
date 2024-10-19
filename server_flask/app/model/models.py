from datetime import date
from typing import Optional, Union

from pydantic import BaseModel, validator

from .classes import Regions, Conclusions, Roles


class Login(BaseModel):
    username: str
    password: str
    new_pswd: Optional[str] = None


class QueryModel(BaseModel):
    id: Optional[str | int] = None

    class Config:
        use_enum_values = True


class User(QueryModel):
    fullname: str
    username: str
    email: Optional[str] = None
    region: Optional[Regions] = None
    role: Optional[Roles] = None


class Name(QueryModel):
    surname: str
    firstname: str
    patronymic: Optional[str] = None

    @validator("surname", "firstname", "patronymic")
    def check_names(cls, v):
        return v.upper().strip() if v else None


class Person(Name):
    birthday: date
    birthplace: Optional[str] = None
    citizenship: Optional[str] = None
    dual: Optional[str] = None
    snils: Optional[str] = None
    inn: Optional[str] = None
    marital: Optional[str] = None
    addition: Optional[str] = None
    destination: Optional[str] = None
    region: Optional[Regions] = None
    editable: Optional[bool] = False


class Prev(Name):
    changed: Optional[str] = None
    reason: Optional[str] = None


class Education(QueryModel):
    view: str
    institution: str
    finished: Union[str, int] = None
    specialty: Optional[str] = None


class Staff(QueryModel):
    position: str
    department: str = "Прямое подчинение"


class Document(QueryModel):
    view: str
    series: Optional[str] = None
    digits: str
    agency: Optional[str] = None
    issue: Optional[date] = None


class Address(QueryModel):
    view: str
    addresses: str


class Contact(QueryModel):
    view: str
    contact: str


class Workplace(QueryModel):
    now_work: Optional[bool] = False
    starts: date
    finished: Optional[date] = None
    workplace: str
    addresses: Optional[str] = None
    position: Optional[str] = None
    reason: Optional[str] = None


class Affilation(QueryModel):
    view: str
    organization: str
    inn: Optional[str] = None


class Relation(QueryModel):
    relation: str
    relation_id: Union[int, str]


class Check(QueryModel):
    workplace: Optional[str] = None
    document: Optional[str] = None
    inn: Optional[str] = None
    debt: Optional[str] = None
    bankruptcy: Optional[str] = None
    bki: Optional[str] = None
    courts: Optional[str] = None
    affilation: Optional[str] = None
    terrorist: Optional[str] = None
    mvd: Optional[str] = None
    internet: Optional[str] = None
    cronos: Optional[str] = None
    cros: Optional[str] = None
    addition: Optional[str] = None
    comment: Optional[str] = None
    conclusion: Optional[Conclusions] = None


class Poligraf(QueryModel):
    theme: str
    results: str


class Investigation(QueryModel):
    theme: str
    info: str


class Inquiry(QueryModel):
    info: str
    initiator: str
    origins: Optional[str] = None


models_tables = {
    "persons": Person,
    "previous": Prev,
    "educations": Education,
    "staffs": Staff,
    "documents": Document,
    "addresses": Address,
    "contacts": Contact,
    "relations": Relation,
    "workplaces": Workplace,
    "affilations": Affilation,
    "checks": Check,
    "poligrafs": Poligraf,
    "investigations": Investigation,
    "inquiries": Inquiry,
}


class NameWasChangedJson(BaseModel):
    firstNameBeforeChange: Optional[str] = None
    lastNameBeforeChange: Optional[str] = None
    midNameBeforeChange: Optional[str] = None
    yearOfChange: Union[str, int] = None
    reason: Optional[str] = None


class EducationJson(BaseModel):
    educationType: Optional[str] = None
    institutionName: Optional[str] = None
    endYear: Union[str, int] = None
    specialty: Optional[str] = None


class ExperienceJson(BaseModel):
    beginDate: Optional[date] = None
    endDate: Optional[date] = None
    currentJob: Optional[bool] = None
    name: Optional[str] = None
    address: Optional[str] = None
    position: Optional[str] = None
    fireReason: Optional[str] = None


class OrganizationsJson(BaseModel):
    name: Optional[str] = None
    inn: Optional[str] = None


class RelatedPersonsOrganizationsJson(BaseModel):
    name: Optional[str] = None
    inn: Optional[str] = None


class StateOrganizationsJson(BaseModel):
    name: Optional[str] = None


class PublicOfficeOrganizationsJson(BaseModel):
    name: Optional[str] = None


class AnketaSchemaJson(BaseModel):
    lastName: str
    firstName: str
    midName: Optional[str] = None
    birthday: date
    birthplace: Optional[str] = None
    citizen: Optional[str] = None
    additionalCitizenship: Optional[str] = None
    maritalStatus: Optional[str] = None
    inn: Optional[str] = None
    snils: Optional[str] = None
    positionName: Optional[str] = None
    department: Optional[str] = None
    passportSerial: Optional[str] = None
    passportNumber: Optional[str] = None
    passportIssueDate: Optional[date] = None
    passportIssuedBy: Optional[str] = None
    validAddress: Optional[str] = None
    regAddress: Optional[str] = None
    email: Optional[str] = None
    contactPhone: Optional[str] = None
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
