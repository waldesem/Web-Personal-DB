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
            'fullname': str(self.sheet['K3'].value).title().strip(),
            'previous': str(self.sheet['S3'].value).strip(),
            'birthday': datetime.strptime(str(self.sheet['L3'].value).strip(), '%d.%m.%Y').date(),
            'birthplace': str(self.sheet['M3'].value).strip(),
            'country': str(self.sheet['T3'].value).strip(),
            'snils': str(self.sheet['U3'].value).strip(),
            'inn': str(self.sheet['V3'].value).strip(),
            'education': str(self.sheet['X3'].value).strip()
        }
        self.passport = {
            'view': 'Паспорт гражданина России',
            'series': str(self.sheet['P3'].value).strip(),
            'number': str(self.sheet['Q3'].value).strip(),
            'issue': datetime.strptime(str(self.sheet['R3'].value).strip(), '%d.%m.%Y').date()
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
            'start_date': datetime.strptime(re.split(r'-', str(self.sheet[f'AA{i}'].value))[0].strip(), '%d.%m.%Y').date() \
                if re.match(r'\d\d.\d\d.\d\d\d\d', re.split(r'-', str(self.sheet[f'AA{i}'].value))[0].strip()) \
                    else datetime.strptime('2000-01-01', '%Y-%m-%d').date(),

            'end_date': datetime.strptime(re.split(r'-', str(self.sheet[f'AA{i}'].value))[1].strip(), '%d.%m.%Y').date() \
                 if re.match(r'\d\d.\d\d.\d\d\d\d', re.split(r'-', str(self.sheet[f'AA{i}'].value))[1].strip()) \
                    else datetime.now().date(),
                        
            'workplace': str(self.sheet[f'AB{i}'].value).strip(),
            'address': str(self.sheet[f'AC{i}'].value).strip(),
            'position': str(self.sheet[f'AD{i}'].value).strip()
            }
            for i in range(3, 6)
        ]
        self.staff = {
            'position': str(self.sheet['C3'].value).strip(),
            'department': str(self.sheet['D3'].value).strip()
        }


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
