import os
import secrets
import sqlite3

from app.models.classes import Conclusions, Regions, Roles, Statuses
from config import Config
from werkzeug.security import generate_password_hash


def register_cli(app):
    @app.cli.command("init")
    def init_env():
        with open(".env", "w", encoding="utf-8") as file:
            file.write(
                f"SECRET_KEY='{secrets.token_hex()}'"
            )
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

        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            with open(Config.DATABASE_SQL, "r", encoding="utf-8") as file:
                sql = file.read()
                cursor.executescript(sql)
                cursor.executemany(
                    "INSERT INTO roles (role) VALUES (?)", 
                    [(role.value,) for role in Roles]
                )
                cursor.executemany(
                    "INSERT INTO statuses (status) VALUES (?)",
                    [(status.value,) for status in Statuses],
                )
                cursor.executemany(
                    "INSERT INTO conclusions (conclusion) VALUES (?)",
                    [(conclusion.value,) for conclusion in Conclusions],
                )
                cursor.execute(
                    "INSERT INTO regions (region) VALUES (?)",
                    [(region.value,) for region in Regions],
                )
                conn.commit()

                user = cursor.execute(
                    "INSERT INTO users (fullname, username, password, email, region_id) VALUES (?, ?, ?, ?, ?)",
                    (
                        "Администратор",
                        "superadmin",
                        generate_password_hash(
                            Config.DEFAULT_PASSWORD,
                            method="scrypt",
                            salt_length=16,
                        ),
                        "admin@example",
                        1,
                    ),
                )
                user_id = user.lastrowid
                conn.commit()

                role_admin = cursor.execute(
                    "SELECT * FROM roles WHERE role = 'admin'",
                )
                admin = role_admin.fetchone()
                role_user = cursor.execute(
                    "SELECT * FROM roles WHERE role = 'user'",
                )
                user = role_user.fetchone()
                cursor.execute(
                    "INSERT INTO users_roles (user_id, role_id) VALUES (?, ?)",
                    (user_id, admin[0]),
                )
                cursor.execute(
                    "INSERT INTO users_roles (user_id, role_id) VALUES (?, ?)",
                    (user_id, user[0]),
                )
                conn.commit()

        print("Tables created and filled")
