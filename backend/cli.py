import bcrypt
import os

from config import Config
from app.models.model import async_session,  User, Role, Group, Region, Status, Conclusion
from app.models.classes import Roles, Groups, Regions, Statuses, Conclusions 


async def register_cli(app):
    @app.cli.command('create')
    async def create_default():
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
        
        async_session.create_all()
        
        async with async_session() as session:
            regions = await session.execute(Region.region).all()
            for reg in Regions:
                if reg.value not in [rgn[0] for rgn in regions]:
                    session.add(Region(region=reg.value))
                    print(f'Region {reg.value} created')

        async with async_session() as session:
            statuses = await session.execute(Status.status).all()
            for item in Statuses:
                if item.value not in [status[0] for status in statuses]:
                    session.add(Status(status=item.value))
                    print(f'Status {item.value} created')

        async with async_session() as session:
            conclusions = await session.execute(Region.region).all()
            for item in Conclusions:
                if item.value not in [concl[0] for concl in conclusions]:
                    session.add(Conclusion(region=item.value))
                    print(f'Conclusion {item.value} created')

        async with async_session() as session:
            groups = await session.execute(Group.group).all()
            for grp in Groups:
                if grp.name not in [gr[0] for gr in groups]:
                    session.add(Group(group=grp.name))
                    print(f'Group {grp.name} created')

        async with async_session() as session:
            roles = await session.execute(Role.role).all()
            for actor in Roles:
                if actor.value not in [rl[0] for rl in roles]:
                    session.add(Role(role=actor.value))
                    print(f'Role {actor.value} created')

        async with async_session() as session:
            if not session.execute(User).filter_by(username=Roles.admin.name).one_or_none():
                new_admin = User(fullname='Administrator',
                                username=Roles.admin.value,
                                password=bcrypt.hashpw('88888888'.encode('utf-8'),
                                                        bcrypt.gensalt()),  # admin
                                email='admin@admin.admin')
                session.add(new_admin)
                session.flush()
                new_admin.roles.append(session.execute(Role).
                                    filter_by(role=Roles.admin.value).first())
                new_admin.groups.append(session.execute(Group).
                                        filter_by(group=Groups.admins.name).first())
                session.add(new_admin)
                print('Admin created')

        await session.commit()