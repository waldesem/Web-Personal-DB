import os

import bcrypt
from sqlalchemy import select

from app import db
from config import Config
from app.models.model import User, Region, Role, Group, \
    Status, Conclusion, Category, Risk
from app.models.classes import Roles, Groups, Regions, \
    Statuses, Conclusions, Categories, Risks


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
        
        db.create_all()

        regions = db.session.execute(select(Region.region)).all()
        for reg in Regions:
            if reg.value not in [rgn[0] for rgn in regions]:
                db.session.add(Region(region=reg.value))
                print(f'Region {reg.value} created')

        statuses = db.session.execute(select(Status.status)).all()
        for item in Statuses:
            if item.value not in [stat[0] for stat in statuses]:
                db.session.add(Status(status=item.value))
                print(f'Status {item.value} created')

        conclusion_query = db.session.execute(select(Conclusion.conclusion)).all()
        for item in Conclusions:
            if item.value not in [concl[0] for concl in conclusion_query]:
                db.session.add(Conclusion(conclusion=item.value))
                print(f'Conclusion {item.value} created')

        category_query = db.session.query(Category.category).all()
        for item in Categories:
            if item.value not in [cat[0] for cat in category_query]:
                db.session.add(Category(category=item.value))
                print(f'Category {item.value} created')

        risk_query = db.session.execute(select(Risk.risk)).all()
        for item in Risks:
            if item.value not in [risk[0] for risk in risk_query]:
                db.session.add(Risk(risk=item.value))
                print(f'Risk {item.value} created')
                
        groups = db.session.execute(select(Group.group)).all()
        for grp in Groups:
            if grp.name not in [gr[0] for gr in groups]:
                db.session.add(Group(group=grp.name))
                print(f'Group {grp.name} created')

        roles = db.session.execute(select(Role.role)).all()
        for actor in Roles:
            if actor.value not in [rl[0] for rl in roles]:
                db.session.add(Role(role=actor.value))
                print(f'Role {actor.value} created')

        if not db.session.execute(
            select(User)
            .filter_by(username=Roles.admin.name)
            ).one_or_none():
            new_admin = User(fullname='Administrator',
                             username=Roles.admin.value,
                             password=bcrypt.hashpw('88888888'.encode('utf-8'),
                                                    bcrypt.gensalt()),  # admin
                             email='admin@admin.admin')
            new_admin.roles.append(db.session.query(Role).
                                   filter_by(role=Roles.admin.value).first())
            new_admin.groups.append(db.session.query(Group).
                                    filter_by(group=Groups.admins.name).first())
            db.session.add(new_admin)
            print('Admin created')

        db.session.commit()
        print('Default values created')
        