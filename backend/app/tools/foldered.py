import os
from datetime import datetime

from config import Config


class Folders:

    def __init__(self, region, person_id, surname, firstname, patronymic):
        self.url = os.path.join(
            region,
            Config.BASE_PATH,
            surname[0].upper(),
            f"{person_id}-{surname.upper()} "
            f"{firstname.upper()} "
            f"{patronymic.upper()}".rstrip(),
        )

    @staticmethod
    def _check_url(region, person_id, surname, firstname, patronymic):
        url = os.path.join(
            region,
            Config.BASE_PATH,
            surname[0].upper(),
            f"{person_id}-{surname.upper()} "
            f"{firstname.upper()} "
            f"{patronymic.upper()}".rstrip(),
        )
        if not os.path.isdir(url):
            os.mkdir(url)
        return url

    def create_main_folder(self):
        return self._check_url(self.url)

    def create_parent_folder(self, folder_name):
        parent_folder = os.path.join(self.create_main_folder(), folder_name)
        return self._check_url(parent_folder)

    def create_subfolder(self, parent_folder):
        subfolder = os.path.join(
            self.url,
            self.create_parent_folder(parent_folder),
            datetime.now().strftime("%Y-%m-%d"),
        )
        return self._check_url(subfolder)    

