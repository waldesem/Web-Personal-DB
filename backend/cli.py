import bcrypt
import os
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker

from sqlalchemy.sql import select

from config import Config
from app.models.model import User, Role, Group, Region, Status, Conclusion
from app.models.classes import Roles, Groups, Regions, Statuses, Conclusions 

engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))
Session = sessionmaker(engine, expire_on_commit=False)

def register_cli(app):
    @app.cli.command('create')
    def create_default():
        """Create default values"""
        base_path = os.path.join(Config.BASE_PATH)
        if not os.path.isdir(base_path):
            os.mkdir(base_path)
            print('Directory BASE_PATH created')
        
        for letter in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ':
            letter_path = os.path.join(base_path, letter)
            if not os.path.isdir(letter_path):
                os.mkdir(letter_path)
        print(f'Alphabet directories created')
            
        with Session() as session:
            session.create_all()

            regions = session.execute(select(Region.region)).all()
            regions_values = [reg[0] for reg in regions]
            for reg in Regions:
                if reg.value not in regions_values:
                    session.add(Region(region=reg.value))
                    print(f'Region {reg.value} created')

            statuses = session.execute(select(Status.status)).all()
            statuses_values = [status[0] for status in statuses]
            for item in Statuses:
                if item.value not in statuses_values:
                    session.add(Status(status=item.value))
                    print(f'Status {item.value} created')

            conclusions = session.execute(select(Region.region)).all()
            conclusions_values = [concl[0] for concl in conclusions]
            for item in Conclusions:
                if item.value not in conclusions_values:
                    session.add(Conclusion(region=item.value))
                    print(f'Conclusion {item.value} created')

            groups = session.execute(select(Group.group)).all()
            groups_values = [gr[0] for gr in groups]
            for grp in Groups:
                if grp.name not in groups_values:
                    session.add(Group(group=grp.name))
                    print(f'Group {grp.name} created')

            roles = session.execute(select(Role.role)).all()
            roles_values = [rl[0] for rl in roles]
            for actor in Roles:
                if actor.value not in roles_values:
                    session.add(Role(role=actor.value))
                    print(f'Role {actor.value} created')

            if not session.execute(select(User)).\
                    filter_by(username=Roles.admin.name).one_or_none():
                new_admin = User(fullname='Administrator',
                                username='admin',
                                password=bcrypt.hashpw('88888888'.encode('utf-8'), 
                                                        bcrypt.gensalt()),
                                email='admin@admin.admin')
                session.add(new_admin)
                session.flush()
                new_admin.roles.append(session.execute(select(Role)).\
                                            filter_by(role=Roles.admin.value).first())
                new_admin.groups.append(session.execute(select(Group)).\
                                            filter_by(group=Groups.admins.name).first())
                session.add(new_admin)
                print('Admin created')

        session.commit()