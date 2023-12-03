import bcrypt
import os

from sqlalchemy.sql import select

from config import Config
from app.models.model import async_session, User, Role, Group, Region, Status, Conclusion
from app.models.classes import Roles, Groups, Regions, Statuses, Conclusions 


def register_cli(app):
    @app.cli.command('create')
    async def create_default():
        """Create default values"""
        # base_path = os.path.join(Config.BASE_PATH)
        # if not os.path.isdir(base_path):
        #     os.mkdir(base_path)
        #     print('Directory BASE_PATH created')
        
        # for letter in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ':
        #     letter_path = os.path.join(base_path, letter)
        #     if not os.path.isdir(letter_path):
        #         os.mkdir(letter_path)
        # print(f'Alphabet directories created')
            
        async with async_session() as session:
            session.create_all()

            regions = await session.execute(select(Region.region)).all()
            regions_values = [reg[0] for reg in regions]
            for reg in Regions:
                if reg.value not in regions_values:
                    await session.add(Region(region=reg.value))
                    print(f'Region {reg.value} created')

            statuses = await session.execute(select(Status.status)).all()
            statuses_values = [status[0] for status in statuses]
            for item in Statuses:
                if item.value not in statuses_values:
                    await session.add(Status(status=item.value))
                    print(f'Status {item.value} created')

            conclusions = await session.execute(select(Region.region)).all()
            conclusions_values = [concl[0] for concl in conclusions]
            for item in Conclusions:
                if item.value not in conclusions_values:
                    await session.add(Conclusion(region=item.value))
                    print(f'Conclusion {item.value} created')

            groups = await session.execute(select(Group.group)).all()
            groups_values = [gr[0] for gr in groups]
            for grp in Groups:
                if grp.name not in groups_values:
                    await session.add(Group(group=grp.name))
                    print(f'Group {grp.name} created')

            roles = await session.execute(select(Role.role)).all()
            roles_values = [rl[0] for rl in roles]
            for actor in Roles:
                if actor.value not in roles_values:
                    await session.add(Role(role=actor.value))
                    print(f'Role {actor.value} created')

            if not await session.execute(select(User)).\
                    filter_by(username=Roles.admin.name).one_or_none():
                new_admin = User(fullname='Administrator',
                                username='admin',
                                password=bcrypt.hashpw('88888888'.encode('utf-8'), 
                                                        bcrypt.gensalt()),
                                email='admin@admin.admin')
                await session.add(new_admin)
                await session.flush()
                await new_admin.roles.append(session.execute(select(Role)).\
                                            filter_by(role=Roles.admin.value).first())
                await new_admin.groups.append(session.execute(select(Group)).\
                                            filter_by(group=Groups.admins.name).first())
                await session.add(new_admin)
                print('Admin created')

        await session.commit()
