from datetime import datetime
import os
import secrets

from app.tools.classes import Conclusions, Regions, Roles, Statuses
from app.tools.queries import execute_script, execute, select_single
from config import Config
from werkzeug.security import generate_password_hash


def register_cli(app):
    @app.cli.command("init")
    def init_env():
        with open(".env", "w", encoding="utf-8") as file:
            file.write(f"SECRET_KEY='{secrets.token_hex()}'")
            print(".env file created")

    @app.cli.command("create")
    def create_default():
        """Create default values"""
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
            for query in [
                (
                    "INSERT INTO roles (prefix, role) VALUES (?, ?)",
                    [
                        (
                            role.name,
                            role.value,
                        )
                        for role in Roles
                    ],
                ),
                (
                    "INSERT INTO statuses (prefix, status) VALUES (?, ?)",
                    [
                        (
                            status.name,
                            status.value,
                        )
                        for status in Statuses
                    ],
                ),
                (
                    "INSERT INTO conclusions (prefix, conclusion) VALUES (?, ?)",
                    [
                        (
                            conclusion.name,
                            conclusion.value,
                        )
                        for conclusion in Conclusions
                    ],
                ),
                (
                    "INSERT INTO regions (prefix, region) VALUES (?, ?)",
                    [
                        (
                            region.name,
                            region.value,
                        )
                        for region in Regions
                    ],
                ),
            ]:
                execute(*query)

            user_id = execute(
                "INSERT INTO users (fullname, username, password, email, \
                    pswd_create, change_pswd, last_login, blocked, deleted, \
                        attempt, created, updated, region_id) \
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    "Администратор",
                    "superadmin",
                    generate_password_hash(
                        Config.DEFAULT_PASSWORD,
                        method="scrypt",
                        salt_length=16,
                    ),
                    "admin@example",
                    datetime.now(),
                    False,
                    None,
                    0,
                    0,
                    0,
                    datetime.now(),
                    None,
                    1,
                ),
            )

            admin = select_single(
                "SELECT * FROM roles WHERE role = 'admin'",
            )
            user = select_single(
                "SELECT * FROM roles WHERE role = 'user'",
            )
            execute(
                "INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)",
                [
                    (user_id, admin["id"]),
                    (user_id, user[0]),
                ],
            )

        print("Tables created and filled")
