from flask import Flask
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from config import Config
from app.models.model import db, ma
from app.login.userlogin import login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)    # загрузка конфигурации
    db.init_app(app)    # инициализация базы данных
    ma.init_app(app)    # инициализация маршаллинга 
    login_manager.init_app(app)     # инициализация входа пользователей
    migrate = Migrate()
    migrate.init_app(app, db, render_as_batch=True)     # инициализация миграций
    boootstrap = Bootstrap()
    boootstrap.init_app(app)    # инициализация Bootstrap
    # импорт и регистрация Blueprints
    from app.main import bpr as route
    app.register_blueprint(route)
    from app.main import bpa as api
    app.register_blueprint(api)
    return app

# for start application in debug mode enter commands in terminal: 
# export FLASK_APP=app
# export FLASK_DEBUG=1
# export SECRET_KEY=123
# flask run
