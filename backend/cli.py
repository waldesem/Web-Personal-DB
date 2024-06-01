import os
import secrets

from app.models.classes import Conclusions, Regions, Roles, Statuses
from app.models.model import (
    Base,
    Conclusion,
    Region,
    Role,
    Status,
    User,
    engine,
)
from config import Config
from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash


def register_cli(app):
    @app.cli.command("init")
    def init_env():
        with open(".env", "w", encoding="utf-8") as file:
            file.write(
                f"SECRET_KEY='{secrets.token_hex()}'\n"
                f"JWT_SECRET_KEY='{secrets.token_hex()}'"
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

        with Session(engine) as session:
            Base.metadata.create_all(engine)
            for item in [
                [Region(region=reg.value) for reg in Regions],
                [Status(status=item.value) for item in Statuses],
                [Conclusion(conclusion=item.value) for item in Conclusions],
                [Role(role=actor.value) for actor in Roles],
            ]:
                session.add_all(item)
            session.flush()

            superadmin = User(
                fullname="Администратор",
                username="superadmin",
                password=generate_password_hash(
                    Config.DEFAULT_PASSWORD,
                    method="scrypt",
                    salt_length=16,
                ),
                email="admin@example.com",
                region_id=session.execute(
                    select(Region.id).filter_by(region=Regions.MAIN_OFFICE.value)
                ).scalar_one_or_none(),
            )
            session.add(superadmin)
            superadmin.roles.append(
                session.execute(
                    select(Role).filter_by(role=(Roles.admin.value))
                ).scalar_one_or_none()
            )
            superadmin.roles.append(
                session.execute(
                    select(Role).filter_by(role=(Roles.user.value))
                ).scalar_one_or_none()
            )
            session.add(superadmin)
            session.commit()

            print("Models created and filled")
