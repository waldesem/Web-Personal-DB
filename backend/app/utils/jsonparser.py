import re
import json
from datetime import datetime

from sqlalchemy import select

from ..models.model import async_session, Region

class JsonFile:
    """ Create class for import data from json file"""

    def __init__(self, file) -> None:
        with open(file, 'r', newline='', encoding='utf-8-sig') as f:
            self.json_dict = json.load(f)

            self.resume = {
                'region_id': self.parse_region() if self.parse_region() else 1,
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
            self.affilation = self.parse_affilation()
    
    async def parse_region(self):
        async with async_session() as session:
            regions = await {rgn[1]: rgn[0] for rgn \
                             in session.execute(select(Region.id, 
                                                       Region.region)).all()}
            if 'department' in self.json_dict:
                divisions = re.split(r'/', self.json_dict['department'].strip())
                return [regions.get(div.strip(), 1) for div in divisions][0]
    
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
    
    def parse_affilation(self):
        affilation = []
        if self.json_dict['hasPublicOfficeOrganizations']:
            if len(self.json_dict['publicOfficeOrganizations']):
                for item in self.json_dict['publicOfficeOrganizations']:
                    public = {
                        'view': 'Являлся государственным или муниципальным служащим',
                        'name': f"{item['name'] if 'name' in item else ''}",
                        'position': f"{item['position'] if 'position' in item else ''}"
                    }
                    affilation.append(public)

        if self.json_dict['hasStateOrganizations']:
            if len(self.json_dict['stateOrganizations']):
                for item in self.json_dict['publicOfficeOrganizations']:
                    state = {
                        'view': 'Являлся государственным должностным лицом',
                        'name': f"{item['name'] if 'name' in item else ''}",
                        'position': f"{item['position'] if 'position' in item else ''}"
                    }
                    affilation.append(state)

        if self.json_dict['hasRelatedPersonsOrganizations']:
            if len(self.json_dict['relatedPersonsOrganizations']):
                for item in self.json_dict['relatedPersonsOrganizations']:
                    related = {
                        'view': 'Связанные лица работают в госудраственных организациях',
                        'name': f"{item['name'] if 'name' in item else ''}",
                        'position': f"{item['position'] if 'position' in item else ''}",
                        'inn': f"{item['inn'] if 'inn' in item else ''}"
                    }
                    affilation.append(related)
        
        if self.json_dict['hasOrganizations']:
            if len(self.json_dict['organizations']):
                for item in self.json_dict['organizations']:
                    organization = {
                        'view': 'Участвует в деятельности коммерческих организаций"',
                        'name': f"{item['name'] if 'name' in item else ''}",
                        'position': f"{item['workCombinationTime'] if 'workCombinationTime' in item else ''}",
                        'inn': f"{item['inn'] if 'inn' in item else ''}"
                    }
                    affilation.append(organization)
        return affilation