from datetime import date, datetime
from typing import Optional, Union

from pydantic import BaseModel, Field

from ..tools.classes import Addresses, Affiliates, Contacts, Documents, Educations, Poligrafs, Regions, Conclusions, Relations 

class QueryModel(BaseModel):
    updated: datetime = Field(default_factory=lambda: datetime.now())


class User(QueryModel):
    fullname: str
    username: str
    email: str = Field(regex="[a-zA-z_0-9\.]+@[a-zA-z]+\.[a-zA-z]+")
    region: Regions = Regions.main.name 
    has_admin: bool = False


class Name(QueryModel):
    surname: str
    firstname: str
    patronymic: Optional[str]


class Person(Name):
    birthday: date
    birthplace: Optional[str]
    citizenship: str = "Россия"
    dual: Optional[str]
    snils: Optional[int]
    inn: Optional[int]
    marital: Optional[str]
    addition: Optional[str]
    path: Optional[str]
    region: Regions = Regions.main.name  
        

class Previous(Name):
    changed: Optional[str]
    reason: Optional[str]


class Education(QueryModel):
    view: Educations
    name: str
    finished: Optional[str]
    speciality: Optional[str]


class Staff(QueryModel):
    position: str
    department: str = "Прямое подчинение ПП"


class Document(QueryModel):
    view: Documents
    series: Optional[str]
    number: str
    agency: Optional[str]
    issued: Optional[date]


class Address(QueryModel):
    view: Addresses
    address: str


class Contact(QueryModel):
    view: Contacts
    contact: str


class Workplace(QueryModel):
    now_work: bool = False
    started: date
    finished: Optional[date]
    workplace: str
    address: Optional[str]
    position: str
    reason: Optional[str]


class Affilation(QueryModel):
    view: Affiliates
    name: str
    inn: Optional[str]
    position: str


class Relation(QueryModel):
    relation: Relations
    relation_id: Union[int, str]


class Check(QueryModel):
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
    pfo: bool = False
    comment: Optional[str]
    conclusion: Conclusions


class Poligraf(QueryModel):
    theme: Poligrafs
    results: str


class Investigation(QueryModel):
    theme: str
    info: str


class Inquiry(QueryModel):
    info: str
    initiator: str


class Connects(QueryModel):
    view: Optional[str]
    company: str
    city: Optional[str]
    fullname: Optional[str]
    phone: Optional[str]
    adding: Optional[str]
    mobile: Optional[str]
    email: Optional[str] = Field(regex="[a-zA-z_0-9]+@[a-zA-z]+\.[a-zA-z]+")
    comment: Optional[str]


models_tables = {
    "staffs": Staff,
    "previous": Previous,
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
