import os
from datetime import datetime

import bcrypt
from sqlalchemy import select

from app import db
from config import Config
from app.models.classes import Roles, Groups, Regions, Statuses, Conclusions, Categories
from app.models.model import (
    Person,
    User,
    Region,
    Role,
    Group,
    Status,
    Conclusion,
    Category,
)


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

        db.drop_all()
        db.create_all()

        db.session.add_all([Region(region=reg.value) for reg in Regions])
        db.session.add_all([Status(status=item.value) for item in Statuses])
        db.session.add_all([Conclusion(conclusion=item.value) for item in Conclusions])
        db.session.add_all([Category(category=item.value) for item in Categories])
        db.session.add_all([Group(group=grp.value) for grp in Groups])
        db.session.add_all([Role(role=actor.value) for actor in Roles])

        db.session.flush()

        superadmin = User(
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
        superadmin.groups.append(
            db.session.execute(
                select(Group).filter_by(group=(Groups.admins.value))
            ).scalar_one_or_none()
        )
        db.session.add(superadmin)

        db.session.add(
            Person(
                category_id=Category().get_id(Categories.candidate.value),
                region_id=Region().get_id(Regions.MAIN_OFFICE.value),
                fullname="Бендер Остап Ибрагимович",
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
                path=Config.BASE_PATH,
                status_id=Status().get_id(Statuses.new.value),
            )
        )

        db.session.commit()

        print("Models created and filled")
