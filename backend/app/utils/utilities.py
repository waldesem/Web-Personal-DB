import os
import json
from datetime import datetime

from flask import current_app
from ..models.model import db, Person
from ..models.classes import Status


class JsonFile:
    """ Create class for import data from json file"""

    def __init__(self, file) -> None:
        with open(file, 'r', newline='', encoding='utf-8-sig') as f:
            self.json_dict = json.load(f)

            self.resume = {
                'fullname': self.parse_fullname(),
                'previous': self.parse_previous(),
                'birthday': self.parse_birthday(),
                'birthplace': self.json_dict['birthplace'].strip() \
                    if 'birthplace' in self.json_dict else 'Отсутствует',
                'country': self.json_dict['citizen'].strip() \
                    if 'citizen' in self.json_dict else 'Отсутствует',
                'ext_country': self.json_dict['additionalCitizenship'] \
                    if 'additionalCitizenship' in self.json_dict else '',
                'snils': self.json_dict['snils'].strip() \
                    if 'snils' in self.json_dict else 'Отсутствует',
                'inn': self.json_dict['inn'].strip() \
                    if 'inn' in self.json_dict else 'Отсутствует',
                'marital': self.json_dict['maritalStatus'].strip() \
                    if 'maritalStatus' in self.json_dict else 'Отсутствует',
                'education': self.parse_education()
            }
            
            self.workplaces = self.parse_workplace()
            
            self.passport = [
                {
                    'view': 'Паспорт',
                    'series': self.json_dict['passportSerial'].strip() \
                        if 'passportSerial' in self.json_dict else 'Отсутствует',
                    'number': self.json_dict['passportNumber'].strip() \
                        if 'passportNumber' in self.json_dict else 'Отсутствует',
                    'issue': datetime.strptime(self.json_dict['passportIssueDate'], '%Y-%m-%d') \
                        if 'passportIssueDate' in self.json_dict \
                            else datetime.strptime('1900-01-01', '%Y-%m-%d'),
                    'agency': self.json_dict['passportIssuedBy'].strip() \
                        if 'passportIssuedBy' in self.json_dict else 'Отсутствует',
                }
            ]
            self.addresses = [
                {
                    'view': "Адрес регистрации", 
                    'address': self.json_dict['regAddress'].strip() \
                        if 'regAddress' in self.json_dict else 'Отсутствует',
                },
                {
                    'view': "Адрес проживания", 
                    'address': self.json_dict['validAddress'].strip() \
                        if 'validAddress' in self.json_dict else 'Отсутствует',
                }
            ]
            self.contacts = [
                {
                    'view': 'Мобильный телефон', 
                    'contact': self.json_dict['contactPhone'].strip() \
                        if 'contactPhone' in self.json_dict else 'Отсутствует',
                },
                {
                    'view': 'Электронная почта', 
                    'contact': self.json_dict['email'].strip() \
                        if 'email' in self.json_dict else 'Отсутствует',
                }
            ]
            self.staff = [
                {
                    'position': self.json_dict['positionName'].strip() \
                        if 'positionName' in self.json_dict else 'Отсутствует',
                    'department': self.json_dict['department'].strip() \
                        if 'department' in self.json_dict else 'Отсутствует'
                }
            ]
            self.addition = self.parse_addition()
            

    def parse_fullname(self):
        lastName = self.json_dict['lastName'].strip() \
            if 'lastName' in self.json_dict else 'ОТСУТСТВУЕТ!!!'
        firstName = self.json_dict['firstName'].strip() \
            if 'firstName' in self.json_dict else 'ОТСУТСТВУЕТ!!!'
        midName = self.json_dict['midName'].strip() \
            if 'midName' in self.json_dict else ''
        return f"{lastName} {firstName} {midName}".rstrip()
    
    def parse_birthday(self):
        birthday = datetime.strptime(self.json_dict['birthday'], '%Y-%m-%d') \
            if 'birthday' in self.json_dict else datetime.strptime('1900-01-01', '%Y-%m-%d')
        return birthday

    def parse_previous(self):
        if 'hasNameChanged' in self.json_dict:
            if len(self.json_dict['nameWasChanged']):
                previous = []
                for item in self.json_dict['nameWasChanged']:
                    firstNameBeforeChange = item['firstNameBeforeChange'].strip() \
                        if 'firstNameBeforeChange' in item else ''
                    lastNameBeforeChange = item['lastNameBeforeChange'].strip() \
                        if 'lastNameBeforeChange' in item else ''
                    midNameBeforeChange = item['midNameBeforeChange'].strip() \
                        if 'midNameBeforeChange' in item else ''
                    yearOfChange = str(item['yearOfChange']) \
                        if 'yearOfChange' in item else 'Отсутствует'
                    reason = str(item['reason']).strip() \
                        if 'reason' in item else 'Причина неизвестна'
                    previous.append(f"{yearOfChange} - {firstNameBeforeChange} "
                                    f"{lastNameBeforeChange} {midNameBeforeChange}, "
                                    f"{reason}".replace("  ", ""))
                return '; '.join(previous)
        return ''
    
    def parse_education(self):
        if 'education' in self.json_dict:
            if len(self.json_dict['education']):
                education = []
                for item in self.json_dict['education']:
                    institutionName = item['institutionName'] \
                        if 'institutionName' in item else 'Нет данных'
                    endYear = item['endYear'] if 'specialty' in item else 'н.в.'
                    specialty = item['specialty'] \
                        if 'specialty' in item else 'неизвестно'
                    education.append(f"{str(endYear)} - {institutionName}, "
                                     f"{specialty}".replace("  ", ""))
                return '; '.join(education)
        return ''
    
    def parse_workplace(self):
        if 'experience' in self.json_dict:
            if len(self.json_dict['experience']):
                experience = []
                for item in self.json_dict['experience']:
                    work = {
                        'start_date': datetime.strptime(item['beginDate'], '%Y-%m-%d') \
                            if 'beginDate' in item \
                                else datetime.strptime('1900-01-01', '%Y-%m-%d'),
                        'end_date': datetime.strptime(item['endDate'], '%Y-%m-%d') \
                            if 'endDate' in item \
                                else datetime.now().date(),
                        'workplace': item['name'].strip() if 'name' in item else '',
                        'address': item['address'].strip() if 'address' in item else '',
                        'position': item['position'].strip() if 'position' in item else '',
                        'reason': item['fireReason'].strip() if 'fireReason' in item else ''
                    }
                    experience.append(work)
                return experience
        return []
    
    def parse_addition(self):
        public = []
        if self.json_dict['hasPublicOfficeOrganizations']:
            if len(self.json_dict['publicOfficeOrganizations']):
                for item in self.json_dict['publicOfficeOrganizations']:
                    public.append(f"{item['name'] if 'name' in item else ''}, "
                                  f"{item['position'] if 'position' in item else ''}")

        state = []
        if self.json_dict['hasStateOrganizations']:
            if len(self.json_dict['stateOrganizations']):
                for item in self.json_dict['publicOfficeOrganizations']:
                    state.append(f"{item['name'] if 'name' in item else ''}, "
                                 f"{item['position'] if 'position' in item else ''}")

        related = []
        if self.json_dict['hasRelatedPersonsOrganizations']:
            if len(self.json_dict['hasRelatedPersonsOrganizations']):
                for item in self.json_dict['hasRelatedPersonsOrganizations']:
                    related.append(f"{item['name'] if 'name' in item else ''}, "
                                   f"{item['inn'] if 'inn' in item else ''}, "
                                   f"{item['position'] if 'position' in item else ''}")
        
        organization = []
        if self.json_dict['hasOrganizations']:
            if len(self.json_dict['organizations']):
                for item in self.json_dict['organizations']:
                    organization.append(f"{item['orgType'] if 'orgType' in item else ''} "
                                        f"{item['inn'] if 'inn' in item else ''} "
                                        f"{item['name'] if 'name' in item else ''} "
                                        f"{item['workCombinationTime'] if 'workCombinationTime' in item else ''}")
        
        return (f"{'; '.join(public)}. {'; '.join(state)}. "
                f"{'; '.join(related)}. {'; '.join(organization)}.")



