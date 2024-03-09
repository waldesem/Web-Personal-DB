import os
from datetime import datetime

from config import Config


def create_folders(person_id, fullname, folder_name):
    """
    Check if a folder exists for a given person and create it if it does not exist.
    """
    person_path = os.path.join(fullname[0].upper(), f"{person_id}-{fullname}")
    url = os.path.join(Config.BASE_PATH, person_path)
    if not os.path.isdir(url):
        os.mkdir(url)

    folder = os.path.join(url, folder_name)
    if not os.path.isdir(folder):
        os.mkdir(folder)
    if folder_name == "image":
        return url
    
    subfolder = os.path.join(folder, datetime.now().strftime("%Y-%m-%d"))
    if not os.path.isdir(subfolder):
        os.mkdir(subfolder)
    return os.path.join(
        fullname[0].upper(), f"{person_id}-{fullname}", folder, subfolder
    )