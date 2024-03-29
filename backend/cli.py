import os
from datetime import datetime
import shutil

import bcrypt
from sqlalchemy import select

from config import Config, basedir
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


def register_cli(app):
    @app.cli.command("create")
    def create_default():
        """Create default values"""
        if not os.path.isdir(Config.BASE_PATH):
            os.mkdir(Config.BASE_PATH)
            print("Directory BASE_PATH created")
        shutil.copy(
            os.path.join(basedir, "no-photo.png"),
            os.path.join(Config.NO_PHOTO),
        )

        for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ":
            letter_path = os.path.join(Config.BASE_PATH, letter)
            if not os.path.isdir(letter_path):
                os.mkdir(letter_path)
        print(f"Alphabet directories created")

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
            password=bcrypt.hashpw(
                Config.DEFAULT_PASSWORD.encode("utf-8"), bcrypt.gensalt()
            ),
        )
        db.session.add(superadmin)
        db.session.flush()

        superadmin.roles.append(
            db.session.execute(
                select(Role).filter_by(role=(Roles.admin.value))
            ).scalar_one_or_none()
        )
        db.session.add(superadmin)

        db.session.add(
            Person(
                region_id=Region().get_id(Regions.MAIN_OFFICE.value),
                surname="Бендер".upper(),
                firstname="Остап".upper(),
                patronymic="Ибрагимович".upper(),
                previous="Остап Сулейман",
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
        )

        db.session.commit()

        print("Models created and filled")
