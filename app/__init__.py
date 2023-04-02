import os
import logging
from logging.handlers import RotatingFileHandler

from apiflask import APIFlask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS 

from config import DevelopmentConfig, ProductionConfig
from app.models.model import db, ma, User


def create_app():
    app = APIFlask(__name__)
    app.config.from_object(DevelopmentConfig)    # загрузка конфигурации
    CORS(app)
    db.init_app(app)    # инициализация базы данных
    ma.init_app(app)    # инициализация маршаллинга
    login_manager = LoginManager()
    login_manager.login_view = 'route.login'
    login_manager.init_app(app)     # инициализация входа пользователей
    migrate = Migrate()
    migrate.init_app(app, db, render_as_batch=True)     # инициализация миграций
    # импорт и регистрация Blueprints
    from app.routes import bp as route_bp
    app.register_blueprint(route_bp)
    # logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/log.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.WARNING)
    app.logger.info('This is a warning message')

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
