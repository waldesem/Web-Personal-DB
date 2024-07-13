import os
import sqlite3
import psycopg2

from werkzeug.security import generate_password_hash

from app.classes.classes import Regions
from config import Config


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

    file = (
        open("sqlite.sql", "r", encoding="utf-8")
        if "sqlite" in Config.DATABASE_URI
        else open("psql.sql", "r", encoding="utf-8")
    )
    with file:
        sql = file.read()
        connection = (
            sqlite3.connect(Config.SQLITE_URI)
            if "sqlite" in Config.DATABASE_URI
            else psycopg2.connect(Config.POSTGRE_URI)
        )

        with connection:
            cursor = connection.cursor()
            try:
                if "sqlite" in Config.DATABASE_URI:
                    cursor.executescript(sql)
                else:
                    cursor.execute(sql)
                connection.commit()
                print("Database created")

                cursor.execute(
                    """
                    INSERT INTO users 
                    (fullname, username, passhash, has_admin, region) 
                    VALUES ('Супер Админ', 'superadmin', %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (
                        generate_password_hash(Config.DEFAULT_PASSWORD),
                        True,
                        Regions.main.value,
                    ),
                )
                connection.commit()
                print("Superadmin created")
            except connection.Error as e:
                print(f"Error: {e}")
                connection.rollback()


if __name__ == "__main__":
    init_app()
