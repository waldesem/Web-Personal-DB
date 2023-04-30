from flask import request
from flask_login import login_user, logout_user, current_user
from apiflask.views import MethodView

from . import bp
from ..models.model import User, db


class Login(MethodView):

    def get(self):
        if current_user.is_authenticated:  # если пользователь уже авторизован
            return {"user": current_user.username}
        else:
            return {"user": "None"}

    def post(self):
        user_form = request.form.to_dict()  # получаем данные из формы
        username = user_form['username']
        user = db.session.query(User).filter_by(username=username).first()  # получаем данные из Users
        if db.session.query(User).filter_by(username=username, password=user_form['password']).first():
            login_user(user, remember=bool(user_form['remember']))  # если авторизован - переход на главную страницу
            return {"user": current_user.username}
        else:
            return {"user": "None"}  # если авторизация не удалась выводим сообщение


@bp.get('/logout')
def logout():  # выход пользователя из системы
    logout_user()
    return {"user": "None"}


bp.add_url_rule('/login', view_func=Login.as_view('login'))
