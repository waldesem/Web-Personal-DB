import os
from datetime import datetime

from config import Config


def create_folders(
    person_id, 
    surname, 
    firstname, 
    patronymic, 
    folder_name
):
    """
    Check if a folder exists for a given person and create it if it does not exist.
    """
    person_path = os.path.join(
        surname[0].upper(), 
        f"{person_id}-{surname} {firstname} {patronymic}".rstrip(),
    )

    url = os.path.join(Config.BASE_PATH, person_path)
    if not os.path.isdir(url):
        os.mkdir(url)

    if folder_name == "resume":
        return url

    folder = os.path.join(url, folder_name)
    if not os.path.isdir(folder):
        os.mkdir(folder)

    if folder_name == "image":
        return folder
    
    subfolder = os.path.join(
        folder, 
        datetime.now().strftime("%Y-%m-%d")
    )
    if not os.path.isdir(subfolder):
        os.mkdir(subfolder)

    return subfolder