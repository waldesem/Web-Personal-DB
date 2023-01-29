import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField, SelectField, DateField
from wtforms.validators import DataRequired, Length, InputRequired, Optional

current_year = datetime.date.today().year


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

    full_name = StringField("Фамилия Имя Отчество", validators=[InputRequired()])
    last_name = StringField("Предыдущие ФИО", validators=[Optional()])
    birthday = DateField("Дата рождения", format='%d-%m-%Y', validators=[InputRequired()])
    birth_place = StringField("Место рождения", validators=[Optional()])
    country = StringField("Гражданство", validators=[Optional()])
    series_passport = StringField("Серия паспорта", validators=[Optional()])
    number_passport = StringField("Номер паспорта", validators=[Optional()])
    agency = StringField("Орган выдавший", validators=[Optional()])
    date_given = DateField("Дата выдачи", format='%d-%m-%Y', validators=[Optional()])
    snils = StringField("СНИЛС", validators=[Optional()])
    inn = StringField("ИНН", validators=[Optional(), Length(min=12, max=12)])
    reg_address = TextAreaField("Адрес регистрации", validators=[Optional()])
    live_address = TextAreaField("Адрес проживания", validators=[Optional()])
    phone = StringField("Телефон", validators=[Optional()])
    email = StringField("Email: ", validators=[Optional()])
    education = TextAreaField("Образование", validators=[Optional()])
    addition = TextAreaField("Дополнительная информация", validators=[Optional()])
    update_date = DateField("Дата обновления", format='%d-%m-%Y', validators=[Optional()])
    status = StringField("Статус", validators=[Optional()])
    submit = SubmitField("Принять изменения")


class CheckForm(FlaskForm):
    """ Create form for page adding check """

    staff = StringField("Должность", validators=[Optional()])
    department = StringField("Кластер/Блок", validators=[Optional()])
    check_work_place = TextAreaField("Проверка по месту работы", validators=[Optional()])
    check_passport = TextAreaField("Проверка паспорта", validators=[Optional()])
    check_debt = TextAreaField("Проверка задолженностей", validators=[Optional()])
    check_bankruptcy = TextAreaField("Проверка банкротства", validators=[Optional()])
    check_bki = TextAreaField("Проверка кредитной истории", validators=[Optional()])
    check_affiliation = TextAreaField("Проверка аффилированности", validators=[Optional()])
    check_terrorist = TextAreaField("Проверка списка террористов", validators=[Optional()])
    check_internet = TextAreaField("Проверка по открытым источникам", validators=[Optional()])
    check_cronos = TextAreaField("Проверка Кронос", validators=[Optional()])
    check_cross = TextAreaField("Проверка Крос", validators=[Optional()])
    check_addition = TextAreaField("Дополнительная информация", validators=[Optional()])
    pfo = BooleanField("Полиграф", default=False)
    resume = SelectField('Решение', choices=['Без замечаний', 'С комментарием', 'Отказ'])
    officer = StringField("Сотрудник СБ", validators=[Optional()])
    date_check = DateField("Дата проверки", format='%d-%m-%Y', validators=[Optional()])
    url = StringField("Материалы проверки", validators=[Optional()])
    submit = SubmitField("Принять изменения")


class PoligrafForm(FlaskForm):
    """ Create form for page adding poligraf"""

    info = StringField("Информация", validators=[Optional()])
    date_pfo = DateField("Дата проведения", validators=[Optional()])
    officer = StringField("Сотрудник СБ", validators=[Optional()])
    submit = SubmitField("Принять")


class InvestigationForm(FlaskForm):
    """ Create form for page adding investigation"""

    info = StringField("Информация", validators=[Optional()])
    source = DateField("Источник", validators=[Optional()])
    date_inv = DateField("Дата проверки", validators=[Optional()])
    submit = SubmitField("Принять")


class InquiryForm(FlaskForm):
    """ Create form for page adding inquiry"""

    staff = StringField("Последняя должность", validators=[Optional()])
    period = StringField("Период работы", validators=[Optional()])
    info = TextAreaField("Информация", validators=[Optional()])
    firm = StringField("Инициатор", validators=[Optional()])
    submit = SubmitField("Принять")


class RegistrForm(FlaskForm):
    """ Create form for page registry check"""

    supervisor = StringField("Руководитель", validators=[Optional()])
    checks = TextAreaField("Комментарий", validators=[Optional()])
    fin_decision = SelectField('Решение', choices=['Без замечаний', 'С комментарием', 'Отказ'])
    final_date = DateField("Дата проверки", format='%d-%m-%Y', validators=[Optional()])
    submit = SubmitField("Принять")


class InfoForm(FlaskForm):
    """ Create form for statistic information"""

    year = SelectField('Год', choices=[str(current_year - 2),
                                       str(current_year - 1),
                                       str(current_year)])
    month = SelectField('Месяц', choices=[('Январь', '01'),
                                          ('Февраль', '02'),
                                          ('Март', '03'),
                                          ('Апрель', '04'),
                                          ('Май', '05'),
                                          ('Июнь', '06'),
                                          ('Июль', '07'),
                                          ('Август', '08'),
                                          ('Сентябрь', '09'),
                                          ('Октбярь', '10'),
                                          ('Ноябрь', '11'),
                                          ('Декабрь', '12')])
    submit = SubmitField("Применить")
