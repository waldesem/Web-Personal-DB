import logging
import bcrypt
from datetime import datetime

from apiflask import APIFlask
from flask_migrate import Migrate
from flask_cors import CORS

from app.models.model import User, Log, db, ma
from app.routes.login import jwt
from app.utils.schedule import scheduler
from app.utils.check import broker

 
def create_app():
    """
    Initializes and returns an APIFlask app object with various extensions and configurations.
    Returns:
        app (APIFlask): An APIFlask app object.
    """
    app = APIFlask(__name__, title="Web-Personal-DB", version="1.0")
    app.config.from_pyfile('env.py')
    app.json.sort_keys = False
    CORS(app, supports_credentials=True)
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db, render_as_batch=True)
    broker.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    from app.routes import bp as route_bp
    app.register_blueprint(route_bp)

    with app.app_context():
        db.create_all()
        admin_user = db.session.query(User).filter_by(username='admin').first()
        if not admin_user:
            new_admin = User(fullname='Administrator',
                             username='admin',
                             pswd_create=datetime.now(),
                             password=bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt()),
                             role = 'admin')            
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
