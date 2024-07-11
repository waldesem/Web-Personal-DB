from datetime import date
from typing import Optional, Union

from pydantic import BaseModel, validator

from ..classes.classes import (
    Addresses,
    Affiliates,
    Contacts,
    Documents,
    Educations,
    Poligrafs,
    Regions,
    Conclusions,
    Relations,
)


class QueryModel(BaseModel):
    id: Optional[str | int] = None

    class Config:
        use_enum_values = True


class User(QueryModel):
    fullname: str
    username: str
    region: Regions
    has_admin: bool = False


class Name(QueryModel):
    surname: str
    firstname: str
    patronymic: Optional[str] = None

    @validator("surname", "firstname", "patronymic")
    def check_names(cls, v):
        return v.upper().strip() if v else None


class Person(Name):
    birthday: date
    birthplace: Optional[str] = "Москва"
    citizenship: str = "Россия"
    dual: Optional[str] = None
    snils: Optional[int] = None
    inn: Optional[int] = None
    marital: Optional[str] = None
    addition: Optional[str] = None
    destination: Optional[str] = None
    region: Optional[Regions] = None


class Prev(Name):
    changed: Optional[str] = None
    reason: Optional[str] = None


class Education(QueryModel):
    view: Educations
    institution: str
    finished: Optional[str] = None
    speciality: Optional[str] = None


class Staff(QueryModel):
    position: str
    department: str = "Прямое подчинение ПП"


class Document(QueryModel):
    view: Documents
    series: Optional[str] = None
    digits: str
    agency: Optional[str] = None
    issue: Optional[date] = None


class Address(QueryModel):
    view: Addresses
    addresses: str


class Contact(QueryModel):
    view: Contacts
    contact: str


class Workplace(QueryModel):
    now_work: Optional[bool] = False
    starts: date
    finished: Optional[date] = None
    workplace: str
    addresses: Optional[str] = None
    position: str
    reason: Optional[str] = None


class Affilation(QueryModel):
    view: Affiliates
    organization: str
    inn: Optional[str] = None
    position: str


class Relation(QueryModel):
    relation: Relations
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
    theme: Poligrafs
    results: str


class Investigation(QueryModel):
    theme: str
    info: str


class Inquiry(QueryModel):
    info: str
    origins: str


models_tables = {
    "previous": Prev,
    "staffs": Staff,
    "documents": Document,
    "addresses": Address,
    "contacts": Contact,
    "educations": Education,
    "workplaces": Workplace,
    "affilations": Affilation,
    "relations": Relation,
    "checks": Check,
    "investigations": Investigation,
    "poligrafs": Poligraf,
    "inquiries": Inquiry,
}
