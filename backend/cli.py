import bcrypt
import os

from app import db
from config import Config
from app.models.model import User, Region, Role, Group
from app.models.classes import Roles, Groups, Regions


def register_cli(app):
    @app.cli.command('create')
    def create_default():

        if not os.path.isdir(os.path.join(Config.BASE_PATH)):
            os.mkdir(os.path.join(Config.BASE_PATH))
            print('Directory BASE_PATH created')

        db.create_all()

        regions = db.session.query(Region.region).all()
        for reg in Regions:
            if reg.value not in [rgn[0] for rgn in regions]:
                db.session.add(Region(region=reg.value))
                print(f'Region {reg.value} created')

        groups = db.session.query(Group.group).all()
        for grp in Groups:
            if grp.name not in [gr[0] for gr in groups]:
                db.session.add(Group(group=grp.name))
                print(f'Group {grp.name} created')

        roles = db.session.query(Role.role).all()
        for actor in Roles:
            if actor.value not in [rl[0] for rl in roles]:
                db.session.add(Role(role=actor.value))
                print(f'Role {actor.value} created')

        if not db.session.query(User).filter_by(username=Roles.admin.name).one_or_none():
            new_admin = User(fullname='Administrator',
                             username=Roles.admin.value,
                             password=bcrypt.hashpw('88888888'.encode('utf-8'),
                                                    bcrypt.gensalt()),  # admin
                             region_id=db.session.query(Region.id).\
                                filter_by(region=Regions.NULL.value).scalar())
            db.session.add(new_admin)
            db.session.flush()
            new_admin.roles.append(db.session.query(Role).
                                   filter_by(role=Roles.admin.value).first())
            new_admin.groups.append(db.session.query(Group).
                                    filter_by(group=Groups.admins.name).first())
            db.session.add(new_admin)
            print('Admin created')

        db.session.commit()
