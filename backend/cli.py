import os

import bcrypt
from sqlalchemy import select

from app import db
from config import Config
from app.models.model import User, Region, Role, Group, \
    Status, Conclusion, Category
from app.models.classes import Roles, Groups, Regions, \
    Statuses, Conclusions, Categories


def register_cli(app):
    @app.cli.command('create')
    def create_default():
        """Create default values"""
        base_path = os.path.join(Config.BASE_PATH)
        if not os.path.isdir(base_path):
            os.mkdir(base_path)
            print('Directory BASE_PATH created')
        
        for letter in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ':
            letter_path = os.path.join(Config.BASE_PATH, letter)
            if not os.path.isdir(letter_path):
                os.mkdir(letter_path)
        print(f'Alphabet directories created')
        
        db.drop_all()
        db.create_all()

        db.session.add_all([Region(region=reg.value) for reg in Regions])
        db.session.add_all([Status(status=item.value) for item in Statuses])
        db.session.add_all([Conclusion(conclusion=item.value) for item in Conclusions])
        db.session.add_all([Category(category=item.value) for item in Categories])
        db.session.add_all([Group(group=grp.name) for grp in Groups])
        db.session.add_all([Role(role=actor.value) for actor in Roles])

        db.session.flush()

        superadmin = User(fullname='Administrator',
                            username=Roles.superadmin.value,
                            password=bcrypt.hashpw('88888888'.encode('utf-8'),
                                                bcrypt.gensalt()),
                            email='admin@admin.admin')
        
        db.session.add(superadmin)
        db.session.flush()

        superadmin.roles.append(Role().get_role(Roles.superadmin.value))
        superadmin.groups.append(Group().get_group(Groups.admins.name))
        db.session.add(superadmin)

        db.session.commit()
        print('Default values created')
        