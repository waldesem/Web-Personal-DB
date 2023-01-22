from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired, Optional


class LoginForm(FlaskForm):
    """ Create form for login page"""

    username = StringField("Логин: ", validators=[InputRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=1, max=20)])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")


class SearchForm(FlaskForm):
    """ Create form for search"""

    full_name = StringField("Полное ФИО: ", validators=[InputRequired()])
    birthday = StringField("ДД-ММ-ГГГ: ", validators=[Optional()])
    submit = SubmitField("Поиск")


class ResumeForm(FlaskForm):
    """ Create form for edit resume page"""

    staff = StringField("Должность", validators=[InputRequired()])
    department = StringField("Кластер/Блок", validators=[Optional()])
    full_name = StringField("Фамилия Имя Отчество", validators=[InputRequired()])
    last_name = StringField("Предыдущие ФИО", validators=[Optional()])
    birthday = StringField("Дата рождения", validators=[InputRequired()])
    birth_place = StringField("Место рождения", validators=[Optional()])
    country = StringField("Гражданство", validators=[Optional()])
    series_passport = StringField("Серия паспорта", validators=[InputRequired()])
    number_passport = StringField("Номер паспорта", validators=[InputRequired()])
    date_given = StringField("Дата выдачи", validators=[Optional()])
    snils = StringField("СНИЛС", validators=[Optional()])
    inn = StringField("ИНН", validators=[Optional(), Length(min=12, max=12)])
    reg_address = TextAreaField("Адрес регистрации", validators=[Optional()])
    live_address = TextAreaField("Адрес проживания", validators=[Optional()])
    phone = StringField("Телефон", validators=[Optional()])
    email = StringField("Email: ", validators=[Optional()])
    education = TextAreaField("Образование", validators=[Optional()])
    submit = SubmitField("Принять изменения")


class CheckForm(FlaskForm):
    """ Create form for page adding check """

    check_work_place = TextAreaField("Проверка по месту работы", validators=[InputRequired()])
    check_passport = TextAreaField("Проверка паспорта", validators=[InputRequired()])
    check_debt = TextAreaField("Проверка задолженностей", validators=[InputRequired()])
    check_bankruptcy = TextAreaField("Проверка банкротства", validators=[InputRequired()])
    check_bki = TextAreaField("Проверка кредитной истории", validators=[InputRequired()])
    check_affiliation = TextAreaField("Проверка аффилированности", validators=[InputRequired()])
    check_internet = TextAreaField("Проверка по открытым источникам", validators=[InputRequired()])
    check_cronos = TextAreaField("Проверка Кронос", validators=[InputRequired()])
    check_cross = TextAreaField("Проверка Крос", validators=[InputRequired()])
    resume = SelectField('Решение', choices=[('Без замечаний', 'Без замечаний'),
                                             ('С комментарием', 'С комментарием'),
                                             ('Отказ', 'Отказ')])
    officer = StringField("Сотрудник СБ", validators=[InputRequired()])
    submit = SubmitField("Принять изменения")


class InquiryForm(FlaskForm):
    """ Create form for page adding inquiry"""

    staff = StringField("Последняя должность", validators=[InputRequired()])
    period = StringField("Период работы", validators=[InputRequired()])
    info = TextAreaField("Информация", validators=[InputRequired()])
    firm = StringField("Инициатор", validators=[InputRequired()])
    submit = SubmitField("Принять")
