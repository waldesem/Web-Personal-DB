import os
from datetime import datetime
import secrets

from sqlalchemy import select
from werkzeug.security import generate_password_hash

from config import Config
from app.utils.folders import create_folders
from app.models.classes import Roles, Regions, Statuses, Conclusions
from app.models.model import (
    db,
    Person,
    User,
    Region,
    Role,
    Status,
    Conclusion,
)

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://flask:flask@localhost/personal"

def register_cli(app):
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
        print(f"Alphabet directories created")

        with open(".env", "w", encoding="utf-8") as file:
            file.write(
                f"SECRET_KEY='{secrets.token_hex()}'\n" 
                f"JWT_SECRET_KEY='{secrets.token_hex()}'\n" 
                f"SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://flask:flask@localhost/personal'"
            )
        print(".env file created")

        db.create_all()

        for item in [
            [Region(region=reg.value) for reg in Regions],
            [Status(status=item.value) for item in Statuses],
            [Conclusion(conclusion=item.value) for item in Conclusions],
            [Role(role=actor.value) for actor in Roles],
        ]:
            db.session.add_all(item)
        db.session.flush()

        superadmin = User(
            fullname="Администратор",
            username="superadmin",
            password=generate_password_hash(
                Config.DEFAULT_PASSWORD,
                method="scrypt",
                salt_length=16,
            ),
        )
        db.session.add(superadmin)
        db.session.flush()

        superadmin.roles.append(
            db.session.execute(
                select(Role).filter_by(role=(Roles.admin.value))
            ).scalar_one_or_none()
        )
        superadmin.roles.append(
            db.session.execute(
                select(Role).filter_by(role=(Roles.user.value))
            ).scalar_one_or_none()
        )
        db.session.add(superadmin)

        candidate = Person(
            region_id=Region().get_id(Regions.MAIN_OFFICE.value),
            surname="Бендер".upper(),
            firstname="Остап".upper(),
            patronymic="Ибрагимович".upper(),
            birthday=datetime.now().date(),
            birthplace="Неизвестно",
            country="Россия",
            ext_country="Турция",
            snils="12345678901",
            inn="123456789012",
            education="Частная гимназия Илиади",
            marital="женат",
            addition="великий комбинатор",
            status_id=Status().get_id(Statuses.new.value),
        )
        db.session.add(candidate)
        db.session.flush()

        path = create_folders(
            candidate.id,
            candidate.surname,
            candidate.firstname,
            candidate.patronymic,
            "resume",
        )
        candidate.path = path

        db.session.commit()
        print("Models created and filled")
