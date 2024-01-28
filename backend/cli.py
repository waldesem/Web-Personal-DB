from datetime import datetime
import os
import bcrypt

from app import db
from config import Config
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
from app.models.classes import Roles, Groups, Regions, Statuses, Conclusions, Categories


def register_cli(app):
    @app.cli.command("create")
    def create_default():
        """Create default values"""
        base_path = os.path.join(Config.BASE_PATH)
        if not os.path.isdir(base_path):
            os.mkdir(base_path)
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

        superadmin.roles.append(Role().get_role(Roles.admin.value))
        superadmin.groups.append(Group().get_group(Groups.admins.value))
        db.session.add(superadmin)

        db.session.add(
            Person(
                category_id=Category().get_id(Categories.candidate.value),
                region_id=Region().get_id(Regions.MAIN_OFFICE.value),
                fullname="Бендер Остап Сулеман",
                previous="Ильф и Петров",
                birthday=datetime.now().date() - 100,
                birthplace="г.Нью-Васюки",
                country="Россия",
                ext_country="Турция",
                snils="12345678901",
                inn="123456789012",
                education="Университет Джордано Бруно",
                marital="не женат",
                addition="Холодный философ и свободный художник",
                path=Config.BASE_PATH,
                status_id=Status().get_id(Statuses.new.value),
            )
        )

        db.session.commit()

        print("Models created and filled")
