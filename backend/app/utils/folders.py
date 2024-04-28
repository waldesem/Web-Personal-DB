import os
from datetime import datetime

from config import Config


class Folders:

    def __init__(self, person_id, surname, firstname, patronymic):
        self.url = os.path.join(
            Config.BASE_PATH,
            surname[0].upper(),
            f"{person_id}-{surname.upper()} "
            f"{firstname.upper()} "
            f"{patronymic.upper()}".rstrip(),
        )

    @staticmethod
    def _check_url(url):
        if not os.path.isdir(url):
            os.mkdir(url)

    def create_main_folder(self):
        self._check_url(self.url)
        return self.url

    def create_parent_folder(self, folder_name):
        parent_folder = os.path.join(self.create_main_folder(), folder_name)
        self._check_url(parent_folder)
        return parent_folder

    def create_subfolder(self, parent_folder):
        subfolder = os.path.join(
            self.url,
            self.create_parent_folder(parent_folder),
            datetime.now().strftime("%Y-%m-%d"),
        )
        self._check_url(subfolder)
        return subfolder
