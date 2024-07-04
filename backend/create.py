import os

from app.classes.classes import Regions
from app.databases.database import execute, scriptexec
from config import Config
from werkzeug.security import generate_password_hash


def init_app():
    if not os.path.isdir(Config.BASE_PATH):
        os.mkdir(Config.BASE_PATH)
    for region in Regions:
        region_path = os.path.join(Config.BASE_PATH, region.value)
        if not os.path.isdir(region_path):
            os.mkdir(region_path)
        for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ":
            letter_path = os.path.join(region_path, letter)
            if not os.path.isdir(letter_path):
                os.mkdir(letter_path)
    print("Default directories created")

    with open(Config.DATABASE_SQL, "r", encoding="utf-8") as file:
        sql = file.read()
        scriptexec(sql)
        execute(
            """INSERT OR REPLACE INTO users 
            (fullname, username, passhash, has_admin, region) 
            VALUES ('Супер Админ', 'superadmin', ?, '1', ?)""", (
                generate_password_hash(Config.DEFAULT_PASSWORD), Regions.main.value,
            )
        )
        print("Database initialized")

if __name__ == "__main__":
    init_app()