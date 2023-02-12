from datetime import datetime

import openpyxl

from app.models.model import *


class ExcelFile:  # получение анкетной информации из файла Excel
    """ Create class for import data from excel files"""

    resume = None
    last_name = None
    passport = None
    address = None
    work = None
    contact = None
    staff = None

    def __init__(self, file) -> None:
        self.file = file
        self.wb = openpyxl.load_workbook(self.file, keep_vba=True)
        self.sheet = self.wb.worksheets[0]
        self.res = dict(full_name=str(self.sheet['K3'].value).title().strip(),
                        last_name=str(self.sheet['S3'].value).title().strip(),
                        birthday=datetime.strftime(datetime.strptime(str(self.sheet['L3'].value).strip(),
                                                                     '%d.%m.%Y'), '%Y-%m-%d'),
                        birth_place=str(self.sheet['M3'].value).strip(),
                        country=str(self.sheet['T3'].value).strip(),
                        snils=str(self.sheet['U3'].value).strip(),
                        inn=str(self.sheet['V3'].value).strip(),
                        education=str(self.sheet['X3'].value).strip())

        self.pas = dict(series_passport=str(self.sheet['P3 '].value).strip(),
                        number_passport=str(self.sheet['Q3 '].value).strip(),
                        date_given=datetime.strftime(datetime.strptime(str(self.sheet['R3 '].value).strip(),
                                                                       '%d.%m.%Y'), '%Y-%m-%d'))

        self.add = [dict(address=str(self.sheet['N3 '].value).strip()),
                    dict(address=str(self.sheet['O3 '].value).strip())]

        self.ct = [dict(contact=str(self.sheet['Y3 '].value).strip()),
                   dict(contact=str(self.sheet['Z3'].value).strip())]

        self.wk = [dict(period=str(self.sheet['AA3'].value).strip(), workplace=str(self.sheet['AB3'].value).strip(),
                        address=str(self.sheet['AC3'].value).strip(), staff=self.sheet['AD3'].value.strip()),
                   dict(period=str(self.sheet['AA4'].value).strip(), workplace=str(self.sheet['AB4'].value).strip(),
                        address=str(self.sheet['AC4'].value).strip(), staff=self.sheet['AD4'].value.strip()),
                   dict(period=str(self.sheet['AA5'].value).strip(), workplace=str(self.sheet['AB5'].value).strip(),
                        address=str(self.sheet['AC5'].value).strip(), staff=self.sheet['AD5'].value.strip())]

        self.st = [dict(staff=str(self.sheet['C3'].value).strip(), department=str(self.sheet['D3'].value).strip(),
                        recruiter=str(self.sheet['E3'].value).strip())]

        self.ln = [dict(last_name=str(self.sheet['S3'].value).strip)]

        ExcelFile.resume = self.res
        ExcelFile.last_name = self.ln
        ExcelFile.passport = self.pas
        ExcelFile.address = self.add
        ExcelFile.work = self.wk
        ExcelFile.contact = self.ct
        ExcelFile.staff = self.st
        self.wb.close()


def part_excel_data(result):  # загрузка данных из Excel файла в БД кроме основных данных
    if ExcelFile.last_name['last_name'] is not None:
        ExcelFile.last_name['last_name_id'] = result.id
        db.session.add(LastName(**ExcelFile.last_name))  # добавляем предыдущее имя в БД
        db.session.commit()
    if ExcelFile.passport['passport'] is not None:
        ExcelFile.passport['passport_id'] = result.id
        db.session.add(Passport(**ExcelFile.passport))  # добавляем анкету в БД
        db.session.commit()
    for addr in ExcelFile.address:
        if addr['address'] is not None:
            addr['address_id'] = result.id
            db.session.add(Address(**ExcelFile.address[addr]))  # добавляем анкету в БД
            db.session.commit()
    for cont in ExcelFile.contact:
        if cont['contact'] is not None:
            cont['phone_id'] = result.id
            db.session.add(Contact(**ExcelFile.last_name[cont]))  # добавляем анкету в БД
            db.session.commit()
    for place in ExcelFile.work:
        if place['workplace'] is not None:
            place['work_place_id'] = result.id
            db.session.add(Workplace(**ExcelFile.last_name[place]))  # добавляем анкету в БД
            db.session.commit()
    for stf in ExcelFile.staff:
        if stf['staff'] is not None:
            stf['staff_id'] = result.id
            db.session.add(Staff(**ExcelFile.last_name[stf]))  # добавляем анкету в БД
            db.session.commit()


def part_resume_data(result, last_name, passport, address, work, contact, staff, relation):  # загрузка данных вручную
    if last_name.full_name is not None:
        last_name.last_name_id = result.id
        db.session.add(LastName(last_name))
        db.session.commit()
    if passport.number_passport is not None:
        passport.passport_id = result.id
        db.session.add(Passport(passport))
        db.session.commit()
    if address.address is not None:
        address.address_id = result.id
        db.session.add(Address(address))
        db.session.commit()
    if work.orgnization is not None:
        work.work_place_id = result.id
        db.session.add(Workplace(work))
        db.session.commit()
    if contact.contact is not None:
        contact.contact_id = result.id
        db.session.add(Contact(contact))
        db.session.commit()
    if staff.staff is not None:
        staff.staff_id = result.id
        db.session.add(Staff(staff))
        db.session.commit()
    if relation.relation is not None:
        relation.relation_id = result.id
        db.session.add(RelationShip(relation))
        db.session.commit()