def add_resume(resume: dict, location_id, action):
    """
    Adds a resume to the database.
    """
    result = db.session.query(Person).\
        filter(Person.fullname.ilike(resume['fullname']),
               Person.birthday==resume['birthday']).one_or_none()
    if result:
        if action == "create" or action == 'api':
            resume.update({'status': Status.repeat.value, 'region_id': location_id})
        else:
            resume.update({'status': Status.update.value, 'region_id': location_id})
        for k, v in resume.items():
            setattr(result, k, v)
        person_id = result.id
        
        if result.path and not os.path.isdir(os.path.join(current_app.config["BASE_PATH"], 
                                                          result.path)):
            os.mkdir(result.path)
        elif not result.path:
            new_path = os.path.join(current_app.config["BASE_PATH"], 
                                    resume['fullname'][0].upper(),
                                    f'{person_id}-{resume["fullname"]}')
            if not os.path.isdir(new_path):
                os.mkdir(new_path)
            result.path = os.path.join(resume['fullname'][0].upper(), 
                                       f'{person_id}-{resume["fullname"]}')
    else:
        person = Person(**resume | {'region_id': location_id})
        db.session.add(person)
        db.session.flush()
        person_id = person.id
        
        path = os.path.join(current_app.config["BASE_PATH"], 
                            resume['fullname'][0].upper(),
                            f'{person_id}-{resume["fullname"]}')
        if not os.path.isdir(path):
            os.mkdir(path)
        
        person.path = os.path.join(resume['fullname'][0].upper(),
                                   f'{person_id}-{resume["fullname"]}')

    db.session.commit()
    return person_id


