from datetime import datetime
import re
import openpyxl

from app.models.model import db, Staff, Document, Address, Contact, Workplace


class ExcelFile:
    """ Create class for import data from excel files"""

    def __init__(self, file) -> None:
        self.file = file
        self.wb = openpyxl.load_workbook(self.file, keep_vba=True)
        self.sheet = self.wb.worksheets[0]

        self.resume = {
            'fullname': self.parse_cell(self.sheet['K3']).title(),
            'previous': self.parse_cell(self.sheet['S3']).title(),
            'birthday': datetime.strptime(self.parse_cell(self.sheet['L3']), '%d.%m.%Y').date() \
                if re.match(r'\d\d.\d\d.\d\d\d\d', self.parse_cell(self.sheet['L3'])) \
                    else datetime.strptime('2000-01-01', '%Y-%m-%d').date(),
            'birthplace': self.parse_cell(self.sheet['M3']),
            'country': self.parse_cell(self.sheet['T3']),
            'snils': self.parse_cell(self.sheet['U3']).replace(" ", "").replace("-", "")[:11],
            'inn': self.parse_cell(self.sheet['V3'], 12),
            'education': self.parse_cell(self.sheet['X3'])
        }
        self.passport = {
            'view': 'Паспорт гражданина России',
            'series': self.parse_cell(self.sheet['P3'], 4),
            'number': self.parse_cell(self.sheet['Q3'], 6),
            'issue': datetime.strptime(self.parse_cell(self.sheet['R3']), '%d.%m.%Y').date() \
                if re.match(r'\d\d.\d\d.\d\d\d\d', self.parse_cell(self.sheet['L3'])) \
                    else datetime.strptime('2000-01-01', '%Y-%m-%d').date(),
        }
        self.addresses = [
            {'view': "Адрес регистрации", 
             'address': self.parse_cell(self.sheet['N3'])},
            {'view': "Адрес проживания", 
             'address': self.parse_cell(self.sheet['O3'])}
        ]
        self.contacts = [
            {'view': self.parse_cell(self.sheet['Y1']), 
             'contact': self.parse_cell(self.sheet['Y3']).replace(" ", "")},
            {'view': self.parse_cell(self.sheet['Z1']), 
             'contact': self.parse_cell(self.sheet['Z3']).replace(" ", "")}
        ]
        self.workplaces = [
            {
            'workplace': self.parse_cell(self.sheet[f'AB{i}']),
            'address': self.parse_cell(self.sheet[f'AC{i}']),
            'position': self.parse_cell(self.sheet[f'AD{i}'])
            } | self.parse_period(self.sheet[f'AA{i}'].value)
            for i in range(3, 6) if self.sheet[f'AB{i}'].value
        ]
        self.staff = {
            'position': self.parse_cell(self.sheet['C3']),
            'department': self.parse_cell(self.sheet['D3'])
        }

    def parse_cell(self, cell, limit=255):
        return str(cell.value).strip()[:limit]

    def parse_period(self, cell):
        """ Parse period from excel file """
        lst = re.split(r'-', cell)
        if len(lst) == 2:
            start, end = lst[0].strip(), lst[1].strip()
            
            start_date = datetime.strptime(start, '%d.%m.%Y').date() \
                if re.match(r'\d\d.\d\d.\d\d\d\d', start) \
                    else datetime.strptime('2000-01-01', '%Y-%m-%d').date()
            end_date = datetime.strptime(end, '%d.%m.%Y').date() \
                if re.match(r'\d\d.\d\d.\d\d\d\d', end) \
                    else datetime.now().date()
        else:
            start_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()
            end_date = datetime.now().date()
        return {'start_date': start_date, 'end_date': end_date}


def resume_data(person_id, document, addresses, contacts, workplaces, staff):
    """
    Adds resume data to the database for a person.
    Args:
        person_id (int): The ID of the person.
        document (dict): A dictionary containing document information.
        addresses (list): A list of dictionaries containing address information.
        contacts (list): A list of dictionaries containing contact information.
        workplaces (list): A list of dictionaries containing workplace information.
        staff (dict): A dictionary containing staff information.
    Returns:
        None
    """
    db.session.add(Staff(**staff | {'person_id': person_id}))
    db.session.add(Document(**document | {'person_id': person_id}))
    for address in addresses:
        db.session.add(Address(**address | {'person_id': person_id}))
    for contact in contacts:
        db.session.add(Contact(**contact | {'person_id': person_id}))
    for workplace in workplaces:
        db.session.add(Workplace(**workplace | {'person_id': person_id}))
    db.session.commit()
