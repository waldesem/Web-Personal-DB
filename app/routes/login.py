from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from . import bp
from ..models.model import db, User
from ..forms.form import LoginForm


@bp.route("/login", methods=["POST", "GET"])  # вход пользователя в систему
def login():  # пароль и логин из таблицы Users прописываются через интерфейс БД
    user_form = LoginForm()
    if current_user.is_authenticated:  # если пользователь уже авторизован, возвращаемся на главную страницу
        return redirect(url_for('route.index'))
    if user_form.validate_on_submit() and request.method == "POST":  # если пользователь не авторизован
        user_form = LoginForm(request.form)  # получаем данные из формы
        username = user_form.username.data
        password = user_form.password.data
        rmb = user_form.remember.data
        user = db.session.query(User).filter_by(username=username).first()  # получаем данные из таблицы Users
        if db.session.query(User).filter_by(username=username, password=password).first():
            login_user(user, remember=rmb)  # если пользователь успешно авторизован возвращаемся на главную страницу
            return redirect(url_for('route.index'))
        else:  # если авторизация не удалась выводим сообщение об ошибке
            flash("Неверная пара логин/пароль", "warning")
    return render_template("login.html", form=user_form, title="Войти в систему")


@bp.route('/logout')
@login_required
def logout():  # выход пользователя из системы
    logout_user()
    return redirect(url_for('route.login'))
