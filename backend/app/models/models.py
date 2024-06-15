from datetime import date, datetime, timezone
from typing import Optional, Union

from pydantic import BaseModel, Field, field_validator

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
    updated: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("updated")
    def check_updated(cls, v):
        return datetime.now(timezone.utc)


class User(QueryModel):
    fullname: str
    username: str
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    region: Regions
    has_admin: bool = False

    class Config:
        use_enum_values = True


class Name(QueryModel):
    surname: str
    firstname: str
    patronymic: Optional[str]

    @field_validator("surname", "firstname", "patronymic")
    def check_names(cls, v):
        if v:
            return v.upper().strip()


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
    region: Optional[Regions]

    class Config:
        use_enum_values = True


class Prev(Name):
    changed: Optional[str]
    reason: Optional[str]


class Education(QueryModel):
    view: Educations
    name: str
    finished: Optional[str]
    speciality: Optional[str]

    class Config:
        use_enum_values = True


class Staff(QueryModel):
    position: str
    department: str = "Прямое подчинение ПП"


class Document(QueryModel):
    view: Documents
    series: Optional[str]
    number: str
    agency: Optional[str]
    issued: Optional[date]

    class Config:
        use_enum_values = True


class Address(QueryModel):
    view: Addresses
    address: str

    class Config:
        use_enum_values = True


class Contact(QueryModel):
    view: Contacts
    contact: str

    class Config:
        use_enum_values = True


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

    class Config:
        use_enum_values = True


class Relation(QueryModel):
    relation: Relations
    relation_id: Union[int, str]

    class Config:
        use_enum_values = True


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

    class Config:
        use_enum_values = True


class Poligraf(QueryModel):
    theme: Poligrafs
    results: str

    class Config:
        use_enum_values = True


class Investigation(QueryModel):
    theme: str
    info: str

    class Config:
        use_enum_values = True
        

class Inquiry(QueryModel):
    info: str
    initiator: str


class Connects(QueryModel):
    view: Optional[str] = None
    company: Optional[str] = None
    city: Optional[str] = "Москва"
    fullname: Optional[str] = None
    phone: Optional[str] = None
    adding: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$", default=None)
    comment: Optional[str] = None

    @field_validator("company")
    def check_company(cls, v):
        if v:
            return v.upper().strip()


models_tables = {
    "staffs": Staff,
    "previous": Prev,
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
