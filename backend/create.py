import os
import click
import secrets

from config import Config, basedir


@click.command("create")
def create():
    """Create default values"""
    if not os.path.isdir(Config.BASE_PATH):
        os.mkdir(Config.BASE_PATH)
        print("Directory BASE_PATH created")

    for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ":
        letter_path = os.path.join(Config.BASE_PATH, letter)
        if not os.path.isdir(letter_path):
            os.mkdir(letter_path)
    print(f"Alphabet directories created")

    env = os.path.join(basedir, ".env")
    with open(env, "w", encoding="utf-8") as file:
        file.write(
            f"SECRET_KEY='{secrets.token_hex()}'\n" 
            f"JWT_SECRET_KEY='{secrets.token_hex()}'\n" 
            f"SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://flask:flask@localhost/personal'"
        )
    print(".env file created")


if __name__ == "__main__":
    create()