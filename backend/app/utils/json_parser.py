import os
import json
from datetime import datetime

import openpyxl

class JsonFile:
    """ Create class for import data from json file"""

    def __init__(self, file) -> None:
        with open(file, 'r', newline='', encoding='utf-8-sig') as f:
            self.json_dict = json.load(f)

            self.resume = {
                'data': datetime.strptime(self.json_dict['statusDate'], "%Y-%m-%dT%H:%M:%SZ"),
                'fullname': self.parse_fullname(),
                'previous': self.parse_previous(),
                'birthday': self.parse_birthday(),
                'birthplace': self.json_dict['birthplace'].strip() \
                    if 'birthplace' in self.json_dict else 'Неизвестно',
                'country': f"{self.json_dict['citizen'] if 'citizen' in self.json_dict else ''}",
                'ext_country': f"{self.json_dict['additionalCitizenship'] if 'additionalCitizenship' in self.json_dict else ''}",
                'snils': self.json_dict['snils'].strip() if 'snils' in self.json_dict else '',
                'inn': self.json_dict['inn'].strip() if 'inn' in self.json_dict else '',
                'education': self.parse_education()
            }
            
            self.workplaces = self.parse_workplace()
            
            self.passport = [
                {
                    'view': 'Паспорт',
                    'series': self.json_dict['passportSerial'].strip() if 'passportSerial' in self.json_dict else '',
                    'number': self.json_dict['passportNumber'].strip() if 'passportNumber' in self.json_dict else '',
                    'issue': datetime.strptime(self.json_dict['passportIssueDate'], '%Y-%m-%d').date() \
                        if 'passportIssueDate' in self.json_dict else datetime.strptime('1900-01-01', '%Y-%m-%d').date(),
                    'issued': self.json_dict['passportIssuedBy'].strip() if 'passportIssuedBy' in self.json_dict else '',
                }
            ]
            self.addresses = [
                {
                    'view': "Адрес регистрации", 
                    'address': self.json_dict['regAddress'].strip() if 'regAddress' in self.json_dict else '',
                },
                {
                    'view': "Адрес проживания", 
                    'address': self.json_dict['validAddress'].strip() if 'validAddress' in self.json_dict else '',
                }
            ]
            self.contacts = [
                {
                    'view': 'Мобильный телефон', 
                    'contact': self.json_dict['contactPhone'].strip() if 'contactPhone' in self.json_dict else '',
                },
                {
                    'view': 'Электронная почта', 
                    'contact': self.json_dict['email'].strip() if 'email' in self.json_dict else '',
                }
            ]
            self.staff = [
                {
                    'position': self.json_dict['positionName'].strip() if 'positionName' in self.json_dict else '',
                    'department': self.json_dict['department'].strip() if 'department' in self.json_dict else ''
                }
            ]
            self.addition = self.parse_addition()
            

    def parse_fullname(self):
        try:
            lastName = self.json_dict['lastName'].strip()
            firstName = self.json_dict['firstName'].strip()
            midName = self.json_dict['midName'].strip() if 'midName' in self.json_dict else ''
        except KeyError as error:
            print(f"Обязательный ключ {error} отсутствует")
            exit()
        return f"{lastName} {firstName} {midName}".rstrip()
    
    def parse_birthday(self):
        try:
            birthday = datetime.strptime(self.json_dict['birthday'], '%Y-%m-%d').date()
        except KeyError as error:
            print(f"Обязательный ключ {error} отсутствует")
            exit()
        return birthday

    def parse_previous(self):
        if 'hasNameChanged' in self.json_dict:
            if len(self.json_dict['nameWasChanged']):
                previous = []
                for item in self.json_dict['nameWasChanged']:
                    firstNameBeforeChange = item['firstNameBeforeChange'].strip() if 'firstNameBeforeChange' in item else ''
                    lastNameBeforeChange = item['lastNameBeforeChange'].strip() if 'lastNameBeforeChange' in item else ''
                    midNameBeforeChange = item['midNameBeforeChange'].strip() if 'midNameBeforeChange' in item else ''
                    yearOfChange = str(item['yearOfChange']) if 'yearOfChange' in item else 'Дата неизвестна'
                    reason = str(item['reason']).strip() if 'reason' in item else 'Причина неизвестна'
                    previous.append(f"{yearOfChange} - {firstNameBeforeChange} {lastNameBeforeChange} {midNameBeforeChange}, {reason}".replace("  ", ""))
                return '; '.join(previous)
        return ''
    
    def parse_education(self):
        if 'education' in self.json_dict:
            if len(self.json_dict['education']):
                education = []
                for item in self.json_dict['education']:
                    institutionName = item['institutionName'] if 'institutionName' in item else 'Нет данных'
                    beginYear = item['beginYear'] if 'specialty' in item else 'Неизвестно'
                    endYear = item['endYear'] if 'specialty' in item else 'н.в.'
                    specialty = item['specialty'] if 'specialty' in item else 'неизвестно'
                    education.append(f"{str(beginYear)}-{str(endYear)} - {institutionName}, {specialty}".replace("  ", ""))
                return '; '.join(education)
        return ''
    
    def parse_workplace(self):
        if 'experience' in self.json_dict:
            if len(self.json_dict['experience']):
                experience = []
                for item in self.json_dict['experience']:
                    work = {
                        'start_date': datetime.strptime(item['beginDate'], '%Y-%m-%d').date() \
                            if 'beginDate' in item else datetime.strptime('1900-01-01', '%Y-%m-%d').date(),
                        'end_date': datetime.strptime(item['endDate'], '%Y-%m-%d').date() \
                            if 'endDate' in item else datetime.now().date(),
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
                    public.append(f"{item['name'] if 'name' in item else ''}, {item['position'] if 'position' in item else ''}")

        state = []
        if self.json_dict['hasStateOrganizations']:
            if len(self.json_dict['stateOrganizations']):
                for item in self.json_dict['publicOfficeOrganizations']:
                    state.append(f"{item['name'] if 'name' in item else ''}, {item['position'] if 'position' in item else ''}")

        relation = []
        if self.json_dict['hasMtsRelatedPersonsOrganizations']:
            if len(self.json_dict['mtsRelatedPersonsOrganizations']):
                for item in self.json_dict['mtsRelatedPersonsOrganizations']:
                    relation.append(f"{item['name'] if 'name' in item else ''}")
        
        organization = []
        if self.json_dict['hasOrganizations']:
            if len(self.json_dict['organizations']):
                for item in self.json_dict['organizations']:
                    organization.append(f"{item['orgType'] if 'orgType' in item else ''} {item['inn'] if 'inn' in item else ''} {item['name'] if 'name' in item else ''} {item['workCombinationTime'] if 'workCombinationTime' in item else ''}")
        
        return f"{'; '.join(public)}. {'; '.join(state)}. {'; '.join(relation)}. {'; '.join(organization)}."


class ExcelFile:
    """ Create class for export data to excel files"""

    def __init__(self, file) -> None:
        self.file = file
        self.wb = openpyxl.load_workbook(self.file, keep_vba=True)
        self.sheet = self.wb.worksheets[0]

    def upload_data(self, data):
        self.sheet['A3'] = datetime.strftime(data.resume['data'], "%H:%M:%S %d.%m.%Y")
        self.sheet['C3'] = data.staff[0]['position']
        self.sheet['D3'] = data.staff[0]['department']
        self.sheet['K3'] = data.resume['fullname']
        self.sheet['K3'] = data.resume['fullname']
        self.sheet['S3'] = data.resume['previous']
        self.sheet['L3'] = datetime.strftime(data.resume['birthday'], "%d.%m.%Y")
        self.sheet['M3'] = data.resume['birthplace']
        self.sheet['T3'] = data.resume['country']
        self.sheet['U3'] = data.resume['snils']
        self.sheet['V3'] = data.resume['inn']
        self.sheet['X3'] = data.resume['education']
        self.sheet['P3'] = data.passport[0]['series']
        self.sheet['Q3'] = data.passport[0]['number']
        self.sheet['R3'] = data.passport[0]['issue']
        self.sheet['N3'] = data.addresses[0]['address']
        self.sheet['O3'] = data.addresses[1]['address']
        self.sheet['Y3'] = data.contacts[0]['contact']
        self.sheet['Z3'] = data.contacts[1]['contact']
        
        if len(data.workplaces):
            for index, value in enumerate(data.workplaces):
                self.sheet[f'AA{index + 3}'] = f"{datetime.strftime(value['start_date'], '%d.%m.%Y')} - {datetime.strftime(value['end_date'], '%d.%m.%Y')}"
                self.sheet[f'AB{index + 3}'] = value['workplace']
                self.sheet[f'AC{index + 3}'] = value['address']
                self.sheet[f'AD{index + 3}'] = value['position']
        self.wb.save(data.resume['fullname']+'.xlsx')


if __name__ == "__main__":
    
    lst_dir = os.listdir(os.getcwd())
    for file in lst_dir:
        if file.endswith('.json'):
            data = JsonFile(file)
            export = ExcelFile('anketa.xlsx')
            export.upload_data(data)
