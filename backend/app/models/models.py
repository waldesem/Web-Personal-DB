from datetime import date, datetime, timezone
from typing import Optional, Union

from pydantic import BaseModel, Field, validator

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

    @validator("updated")
    def check_updated(cls, _):
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
    patronymic: Optional[str] = None

    @validator("surname", "firstname", "patronymic")
    def check_names(cls, v):
        if v:
            return v.upper().strip()


class Person(Name):
    birthday: date
    birthplace: Optional[str] = "Москва"
    citizenship: str = "Россия"
    dual: Optional[str] = None
    snils: Optional[int] = None
    inn: Optional[int] = None
    marital: Optional[str] = None
    addition: Optional[str] = None
    path: Optional[str] = None
    region: Optional[Regions] = None

    class Config:
        use_enum_values = True


class Prev(Name):
    changed: Optional[str] = None
    reason: Optional[str] = None


class Education(QueryModel):
    view: Educations
    name: str
    finished: Optional[str] = None
    speciality: Optional[str] = None

    class Config:
        use_enum_values = True


class Staff(QueryModel):
    position: str
    department: str = "Прямое подчинение ПП"


class Document(QueryModel):
    view: Documents
    series: Optional[str] = None
    number: str
    agency: Optional[str] = None
    issued: Optional[date] = None

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
    now_work: Optional[bool] = False
    started: date
    finished: Optional[date] = None
    workplace: str
    address: Optional[str] = None
    position: str
    reason: Optional[str] = None


class Affilation(QueryModel):
    view: Affiliates
    name: str
    inn: Optional[str] = None
    position: str

    class Config:
        use_enum_values = True


class Relation(QueryModel):
    relation: Relations
    relation_id: Union[int, str]

    class Config:
        use_enum_values = True


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
    pfo: Optional[bool] = False
    comment: Optional[str] = None
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

    @validator("company")
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
