from flask import request, jsonify, render_template
from flask_login import login_user, logout_user, current_user


from . import bp
from ..models.model import User, db


@bp.route("/login", methods=["POST", "GET"])  # вход пользователя в систему
def login():  # пароль и логин из таблицы Users прописываются через интерфейс БД
    if request.method == 'GET':
        if current_user.is_authenticated:  # если пользователь уже авторизован
            return jsonify(data={"user":current_user.username})
        else:
            return jsonify(data={"user":"None"})
    if request.method == 'POST':
        user_form = request.form.to_dict() # получаем данные из формы
        username = user_form['username']
        password = user_form['password']
        rmb = bool(user_form['remember'])
        user = db.session.query(User).filter_by(username=username).first()  # получаем данные из таблицы Users
        if db.session.query(User).filter_by(username=username, password=password).first():
            login_user(user, remember=rmb)  # если пользователь авторизован возвращаемся на главную страницу
            return jsonify(data={"user":current_user.username})
        else:  # если авторизация не удалась выводим сообщение об ошибке
            return jsonify(data={"user":"None"})


@bp.route('/logout')
def logout():  # выход пользователя из системы
    print('logout')
    logout_user()
    return jsonify(data={"user":"None"})
