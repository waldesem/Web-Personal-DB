from datetime import datetime
import openpyxl

from app.models.model import *
from app.forms.form import *

BASE_PATH = r'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\Персонал\Персонал-3\\'
TODAY = datetime.now()
URL_CHECK = "https://httpbin.org/post"


class ExcelFile:  # получение анкетной информации из файла Excel
    """ Create class for import data from excel files"""

    def __init__(self, file) -> None:
        self.file = file
        self.wb = openpyxl.load_workbook(self.file, keep_vba=True)
        self.sheet = self.wb.worksheets[0]
        self.resume = dict(fullname=str(self.sheet['K3'].value).title().strip(),
                           previous=str(self.sheet['S3'].value).strip(),
                           birthday=datetime.strptime(str(self.sheet['L3'].value).strip(), '%d.%m.%Y').date(),
                           birthplace=str(self.sheet['M3'].value).strip(),
                           country=str(self.sheet['T3'].value).strip(),
                           snils=str(self.sheet['U3'].value).strip(),
                           inn=str(self.sheet['V3'].value).strip(),
                           education=str(self.sheet['X3'].value).strip(),
                           status=STATUS['new'],
                           deadline=TODAY)
        self.passport = dict(view='Паспорт гражданина России',
                             series=str(self.sheet['P3'].value).strip(),
                             number=str(self.sheet['Q3'].value).strip(),
                             issue=datetime.strptime(str(self.sheet['R3'].value).strip(), '%d.%m.%Y').date())

        self.addresses = [dict(view="Адрес регистрации",
                               address=str(self.sheet['N3'].value).strip()),
                          dict(view="Адрес проживания",
                               address=str(self.sheet['O3'].value).strip())]
        self.contacts = [dict(view=str(self.sheet['Y1'].value).strip(),
                              contact=str(self.sheet['Y3'].value).strip()),
                         dict(view=str(self.sheet['Z1'].value).strip(),
                              contact=str(self.sheet['Z3'].value).strip())]
        self.workplaces = [dict(period=str(self.sheet['AA3'].value).strip(),
                                workplace=str(self.sheet['AB3'].value).strip(),
                                address=str(self.sheet['AC3'].value).strip(),
                                position=self.sheet['AD3'].value.strip()),
                           dict(period=str(self.sheet['AA4'].value).strip(),
                                workplace=str(self.sheet['AB4'].value).strip(),
                                address=str(self.sheet['AC4'].value).strip(),
                                position=self.sheet['AD4'].value.strip()),
                           dict(period=str(self.sheet['AA5'].value).strip(),
                                workplace=str(self.sheet['AB5'].value).strip(),
                                address=str(self.sheet['AC5'].value).strip(),
                                position=self.sheet['AD5'].value.strip())]
        self.staff = dict(position=str(self.sheet['C3'].value).strip(),
                          department=str(self.sheet['D3'].value).strip())


# загрузка непостоянных данных из Excel и Json  в БД
def resume_data(cand_id, document, addresses, contacts, workplaces, staff):
    if staff['position']:
        db.session.add(Staff(**staff | {'cand_id': cand_id}))
        db.session.commit()
    if document['number']:
        db.session.add(Document(**document | {'cand_id': cand_id}))
        db.session.commit()
    for address in addresses:
        if address['address']:
            db.session.add(Address(**address | {'cand_id': cand_id}))
            db.session.commit()
    for contact in contacts:
        if contact['contact']:
            db.session.add(Contact(**contact | {'cand_id': cand_id}))
            db.session.commit()
    for work in workplaces:
        if work['workplace']:
            db.session.add(Workplace(**work | {'cand_id': cand_id}))
            db.session.commit()
