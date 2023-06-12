from datetime import datetime
import openpyxl

from app.models.model import db, Staff, Document, Address, Contact, Workplace

BASE_PATH = r'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\Персонал\Персонал-3\\'
URL_CHECK = "https://httpbin.org/post"


class ExcelFile:  # получение анкетной информации из файла Excel
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
            'education': str(self.sheet['X3'].value).strip(),
            'recruiter': str(self.sheet['E3'].value).strip()
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
                'period': str(self.sheet[f'AA{i}'].value).strip(),
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



# загрузка непостоянных данных из Excel и Json  в БД
def resume_data(cand_id, document, addresses, contacts, workplaces, staff):
    objects_to_add = []
    if staff['position']:
        objects_to_add.append(Staff(**staff | {'cand_id': cand_id}))
    if document['number']:
        objects_to_add.append(Document(**document | {'cand_id': cand_id}))
    for address in addresses:
        if address['address']:
            objects_to_add.append(Address(**address | {'cand_id': cand_id}))
    for contact in contacts:
        if contact['contact']:
            objects_to_add.append(Contact(**contact | {'cand_id': cand_id}))
    for work in workplaces:
        if work['workplace']:
            objects_to_add.append(Workplace(**work | {'cand_id': cand_id}))
    db.session.add_all(objects_to_add)
    db.session.commit()
