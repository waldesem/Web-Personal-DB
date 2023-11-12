from typing import List
from datetime import datetime

from pydantic import BaseModel, EmailStr, SecretStr


class ModelBase(BaseModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dump_model(self, instance):
        dummped = instance.__dict__
        del dummped['_sa_instance_state']
        return self.model_dump(**dummped)
    
    def validate_data(self, data):
        validated = self.model_validate(**data)
        return validated.model_dump(**data)


class RegionModel(ModelBase):
    id: int
    region: str 
    users: str
    persons: List[int]
   
       
class GroupModel(ModelBase):
    id: int
    group: str


class RoleModel(ModelBase):
    id: int
    role: str


class UserViewModel(ModelBase):
    id: int
    fullname: str
    username: str
    password: SecretStr
    email: EmailStr
    pswd_create: datetime
    pswd_change: datetime
    last_login: datetime
    blocked: bool
    attempt: int
    region_id: int
    group_id: List[str]
    role_id: List[str]


class ReportModel(ModelBase):
    id: int
    category: str
    title: str
    report: str
    status: str
    create: datetime
    user_id: int


class PersonModel(ModelBase):
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
    

class RelationModel(ModelBase):
    id: int
    relation: str
    relation_id: int
    person_id: int
    

class StaffModel(ModelBase):
    id: int
    position: str
    department: str
    person_id: int


class DocumentModel(ModelBase):
    id: int
    view: str
    series: str
    number: str
    agency: str
    issue: datetime
    person_id: int


class AddressModel(ModelBase):
    id: int
    view: str
    region: str
    address: str
    person_id: int


class WorkplaceModel(ModelBase):
    id: int
    start_date: datetime
    end_date: datetime
    workplace: str
    address: str
    position: str
    reason: str
    person_id: int


class ContactModel(ModelBase):
    id: int
    view: str
    contact: str
    person_id: int


class CheckModel(ModelBase):
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
    pfo: bool
    comments: str
    conclusion: str
    officer: str
    deadline: datetime
    person_id: int


class RegistryModel(ModelBase):
    id: int
    comments: str
    decision: str
    supervisor: str
    deadline: datetime
    person_id: int
    check_id: int


class PoligrafModel(ModelBase):
    id: int
    theme: str
    results: str
    path: str
    officer: str
    deadline: datetime
    person_id: int


class InvestigationModel(ModelBase):
    id: int
    theme: str
    info: str
    path: str
    officer: str
    deadline: datetime
    person_id: int


class InquiryModel(ModelBase):
    id: int
    info: str
    initiator: str
    source: str
    officer: str
    deadline: datetime
    person_id: int


class ConnectModel(ModelBase):
    id: int
    company: str
    city: str
    fullname: str
    phone: str
    adding: str
    mobile: str
    mail: EmailStr
    comment: str
    data: datetime
    group_id: int


class OneSModel(ModelBase):
    id: int
    full_name: str
    birth_date: datetime
    start_date: datetime
    end_date: datetime
    start_position: str
    end_position: str
    person_id: int
