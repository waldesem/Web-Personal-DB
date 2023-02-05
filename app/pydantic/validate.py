from pydantic import BaseModel, ValidationError


class ValidateCandidate(BaseModel):  # модель анкетных данных
    """ Create model for candidates dates"""

    region: str
    full_name: str
    last_name: str
    birthday: str
    birth_place: str
    country: str
    series_passport: str
    number_passport: str
    agency: str
    date_given: str
    snils: str
    inn: str
    reg_address: str
    live_address: str
    phone: str
    email: str
    education: str
    workplace_1: str
    workplace_2: str
    workplace_3: str
    addition: str
    update_date: str
    status: str
    request_id: str


class ValidateCheck(BaseModel):  # модель данных проверки кандидатов
    """ Create model for candidates checks"""

    staff: str
    department: str
    check_work_place: str
    check_passport: str
    check_debt: str
    check_bankruptcy: str
    check_bki: str
    check_affiliation: str
    check_terrorist: str
    check_mvd: str
    check_internet: str
    check_cronos: str
    check_cross: str
    check_addition: str
    pfo: str
    comment: str
    resume: str
    date_check: str
    officer: str
    url: str
    check_id: str


def validate_resume(data):
    try:
        valid = ValidateCandidate(**data)
    except ValidationError as e:
        valid = e
    return valid
    

def validate_check(data):
    try:
        valid = ValidateCheck(**data)
    except ValidationError as e:
        valid = e    
    return valid
