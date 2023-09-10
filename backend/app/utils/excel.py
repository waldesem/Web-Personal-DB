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
            'fullname': str(self.sheet['K3'].value).title().strip().title(),
            'previous': str(self.sheet['S3'].value).strip(),
            'birthday': datetime.strptime(str(self.sheet['L3'].value).strip(), '%d.%m.%Y').date() \
                if re.match(r'\d\d.\d\d.\d\d\d\d', str(self.sheet['L3'].value).strip()) \
                    else datetime.strptime('2000-01-01', '%Y-%m-%d').date(),
            'birthplace': str(self.sheet['M3'].value).strip(),
            'country': str(self.sheet['T3'].value).strip(),
            'snils': str(self.sheet['U3'].value).strip().replace(" ", "").replace("-", "")[:11],
            'inn': str(self.sheet['V3'].value).strip()[:12],
            'education': str(self.sheet['X3'].value).strip()
        }
        self.passport = {
            'view': 'Паспорт гражданина России',
            'series': str(self.sheet['P3'].value).strip()[:4],
            'number': str(self.sheet['Q3'].value).strip()[:6],
            'issue': datetime.strptime(str(self.sheet['R3'].value).strip(), '%d.%m.%Y').date() \
                if re.match(r'\d\d.\d\d.\d\d\d\d', str(self.sheet['L3'].value).strip()) \
                    else datetime.strptime('2000-01-01', '%Y-%m-%d').date(),
        }
        self.addresses = [
            {'view': "Адрес регистрации", 'address': str(self.sheet['N3'].value).strip()},
            {'view': "Адрес проживания", 'address': str(self.sheet['O3'].value).strip()}
        ]
        self.contacts = [
            {'view': str(self.sheet['Y1'].value).strip(), 'contact': str(self.sheet['Y3'].value).strip()},
            {'view': str(self.sheet['Z1'].value).strip(), 'contact': str(self.sheet['Z3'].value).strip()}
        ]
        self.workplaces = [
            {
            'workplace': str(self.sheet[f'AB{i}'].value).strip(),
            'address': str(self.sheet[f'AC{i}'].value).strip(),
            'position': str(self.sheet[f'AD{i}'].value).strip()
            } | self.parse_period(self.sheet[f'AA{i}'].value)
            for i in range(3, 6) if self.sheet[f'AB{i}'].value
        ]
        self.staff = {
            'position': str(self.sheet['C3'].value).strip(),
            'department': str(self.sheet['D3'].value).strip()
        }

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
