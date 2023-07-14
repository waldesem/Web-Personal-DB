import logging

from apiflask import APIFlask
import bcrypt
from flask_migrate import Migrate
from flask_cors import CORS

from app.models.model import User, Log, Roles, db
from app.models.schema import ma
from app.routes.login import jwt
# from app.scheduler.schedule import scheduler
# from app.tasks.tasker import broker

 
def create_app():
    app = APIFlask(__name__, title="Web-Personal-DB", version="1.0")
    app.config.from_pyfile('env.py')
    app.json.sort_keys = False
    CORS(app, supports_credentials=True)
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db, render_as_batch=True)
    # broker.init_app(app)
    # scheduler.init_app(app)
    # scheduler.start()

    from app.routes import bp as route_bp
    app.register_blueprint(route_bp)

    with app.app_context():
        db.create_all()
        if not db.session.query(User).filter_by(username='admin').one_or_none():
            new_admin = User(fullname='Administrator',
                             username='admin',
                             password=bcrypt.hashpw(b'admin'.encode('utf-8'), bcrypt.gensalt()),
                             role = Roles.admin.value)            
            db.session.add(new_admin)
            db.session.commit()

    def log_to_database(record):
        log_entry = Log(
            timestamp=record.created,
            level=record.levelname,
            message=record.msg,
            pathname=record.pathname,
            lineno=record.lineno
        )
        db.session.add(log_entry)
        db.session.commit()

    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.WARNING)
    app.logger.addFilter(log_to_database)

    return app
