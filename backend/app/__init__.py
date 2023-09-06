import bcrypt
from apiflask import APIFlask
from flask_migrate import Migrate
from flask_cors import CORS

from .models.model import User, Region, Role, Group, db
from .models.classes import Roles, Groups, Regions
from .models.schema import  ma
from .routes.login import jwt


def create_app():
    """
    Initializes and configures a Flask application.
    :return: The Flask application instance.
    """
    app = APIFlask(__name__, title="StaffSec", docs_ui="redoc")
    app.config.from_pyfile('../instance/env.py')
    app.json.sort_keys = False
    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db, render_as_batch=True)

    from app.routes import bp as route_bp
    app.register_blueprint(route_bp)

    with app.app_context():    # create DB tables and default values
        db.create_all()  
        
        regions = db.session.query(Region.region).all()
        for reg in Regions:
            if not reg.value in [rgn[0] for rgn in regions]:
                db.session.add(Region(region=reg.value))
                
        groups = db.session.query(Group.group).all()
        for grp in Groups:
            if not grp.value in [gr[0] for gr in groups]:
                db.session.add(Group(group=grp.value)) 
        
        roles = db.session.query(Role.role).all()
        for actor in Roles:
            if not actor.value in [rl[0] for rl in roles]:
                db.session.add(Role(role=actor.value)) 
        db.session.commit()

        if not db.session.query(User).filter_by(username='admin').one_or_none():  # создание супер администратора:)
            new_admin = User(fullname='Administrator',
                             username=Roles.admin.value,  # admin
                             password=bcrypt.hashpw(Roles.admin.value.encode('utf-8'), bcrypt.gensalt()),  # admin
                             region_id=1)
            db.session.add(new_admin)
            db.session.flush()            
            new_admin.roles.append(db.session.query(Role).filter_by(role=Roles.admin.value).first())
            new_admin.groups.append(db.session.query(Group).filter_by(group=Groups.staffsec.value).first())
            new_admin.groups.append(db.session.query(Group).filter_by(group=Groups.creditsec.value).first())
            db.session.add(new_admin)
            
        db.session.commit()

    return app
