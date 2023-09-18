import bcrypt

from app.models.model import db, User, Region, Role, Group
from app.models.classes import Roles, Groups, Regions

def register_command(app):
    @app.cli.command('create')
    def create_default():
        db.create_all()
        regions = db.session.query(Region.region).all()
        for reg in Regions:
            if not reg.value in [rgn[0] for rgn in regions]:
                db.session.add(Region(region=reg.value))
                
        groups = db.session.query(Group.group).all()
        for grp in Groups:
            if not grp.name in [gr[0] for gr in groups]:
                db.session.add(Group(group=grp.name)) 
        
        roles = db.session.query(Role.role).all()
        for actor in Roles:
            if not actor.value in [rl[0] for rl in roles]:
                db.session.add(Role(role=actor.value)) 
        db.session.commit()

        if not db.session.query(User).filter_by(username='admin').one_or_none():  # создание супер администратора:)
            new_admin = User(fullname='Administrator',
                                username=Roles.admin.value,  # admin
                                password=bcrypt.hashpw('administrator'.encode('utf-8'), bcrypt.gensalt()),  # admin
                                region_id=1)
            db.session.add(new_admin)
            db.session.flush()            
            new_admin.roles.append(db.session.query(Role).filter_by(role=Roles.admin.value).first())
            new_admin.groups.append(db.session.query(Group).filter_by(group=Groups.admins.name).first())
            db.session.add(new_admin)
            
        db.session.commit()
