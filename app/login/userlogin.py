from flask_login import LoginManager

from app.models.model import db, Users


login_manager = LoginManager()
login_manager.login_view = 'route.login'
login_manager.login_message = "Авторизуйтесь для доступа к базе данных"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    user = db.session.query(Users).filter_by(id=user_id).first()
    return user
