import click
import os
import secrets

import bcrypt
from sqlmodel import Session, SQLModel, select

from config import settings, basedir
from models.classes import Conclusions, Motivations, Regions, Roles, Statuses
from models.model import (
    Conclusion,
    Motivation,
    Region,
    Role,
    Status,
    User,
    engine,
)

@click.command("initialize")
def initialize():
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

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        for item in [
            [Role(role=actor.value) for actor in Roles],
            [Region(region=reg.value) for reg in Regions],
            [Status(status=item.value) for item in Statuses],
            [Conclusion(conclusion=item.value) for item in Conclusions],
            [Motivation(motivation=item.value) for item in Motivations],
        ]:
            session.add_all(item)
        session.commit()

    with Session(engine) as session:
        superadmin = User(
            fullname="Super Admin",
            username="superadmin",
            email="superadmin@admin.admin",
            region_id=session.exec(
                select(Region.id).filter_by(region=Regions.MAIN_OFFICE.value)
            ).one_or_none(),
            password=bcrypt.hashpw(
                settings.default_password.encode("utf-8"),
                bcrypt.gensalt(),
            ),
        )
        session.add(superadmin)
        superadmin.roles.append(
            session.exec(select(Role).filter_by(role=Roles.admin.value)).one_or_none()
        )
        session.commit()
        print("Database initialized and filled")


if __name__ == "__main__":
    initialize()