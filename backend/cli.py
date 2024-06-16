import os
import secrets

from app.classes.classes import Regions
from app.tools.queries import execute_script, execute
from config import Config
from werkzeug.security import generate_password_hash


def register_cli(app):
    @app.cli.command("init")
    def init_env():
        with open(".env", "w", encoding="utf-8") as file:
            file.write(f"SECRET_KEY='{secrets.token_hex()}'")
        if not os.path.isdir(Config.BASE_PATH):
            os.mkdir(Config.BASE_PATH)
            print("Directory BASE_PATH created")

        for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ":
            letter_path = os.path.join(Config.BASE_PATH, letter)
            if not os.path.isdir(letter_path):
                os.mkdir(letter_path)
        print("Alphabet directories created")

        with open(Config.DATABASE_SQL, "r", encoding="utf-8") as file:
            sql = file.read()
            execute_script(sql)
            execute(
                "INSERT INTO users (fullname, username, password, email, has_admin, region) \
                    VALUES (?, ?, ?, ?, ?, ?)",
                (
                    "Администратор",
                    "superadmin",
                    generate_password_hash(Config.DEFAULT_PASSWORD),
                    "admin@example.ru",
                    1,
                    Regions.main.value,
                ),
            )
            print("Database initialized")
