import os
from datetime import datetime

from config import Config


class Folders:

    """Create folder structure for person

    Args:
        region (str): region
        person_id (str): person id
        surname (str): surname
        firstname (str): firstname
        patronymic (str): patronymic

    Attributes:
        url (str): path to main folder

    """

    def __init__(self, region, person_id, surname, firstname, patronymic):
        self.url = os.path.join(
            Config.BASE_PATH,
            region,
            surname[0].upper(),
            f"{person_id}-{surname.upper()} "
            f"{firstname.upper()} "
            f"{patronymic.upper()}".rstrip(),
        )

    @staticmethod
    def _check_url(url):
        """Check if folder exists and create it if not

        Args:
            url (str): folder path

        Returns:
            str: folder path
        """
        if not os.path.isdir(url):
            os.mkdir(url)
        return url

    def create_main_folder(self):
        """Create main folder for person

        Returns:
            str: path to main folder
        """
        return self._check_url(self.url)

    def create_parent_folder(self, folder_name):
        """Create parent folder for person

        Args:
            folder_name (str): parent folder name

        Returns:
            str: path to parent folder
        """
        parent_folder = os.path.join(self.create_main_folder(), folder_name)
        return self._check_url(parent_folder)

    def create_subfolder(self, parent_folder):
        """Create subfolder for person

        Args:
            parent_folder (str): parent folder name

        Returns:
            str: path to subfolder
        """
        subfolder = os.path.join(
            self.url,
            self.create_parent_folder(parent_folder),
            datetime.now().strftime("%Y-%m-%d"),
        )
        return self._check_url(subfolder)    

