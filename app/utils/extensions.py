from datetime import datetime

import openpyxl

from app.models.model import *


STATUS = dict(new='Новый', active='Начато', robot_start='Автопроверка', robot_end='Предварительно',
              finish='Закончено', pfo_start='ПФО', result='Решение')  # статусы проверки кандидата


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
                           update_date=datetime.now().strftime('%Y-%m-%d %H:%M'))

        self.passport = [dict(series_passport=str(self.sheet['P3'].value).strip(),
                              number_passport=str(self.sheet['Q3'].value).strip(),
                              date_given=datetime.strftime(datetime.strptime(str(self.sheet['R3'].value).strip(),
                                                                             '%d.%m.%Y'), '%Y-%m-%d'))]

        self.address = [dict(type=str(self.sheet['N1':'N2'].value).strip(),
                             address=str(self.sheet['N3'].value).strip()),
                        dict(type=str(self.sheet['O1':'O2'].value).strip(),
                             address=str(self.sheet['O3'].value).strip())]

        self.contact = [dict(type=str(self.sheet['Y1':'Y2'].value).strip(),
                             contact=str(self.sheet['Y3'].value).strip()),
                        dict(type=str(self.sheet['Z1':'Z2'].value).strip(),
                             contact=str(self.sheet['Z3'].value).strip())]

        self.work = [dict(period=str(self.sheet['AA3'].value).strip(),
                          work_place=str(self.sheet['AB3'].value).strip(),
                          address=str(self.sheet['AC3'].value).strip(),
                          staff=self.sheet['AD3'].value.strip()),
                     dict(period=str(self.sheet['AA4'].value).strip(),
                          work_place=str(self.sheet['AB4'].value).strip(),
                          address=str(self.sheet['AC4'].value).strip(),
                          staff=self.sheet['AD4'].value.strip()),
                     dict(period=str(self.sheet['AA5'].value).strip(),
                          work_place=str(self.sheet['AB5'].value).strip(),
                          address=str(self.sheet['AC5'].value).strip(),
                          staff=self.sheet['AD5'].value.strip())]

        self.staff = [dict(staff=str(self.sheet['C3'].value).strip(),
                           department=str(self.sheet['D3'].value).strip())]


def resume_data(result, passports, address, works, contact, staffs, relation=None):
    # загрузка данных из Excel файла в БД кроме основных данных

    for passport in passports:
        if passport['number_passport']:
            passport['passport_id'] = result.id
            passport.pop('csrf_token', None)
            db.session.add(Passport(**passport))  # добавляем анкету в БД
            db.session.commit()

    for addr in address:
        if addr['address']:
            addr['address_id'] = result.id
            addr.pop('csrf_token', None)
            db.session.add(Address(**addr))  # добавляем анкету в БД
            db.session.commit()

    for cont in contact:
        if cont['contact']:
            cont['contact_id'] = result.id
            cont.pop('csrf_token', None)
            db.session.add(Contact(**cont))  # добавляем анкету в БД
            db.session.commit()

    for place in works:
        if place['work_place']:
            place['work_place_id'] = result.id
            place.pop('csrf_token', None)
            db.session.add(Workplace(**place))  # добавляем анкету в БД
            db.session.commit()

    for staff in staffs:
        if staff['staff']:
            staff['staff_id'] = result.id
            staff.pop('csrf_token', None)
            db.session.add(Staff(**staff))  # добавляем анкету в БД
            db.session.commit()

    if relation is not None:
        for rel in relation:
            if rel['full_name']:
                rel['relation_id'] = result.id
                rel.pop('csrf_token', None)
                db.session.add(RelationShip(rel))
                db.session.commit()
