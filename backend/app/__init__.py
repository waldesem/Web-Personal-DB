import logging

import bcrypt
from apiflask import APIFlask
from flask_migrate import Migrate
from flask_cors import CORS

from .models.model import User, Region, Log, db
from .models.classify import Role
from .models.schema import ma
from .routes.login import jwt
# from .mail.mail import mail
# from app.scheduler.schedule import scheduler
# from app.tasks.tasker import broker

def create_app():
    """
    Initializes and configures a Flask application.
    :return: The Flask application instance.
    """
    app = APIFlask(__name__, title="Web-Personal-DB", docs_ui="redoc")  # инициализация API Flask
    app.config.from_pyfile('../instance/env.py')
    app.json.sort_keys = False  # отключение сортировки поля json
    CORS(app, resources={r"/*": {"origins": "*"}}) # CORS для браузера и API Flask 
    db.init_app(app)  # инициализация БД 
    ma.init_app(app)  # инициализация моделей 
    jwt.init_app(app)  # инициализация JWT 
    migrate = Migrate()  # инициализация миграции 
    migrate.init_app(app, db, render_as_batch=True)
    # mail.init_app(app)
    # broker.init_app(app)
    # scheduler.init_app(app)
    # scheduler.start()

    from app.routes import bp as route_bp
    app.register_blueprint(route_bp)  # регистрация маршрутов 

    with app.app_context():
        db.create_all()  # создание таблиц в БД 
        if not db.session.query(Region).filter_by(region='Главный офис').one_or_none():
            default = Region(region='Главный офис')  # создание региона Главный офис id = 1
            db.session.add(default)
        if not db.session.query(User).filter_by(username='admin').one_or_none():  # создание администратора
            new_admin = User(fullname='Administrator',
                             username= Role.admin.value,  # admin 
                             password=bcrypt.hashpw(Role.admin.value.encode('utf-8'), bcrypt.gensalt()),  # admin
                             region_id = 1,  # Главный офис
                             role = Role.admin.value)            
            db.session.add(new_admin)
        db.session.commit()
    
    class LogFilter(logging.Filter):
        """Фильтр логов для записи в БД"""
        def filter(self, record):
            """
            Add a log record to the database.
            Args:
                record (logging.LogRecord): The log record to be added.
            Returns:
                bool: True if the log record was successfully added to the database, False otherwise.
            """
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
