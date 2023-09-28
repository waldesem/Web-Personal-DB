import os
import re
from datetime import datetime

import openpyxl
from flask import current_app
from ..models.model import db, Staff, Document, Address, Contact, Workplace, Person
from ..models.classes import Status
from datetime import datetime


class ExcelFile:
    """ Create class for import data from excel files"""

    def __init__(self, file) -> None:
        self.file = file
        self.wb = openpyxl.load_workbook(self.file, keep_vba=True)
        self.sheet = self.wb.worksheets[0]

        self.resume = {
            'fullname': self.parse_cell(self.sheet['K3']).title(),
            'previous': self.parse_cell(self.sheet['S3']).title(),
            'birthday': self.parse_date(self.parse_cell(self.sheet['L3'])),
            'birthplace': str(self.sheet['M3']).strip(),
            'country': self.parse_cell(self.sheet['T3']),
            'snils': self.parse_cell(self.sheet['U3']).replace(" ", "").\
                replace("-", "")[:11],
            'inn': self.parse_cell(self.sheet['V3'], 12),
            'education': str(self.sheet['X3']).strip()
        }
        self.passport = {
            'view': 'Паспорт гражданина России',
            'series': self.parse_cell(self.sheet['P3'], 4),
            'number': self.parse_cell(self.sheet['Q3'], 6),
            'issue': self.parse_date(self.parse_cell(self.sheet['R3'])),
        }
        self.addresses = [
            {'view': "Адрес регистрации", 
             'address': self.parse_cell(self.sheet['N3'])},
            {'view': "Адрес проживания", 
             'address': str(self.sheet['O3']).strip()}
        ]
        self.contacts = [
            {'view': self.parse_cell(self.sheet['Y1']), 
             'contact': self.parse_cell(self.sheet['Y3']).replace(" ", "")},
            {'view': self.parse_cell(self.sheet['Z1']), 
             'contact': self.parse_cell(self.sheet['Z3']).replace(" ", "")}
        ]
        self.workplaces = [
            {
            'workplace': str(self.sheet[f'AB{i}']).strip(),
            'address': str(self.sheet[f'AC{i}']).strip(),
            'position': str(self.sheet[f'AD{i}']).strip()
            } | self.parse_period(self.sheet[f'AA{i}'].value)
            for i in range(3, 6) if self.sheet[f'AB{i}'].value
        ]
        self.staff = {
            'position': str(self.sheet['C3']).strip(),
            'department': str(self.sheet['D3']).strip
        }

    def parse_cell(self, cell, limit=255):
        return str(cell.value).strip()[:limit]
    
    def parse_date(self, data):
        return datetime.strptime(data, '%d.%m.%Y').date() \
                if re.match(r'\d\d.\d\d.\d\d\d\d', data) \
                    else datetime.strptime('2000-01-01', '%Y-%m-%d').date()

    def parse_period(self, cell):
        """ Parse period from excel file """
        lst = re.split(r'-', cell)
        if len(lst) == 2:
            start, end = lst[0].strip(), lst[1].strip()
            start_date = self.parse_date(start)
            end_date = datetime.strptime(end, '%d.%m.%Y').date() \
                if re.match(r'\d\d.\d\d.\d\d\d\d', end) \
                    else datetime.now().date()
        
        elif len(lst) and len(lst) != 2:
            start_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()
            end_date = datetime.now().date()
        return {'start_date': start_date, 'end_date': end_date}

    def close(self):
        self.wb.close()


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
        
        if result.path and not os.path.isdir(result.path):
            os.mkdir(result.path)
        elif not result.path:
            new_path = os.path.join(current_app.config["BASE_PATH"], 
                                    f'{person_id}-{resume["fullname"]}')
            if not os.path.isdir(new_path):
                os.mkdir(new_path)
            result.path = new_path
    else:
        person = Person(**resume | {'region_id': location_id})
        db.session.add(person)
        db.session.flush()
        person_id = person.id
        
        path = os.path.join(current_app.config["BASE_PATH"], 
                            f'{person_id}-{resume["fullname"]}')
        person.path = path
        if not os.path.isdir(path):
            os.mkdir(path)
        
    db.session.commit()
    return person_id


def create_folders(person_id, fullname, folder_name):
    """
    Check if a folder exists for a given person and create it if it does not exist.
    """
    url = os.path.join(current_app.config["BASE_PATH"], f'{person_id}-{fullname}')
    if not os.path.isdir(url):
        os.mkdir(url)
    folder = os.path.join(url, folder_name)
    if not os.path.isdir(folder):
        os.mkdir(folder)
    subfolder = os.path.join(folder, datetime.now().strftime("%Y-%m-%d"))
    if not os.path.isdir(subfolder):
        os.mkdir(subfolder)
    return subfolder
