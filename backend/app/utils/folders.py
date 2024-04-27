import os
from datetime import datetime

from config import Config


class Folders:

    def __init__(self, person_id, surname, firstname, patronymic):
        self.url = os.path.join(
            Config.BASE_PATH,
            surname[0].upper(),
            f"{person_id}-{surname.upper()} {firstname.upper()} {patronymic.upper()}".rstrip(),
        )

    def create_main_folder(self):
        if not os.path.isdir(self.url):
            os.mkdir(self.url)
        return self.url

    def create_parent_folder(self, folder_name):
        parent_folder = os.path.join(self.url, folder_name)
        if not os.path.isdir(parent_folder):
            os.mkdir(parent_folder)
        return parent_folder

    def create_subfolder(self, parent_folder):
        subfolder = os.path.join(
            self.url, parent_folder, datetime.now().strftime("%Y-%m-%d")
        )
        if not os.path.isdir(subfolder):
            os.mkdir(subfolder)
        return subfolder
