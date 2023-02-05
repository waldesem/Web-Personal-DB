from datetime import datetime

import openpyxl

from app.models.model import Candidate


class ExcelFile:  # получение анкетной информации из файла Excel
    """ Create class for import data from excel files"""

    res = {}

    def __init__(self, file) -> None:
        self.file = file
        self.wb = openpyxl.load_workbook(self.file, keep_vba=True)
        self.sheet = self.wb.worksheets[0]
        self.res = Candidate(full_name=str(self.sheet['K3'].value).title().strip(),
                             last_name=str(self.sheet['S3'].value).title().strip(),
                             birthday=datetime.strftime(datetime.strptime(str(self.sheet['L3'].value).strip(),
                                                                          '%d.%m.%Y'), '%Y-%m-%d'),
                             birth_place=str(self.sheet['M3'].value).strip(),
                             country=str(self.sheet['T3'].value).strip(),
                             series_passport=str(self.sheet['P3'].value).strip(),
                             number_passport=str(self.sheet['Q3'].value).strip(),
                             date_given=datetime.strftime(datetime.strptime(str(self.sheet['R3'].value).strip(),
                                                                            '%d.%m.%Y'), '%Y-%m-%d'),
                             snils=str(self.sheet['U3'].value).strip(),
                             inn=str(self.sheet['V3'].value).strip(),
                             reg_address=str(self.sheet['N3'].value).strip(),
                             live_address=str(self.sheet['O3'].value).strip(),
                             phone=str(self.sheet['Y3'].value).strip(),
                             email=str(self.sheet['Z3'].value).strip(),
                             education=str(self.sheet['X3'].value).strip(),
                             workplace_1=f"{str(self.sheet['AA3'].value).strip()} - "
                                         f"{str(self.sheet['AB3'].value).strip()} - "
                                         f"{str(self.sheet['AD3'].value).strip()}",
                             workplace_2=f"{str(self.sheet['AA4'].value).strip()} - "
                                         f"{str(self.sheet['AB4'].value).strip()} - "
                                         f"{str(self.sheet['AD4'].value).strip()}",
                             workplace_3=f"{str(self.sheet['AA5'].value).strip()} - "
                                         f"{str(self.sheet['AB5'].value).strip()} - "
                                         f"{str(self.sheet['AD5'].value).strip()}"
                             )
        ExcelFile.res = self.res
        self.wb.close()
