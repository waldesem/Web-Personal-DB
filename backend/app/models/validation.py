from typing import List
from datetime import datetime

from pydantic import BaseModel, Field


class RegionModel(BaseModel):
    id: int
    region: str 
    users: str
    persons: List[int]
   
       
class GroupModel(BaseModel):
    id: int
    group: str
    connects: List[int]


class RoleModel(BaseModel):
    id: int
    role: str



class UserViewModel(BaseModel):
    id: int
    fullname: str
    username: str
    password: str
    email: str
    pswd_create: datetime
    pswd_change: datetime
    last_login: datetime
    blocked: bool
    attempt: int
    region_id: int
    group_id: List[int]
    role_id: List[int]

class ReportModel(BaseModel):
    id: int
    category: str
    title: str
    report: str
    status: str
    create: datetime
    user_id: int


class PersonModel(BaseModel):
    id: int
    category: str
    region_id: int
    fullname: str
    previous: str
    birthday: datetime
    birthplace: str
    country: str
    ext_country: str
    snils: str
    inn: str
    education: str
    marital: str
    addition: str
    path: str
    status: str
    create: datetime
    update: datetime
    request_id: int
    

class RelationModel(BaseModel):
    id: int
    relation: str
    relation_id: int
    person_id: int
    

class StaffModel(BaseModel):
    id: int
    position: str
    department: str
    person_id: int


class DocumentModel(BaseModel):
    id: int
    view: str
    series: str
    number: str
    agency: str
    issue: str
    person_id: int


class AddressModel(BaseModel):
    id: int
    view: str
    region: str
    address: str
    person_id: int


class WorkplaceModel(BaseModel):
    id: int
    start_date: datetime
    end_date: datetime
    now_work: bool
    workplace: str
    address: str
    position: str
    reason: str
    person_id: int


class ContactModel(BaseModel):
    id: int
    view: str
    contact: str
    person_id: int


class CheckModel(BaseModel):
    id: int
    workplace: str
    employee: str
    document: str
    inn: str
    debt: str
    bankruptcy: str
    bki: str
    courts: str
    affiliation: str
    terrorist: str
    mvd: str
    internet: str
    cronos: str
    cros: str
    addition: str
    path: str
    pfo: str
    comments: str
    conclusion: str
    officer: str
    deadline: datetime
    person_id: int


class RegistryModel(BaseModel):
    id: int
    comments: str
    decision: str
    supervisor: str
    deadline: datetime
    person_id: int
    check_id: int


class PoligrafModel(BaseModel):
    id: int
    theme: str
    results: str
    path: str
    officer: str
    deadline: datetime
    person_id: int


class InvestigationModel(BaseModel):
    id: int
    theme: str
    info: str
    path: str
    officer: str
    deadline: datetime
    person_id: int



class InquiryModel(BaseModel):
    id: int
    info: str
    initiator: str
    source: str
    officer: str
    deadline: datetime
    person_id: int


class ConnectModel(BaseModel):
    id: int
    company: str
    city: str
    fullname: str
    phone: str
    adding: str
    mobile: str
    mail: str
    comment: str
    data: datetime
    group_id: int


class OneSModel(BaseModel):
    id: int
    full_name: str
    birth_date: str
    start_date: datetime
    start_position: str
    end_date: datetime
    end_position: str
    person_id: int
