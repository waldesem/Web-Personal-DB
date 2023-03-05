from flask import Flask
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager

from config import Config
from app.models.model import db, ma, User


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)    # загрузка конфигурации
    db.init_app(app)    # инициализация базы данных
    ma.init_app(app)    # инициализация маршаллинга
    login_manager = LoginManager()
    login_manager.login_view = 'route.login'
    login_manager.init_app(app)     # инициализация входа пользователей
    migrate = Migrate()
    migrate.init_app(app, db, render_as_batch=True)     # инициализация миграций
    bootstrap = Bootstrap5()
    bootstrap.init_app(app)    # инициализация Bootstrap
    # импорт и регистрация Blueprints
    from app.main import bpr as route
    app.register_blueprint(route)
    from app.api import bpa as api
    app.register_blueprint(api)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    return app

# for start application in debug mode enter commands in terminal: 
# export FLASK_APP=app
# export FLASK_DEBUG=1
# flask run

# for migrate database enter commands in terminal:
# flask db init - only first time if migration folder is not exist
# flask db migrate
# flask db upgrade
