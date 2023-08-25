import bcrypt
from apiflask import APIFlask
from flask_migrate import Migrate
from flask_cors import CORS

from .models.model import User, Region, db
from .models.classify import Role, Location
from .models.schema import ma
from .routes.login import jwt


def create_app():
    """
    Initializes and configures a Flask application.
    :return: The Flask application instance.
    """
    app = APIFlask(__name__, title="StaffSec", docs_ui="redoc")  # инициализация APIFlask
    app.config.from_pyfile('../instance/env.py')
    app.json.sort_keys = False  # отключение сортировки поля json
    CORS(app, resources={r"/*": {"origins": "*"}})  # CORS для браузера и APIFlask
    db.init_app(app)  # инициализация БД 
    ma.init_app(app)  # инициализация моделей 
    jwt.init_app(app)  # инициализация JWT 
    migrate = Migrate()  # инициализация миграции 
    migrate.init_app(app, db, render_as_batch=True)

    from app.routes import bp as route_bp
    app.register_blueprint(route_bp)  # регистрация маршрутов 

    with app.app_context():
        db.create_all()  # создание таблиц в БД 
        if not db.session.query(Region).filter_by(region=Location.MAIN_OFFICE.value).first():
            for region in Location:
                db.session.add(Region(region=region.value))  # добавление регионов из списка
        if not db.session.query(User).filter_by(username='admin').one_or_none():  # создание администратора
            new_admin = User(fullname='Administrator',
                             username=Role.admin.value,  # admin
                             password=bcrypt.hashpw(Role.admin.value.encode('utf-8'), bcrypt.gensalt()),  # admin
                             region_id=1,  # Главный офис
                             role=Role.admin.value)
            db.session.add(new_admin)
        db.session.commit()

    return app
