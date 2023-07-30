import logging
import os

from apiflask import APIFlask
import bcrypt
from flask_migrate import Migrate
from flask_cors import CORS

from .models.model import User, Region, Log, db
from .models.classify import BASE_PATH, Role
from .models.schema import ma
from app.routes.login import jwt
# from app.scheduler.schedule import scheduler
# from app.tasks.tasker import broker

def create_app():
    app = APIFlask(__name__, title="Web-Personal-DB", version="1.0", docs_ui="redoc")
    app.config.from_pyfile('env.py')
    app.json.sort_keys = False
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db, render_as_batch=True)
    # broker.init_app(app)
    # scheduler.init_app(app)
    # scheduler.start()

    # def serve_static_file(path, photo):
    #     filepath = os.path.join(BASE_PATH, path, photo)
    #     return app.send_static_file(filepath)
    
    # app.add_url_rule(os.path.join(BASE_PATH, '<path>', '<photo>'), view_func=serve_static_file)

    from app.routes import bp as route_bp
    app.register_blueprint(route_bp)

    with app.app_context():
        db.create_all()
        if not db.session.query(Region).filter_by(region='all').one_or_none():
            default = Region(region='all')
            db.session.add(default)
        if not db.session.query(User).filter_by(username='admin').one_or_none():
            new_admin = User(fullname='Administrator',
                             username= Role.admin.value,
                             password=bcrypt.hashpw(Role.admin.value.encode('utf-8'), bcrypt.gensalt()),
                             region_id = 1,
                             role = Role.admin.value)            
            db.session.add(new_admin)
        db.session.commit()
    
    class LogFilter(logging.Filter):
        def filter(self, record):
            log_entry = Log(timestamp=record.created,
                level=record.levelname,
                message=record.msg,
                pathname=record.pathname,
                lineno=record.lineno)
            db.session.add(log_entry)
            db.session.commit()
            return True

    log_filter = LogFilter()
    app.logger.addFilter(log_filter)
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.WARNING)

    return app
