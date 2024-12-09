from datetime import date
from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, validator

from .classes import Conclusions, Regions, Roles
from ..utils.utils import secure_filename


class Login(BaseModel):
    username: str
    password: str
    new_pswd: Optional[str]


class Search(BaseModel):
    search: Optional[str]


class Region(BaseModel):
    region: Regions

    class Config:
        use_enum_values = True


class Info(BaseModel):
    start: date
    end: date
    region: Optional[Regions]

    class Config:
        use_enum_values = True


class UserActions(BaseModel):
    item: Literal["drop", "block", "delete"] | Roles | Regions

    class Config:
        use_enum_values = True


class Model(BaseModel):
    id: Optional[str | int]

    class Config:
        use_enum_values = True


class User(Model):
    fullname: str
    username: str
    email: Optional[str]
    region: Optional[Regions]
    role: Optional[Roles]


class Person(Model):
    __modelname__ = "persons"
    surname: str
    firstname: str
    patronymic: Optional[str] = ""
    birthday: date
    birthplace: Optional[str] = ""
    citizenship: Optional[str] = ""
    dual: Optional[str] = ""
    snils: Optional[str] = ""
    inn: Optional[str] = ""
    marital: Optional[str] = ""
    addition: Optional[str] = ""
    destination: Optional[str] = ""
    region: Optional[Regions] = ""
    editable: Optional[bool] = False
    user_id: Optional[str | int]

    @validator("surname", "firstname", "patronymic")
    def check_names(cls, v):
        return v.upper().strip() if v else None


class Prev(Model):
    __modelname__ = "previous"

    surname: str
    firstname: str
    patronymic: Optional[str] = ""
    changed: Optional[str] = ""
    reason: Optional[str] = ""

    @validator("surname", "firstname", "patronymic")
    def check_names(cls, v):
        return v.upper().strip() if v else None


class Education(Model):
    __modelname__ = "educations"

    view: str
    institution: str
    finished: Union[str, int] = ""
    specialty: Optional[str] = ""


class Staff(Model):
    __modelname__ = "staffs"

    position: str
    department: Optional[str] = ""


class Document(Model):
    __modelname__ = "documents"

    view: str
    series: Optional[str] = ""
    digits: str
    agency: Optional[str] = ""
    issue: Optional[date]


class Address(Model):
    __modelname__ = "addresses"

    view: str
    addresses: str


class Contact(Model):
    __modelname__ = "contacts"

    view: str
    contact: str


class Workplace(Model):
    __modelname__ = "workplaces"

    now_work: Optional[bool] = False
    starts: Optional[date]
    finished: Optional[date]
    workplace: str
    addresses: Optional[str] = ""
    position: str
    reason: Optional[str] = ""


class Affilation(Model):
    __modelname__ = "affilations"

    view: str
    organization: str
    inn: Optional[str] = ""


class Relation(Model):
    __modelname__ = "relations"

    type: str
    right_id: Union[int, str]


class Check(Model):
    __modelname__ = "checks"

    workplace: Optional[str] = ""
    document: Optional[str] = ""
    inn: Optional[str] = ""
    debt: Optional[str] = ""
    bankruptcy: Optional[str] = ""
    bki: Optional[str] = ""
    courts: Optional[str] = ""
    affilation: Optional[str] = ""
    terrorist: Optional[str] = ""
    mvd: Optional[str] = ""
    internet: Optional[str] = ""
    cronos: Optional[str] = ""
    cros: Optional[str] = ""
    addition: Optional[str] = ""
    comment: Optional[str] = ""
    conclusion: Conclusions


class Poligraf(Model):
    __modelname__ = "poligrafs"

    theme: str
    results: str


class Investigation(Model):
    __modelname__ = "investigations"

    theme: str
    info: str


class Inquiry(Model):
    __modelname__ = "inquiries"

    info: str
    initiator: str
    origins: Optional[str] = ""


class NameWasChangedJson(BaseModel):
    firstNameBeforeChange: Optional[str] = ""
    lastNameBeforeChange: Optional[str] = ""
    midNameBeforeChange: Optional[str] = ""
    yearOfChange: Union[str, int] = ""
    reason: Optional[str] = ""


class EducationJson(BaseModel):
    educationType: Optional[str] = ""
    institutionName: Optional[str] = ""
    endYear: Union[str, int] = ""
    specialty: Optional[str] = ""


class ExperienceJson(BaseModel):
    beginDate: Optional[date]
    endDate: Optional[date]
    currentJob: Optional[bool] = False
    name: Optional[str] = ""
    address: Optional[str] = ""
    position: Optional[str] = ""
    fireReason: Optional[str] = ""


class OrganizationsJson(BaseModel):
    name: Optional[str] = ""
    inn: Optional[str] = ""


class RelatedPersonsOrganizationsJson(BaseModel):
    name: Optional[str] = ""
    inn: Optional[str] = ""


class StateOrganizationsJson(BaseModel):
    name: Optional[str] = ""


class PublicOfficeOrganizationsJson(BaseModel):
    name: Optional[str] = ""


class AnketaSchemaJson(BaseModel):
    lastName: str
    firstName: str
    midName: Optional[str] = ""
    birthday: date
    birthplace: Optional[str] = ""
    citizen: Optional[str] = ""
    additionalCitizenship: Optional[str] = ""
    maritalStatus: Optional[str] = ""
    inn: Optional[str] = ""
    snils: Optional[str] = ""
    positionName: Optional[str] = ""
    department: Optional[str] = ""
    passportSerial: Optional[str] = ""
    passportNumber: Optional[str] = ""
    passportIssueDate: Optional[date]
    passportIssuedBy: Optional[str] = ""
    validAddress: Optional[str] = ""
    regAddress: Optional[str] = ""
    email: Optional[str] = ""
    contactPhone: Optional[str] = ""
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


class File(BaseModel):
    file: Any
    filename: str

    @validator("filename")
    def check_filename(cls, name):
        return secure_filename(name)