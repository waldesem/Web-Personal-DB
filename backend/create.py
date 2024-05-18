import os
import secrets

import click
from config import basedir, settings


@click.command("create")
def create():
    """Create default values"""
    if not os.path.isdir(settings.base_path):
        os.mkdir(settings.base_path)
        print("Directory BASE_PATH created")

    for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ":
        letter_path = os.path.join(settings.base_path, letter)
        if not os.path.isdir(letter_path):
            os.mkdir(letter_path)
    print("Alphabet directories created")

    env = os.path.join(basedir, ".env")
    with open(env, "w", encoding="utf-8") as file:
        file.write(
            f"jwt_secret_key='{secrets.token_hex()}'\n"
            f"sqlalchemy_database_uri = 'postgresql+psycopg2://flask:flask@localhost/personal'"
        )
    print(".env file created")


if __name__ == "__main__":
    create()
