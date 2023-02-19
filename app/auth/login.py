from flask_login import LoginManager

from app.models.model import Users

login_manager = LoginManager()
login_manager.login_view = 'route.login'
login_manager.login_message = "Авторизуйтесь для доступа к базе данных"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
