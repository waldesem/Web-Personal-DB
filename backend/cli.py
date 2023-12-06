import asyncio
import bcrypt
import os

from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import Config
from app.models.model import engine, \
    Base, User, Role, Group, Region, Status, Conclusion
from app.models.classes import Roles, Groups, Regions, Statuses, Conclusions 

def register_cli(app):
    @app.cli.command('create')
    def init_default():
        asyncio.run(start_tasks())


async def start_tasks():
    tasks = [
        init_folders(),
        init_models()
    ]
    await asyncio.gather(*tasks)


async def init_folders():
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


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:

        reqions_query = await session.execute(select(Region.region))
        regions = reqions_query.all()
        regions_values = [reg[0] for reg in regions]
        for reg in Regions:
            if reg.value not in regions_values:
                session.add(Region(region=reg.value))

        statuses_query = await session.execute(select(Status.status))
        statuses = statuses_query.all()
        statuses_values = [status[0] for status in statuses]
        for item in Statuses:
            if item.value not in statuses_values:
                session.add(Status(status=item.value))

        conclusion_query = await session.execute(select(Conclusion.conclusion))
        conclusions = conclusion_query.all()
        conclusions_values = [concl[0] for concl in conclusions]
        for item in Conclusions:
            if item.value not in conclusions_values:
                session.add(Conclusion(conclusion=item.value))

        groups_query = await session.execute(select(Group.group))
        groups = groups_query.all()
        groups_values = [gr[0] for gr in groups]
        for grp in Groups:
            if grp.name not in groups_values:
                session.add(Group(group=grp.name))

        roles_query = await session.execute(select(Role.role))
        roles = roles_query.all()
        roles_values = [rl[0] for rl in roles]
        for actor in Roles:
            if actor.value not in roles_values:
                session.add(Role(role=actor.value))

        admin_query = await session.execute(
            select(User)
            .filter_by(username=Roles.admin.name)
        )
        admin = admin_query.one_or_none()
        if not admin:
            new_admin = User(
                fullname='Administrator',
                username='admin',
                password=bcrypt.hashpw('88888888'.encode('utf-8'), 
                                       bcrypt.gensalt()),
                email='admin@admin.admin'
                )

            role_query = await session.execute(
                select(Role)
                .filter_by(role=Roles.admin.value)
            )
            role = role_query.scalar_one_or_none()
            new_admin.roles.append(role)

            group_query = await session.execute(
                select(Group)
                .filter_by(group=Groups.admins.name)
            )
            group = group_query.scalar_one_or_none()
            new_admin.groups.append(group)
            
            session.add(new_admin)
            print('Admin created')

        await session.commit()
