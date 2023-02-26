from datetime import datetime

import openpyxl

from app.models.model import *

STATUS = dict(new='1-Новый', active='2-Начато', robot_start='3-Автопроверка', robot_end='4-Предварительно',
              finish='5-Окончено', pfo_start='6-ПФО', result='7-Решение')  # статусы проверки кандидата

BASE_PATH = r'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\Персонал\Персонал-3\\'

TIME_NOW = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class ExcelFile:  # получение анкетной информации из файла Excel
    """ Create class for import data from excel files"""

    def __init__(self, file) -> None:
        self.file = file
        self.wb = openpyxl.load_workbook(self.file, keep_vba=True)
        self.sheet = self.wb.worksheets[0]
        self.resume = dict(full_name=str(self.sheet['K3'].value).title().strip(),
                           last_name=str(self.sheet['S3'].value).strip(),
                           birthday=datetime.strftime(datetime.strptime(str(self.sheet['L3'].value).strip(),
                                                                        '%d.%m.%Y'), '%Y-%m-%d'),
                           birth_place=str(self.sheet['M3'].value).strip(),
                           country=str(self.sheet['T3'].value).strip(),
                           snils=str(self.sheet['U3'].value).strip(),
                           inn=str(self.sheet['V3'].value).strip(),
                           education=str(self.sheet['X3'].value).strip(),
                           status=STATUS['new'],
                           update_date=TIME_NOW)

        self.passport = dict(p_series_passport=str(self.sheet['P3'].value).strip(),
                             p_number_passport=str(self.sheet['Q3'].value).strip(),
                             p_date_given=datetime.strftime(datetime.strptime(str(self.sheet['R3'].value).strip(),
                                                                              '%d.%m.%Y'), '%Y-%m-%d'))

        self.address = [dict(a_type="Адрес регистрации",
                             a_address=str(self.sheet['N3'].value).strip()),
                        dict(a_type="Адрес проживания",
                             a_address=str(self.sheet['O3'].value).strip())]

        self.contact = [dict(c_type=str(self.sheet['Y1'].value).strip(),
                             c_contact=str(self.sheet['Y3'].value).strip()),
                        dict(c_type=str(self.sheet['Z1'].value).strip(),
                             c_contact=str(self.sheet['Z3'].value).strip())]

        self.work = [dict(w_period=str(self.sheet['AA3'].value).strip(),
                          w_work_place=str(self.sheet['AB3'].value).strip(),
                          w_address=str(self.sheet['AC3'].value).strip(),
                          w_staff=self.sheet['AD3'].value.strip()),
                     dict(w_period=str(self.sheet['AA4'].value).strip(),
                          w_work_place=str(self.sheet['AB4'].value).strip(),
                          w_address=str(self.sheet['AC4'].value).strip(),
                          w_staff=self.sheet['AD4'].value.strip()),
                     dict(w_period=str(self.sheet['AA5'].value).strip(),
                          w_work_place=str(self.sheet['AB5'].value).strip(),
                          w_address=str(self.sheet['AC5'].value).strip(),
                          w_staff=self.sheet['AD5'].value.strip())]

        self.staff = dict(s_staff=str(self.sheet['C3'].value).strip(),
                          s_department=str(self.sheet['D3'].value).strip())


def resume_data(cand_id, passport, address, contact, works, staff):  # загрузка вторичных данных из Excel файла в БД
    if staff['s_staff']:
        db.session.add(Staff(**staff | {'staff_id': cand_id}))
        db.session.commit()
    if passport['p_number_passport']:
        db.session.add(Passport(**passport | {'passport_id': cand_id}))
        db.session.commit()
    for addr in address:
        if addr['a_address']:
            db.session.add(Address(**addr | {'address_id': cand_id}))
            db.session.commit()
    for cont in contact:
        if cont['c_contact']:
            db.session.add(Contact(**cont | {'contact_id': cand_id}))
            db.session.commit()
    for place in works:
        if place['w_work_place']:
            db.session.add(Workplace(**place | {'work_place_id': cand_id}))
            db.session.commit()