def create_folders(person_id, fullname, folder_name):
    """
    Check if a folder exists for a given person and create it if it does not exist.
    """
    url = os.path.join(current_app.config["BASE_PATH"], 
                       fullname[0].upper(), 
                       f'{person_id}-{fullname}')
    if not os.path.isdir(url):
        os.mkdir(url)
    folder = os.path.join(url, folder_name)
    if not os.path.isdir(folder):
        os.mkdir(folder)
    subfolder = os.path.join(folder, datetime.now().strftime("%Y-%m-%d"))
    if not os.path.isdir(subfolder):
        os.mkdir(subfolder)
    return os.path.join(fullname[0].upper(), 
                        f'{person_id}-{fullname}', 
                        folder, subfolder)


json_struct = {
  "positionName": "Главный инженер по разработке",
  "department": "Группа разработки",
  "statusDate": "2023-10-23T11:14:24Z",
  "lastName": "Иванов",
  "firstName": "Иван",
  "midName": "Андреевич",
  "hasNameChanged": True,
  "nameWasChanged": [
    {
      "reason": "развод",
      "firstNameBeforeChange": "Петр",
      "lastNameBeforeChange": "Семенов",
      "hasNoMidNameBeforeChange": True,
      "yearOfChange": 2020,
      "nameChangeDocument": "документ"
    },
    {
      "reason": "усыновление/удочерение",
      "firstNameBeforeChange": "Степан",
      "lastNameBeforeChange": "Игоревич",
      "midNameBeforeChange": "Васильев",
      "yearOfChange": 2017,
      "nameChangeDocument": "документ 2"
    }
  ],
  "birthday": "1998-10-10",
  "birthplace": "Москва",
  "citizen": "Россия",
  "hasAdditionalCitizenship": True,
  "additionalCitizenship": "Австралия",
  "maritalStatus": "незарегистрированный брак",
  "regAddress": "Ленина 5",
  "validAddress": "Ленина 5",
  "contactPhone": "+70000000000",
  "hasNoRussianContactPhone": True,
  "email": "mail@pulse.com",
  "hasInn": True,
  "inn": "510189523890",
  "hasSnils": True,
  "snils": "36033751254",
  "passportSerial": "1234",
  "passportNumber": "566789",
  "passportIssueDate": "2015-05-10",
  "passportIssuedBy": "УФМС",
  "education": [
    {
      "educationType": "высшее",
      "institutionName": "МГУ",
      "beginYear": 2017,
      "endYear": 2020,
      "specialty": "менеджмент"
    },
    {
      "educationType": "MBA",
      "institutionName": "МГИМО",
      "beginYear": 2022,
      "endYear": 2023,
      "specialty": "экономика"
    }
  ],
  "hasJob": True,
  "experience": [
    {
      "beginDate": "1988-01-10",
      "endDate": "1989-01-10",
      "name": "ООО Мария",
      "address": "Ленина 1",
      "phone": "+70000000001",
      "activityType": "продажи",
      "position": "менеджер",
      "isPositionMatchEmploymentContract": True,
      "employmentContractPosition": "менеджер по продажам",
      "fireReason": "по собственному желанию"
    },
    {
      "beginDate": "1991-01-10",
      "currentJob": True,
      "name": "ПАО Александра",
      "address": "Ленина 9",
      "phone": "+70000000002",
      "activityType": "продажи",
      "position": "менеджер по обслуживанию"
    }
  ],
  "hasPublicOfficeOrganizations": True,
  "publicOfficeOrganizations": [
    {
      "name": "Учреждение А",
      "position": "стажер"
    },
    {
      "name": "Учреждение Б",
      "position": "методолог"
    }
  ],
  "hasStateOrganizations": True,
  "stateOrganizations": [
    {
      "name": " Министерство А",
      "position": "эксперт"
    },
    {
      "name": " Министерство Б",
      "position": "главный эксперт"
    }
  ],
  "hasRelatedPersonsOrganizations": True,
  "relatedPersonsOrganizations": [
    {
      "name": "Имя 1",
      "inn": "3171083718",
      "position": "специалист"
    },
    {
      "name": "Имя 2",
      "inn": "3171083718",
      "position": "ведущий специалист"
    }
  ],
  "hasMtsRelatedPersonsOrganizations": True,
  "mtsRelatedPersonsOrganizations": [
    {
      "name": "Имя 3"
    },
    {
      "name": "Имя 4"
    }
  ],
  "hasOrganizations": True,
  "organizations": [
    {
      "orgType": "самозанятость",
      "inn": "510189523890",
      "name": "ООО Смирнов",
      "workCombinationTime": "договор"
    },
    {
      "orgType": "ПАО",
      "inn": "3171083718",
      "name": "ОАО Иванов",
      "workCombinationTime": "договор"
    }
  ]
}

