from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired, Optional


class LoginForm(FlaskForm):
    """ Create form for login page"""

    login = StringField("Логин: ", validators=[InputRequired()])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=8, max=20)])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")


class CreateForm(FlaskForm):
    """ Create form for add new candidate"""

    staff = StringField(u"Должность", validators=[InputRequired()])
    department = StringField(u"Кластер/Блок", validators=[InputRequired()])
    full_name = StringField(u"Фамилия Имя Отчество", validators=[InputRequired()])
    last_name = StringField(u"Предыдущие ФИО", validators=[Optional()])
    birthday = StringField(u"Дата рождения", validators=[InputRequired()])
    birth_place = StringField(u"Место рождения", validators=[Optional()])
    country = StringField(u"Гражданство", validators=[Optional()])
    series_passport = StringField(u"Серия паспорта", validators=[InputRequired()])
    number_passport = StringField(u"Номер паспорта", validators=[InputRequired()])
    date_given = StringField(u"Дата выдачи", validators=[InputRequired()])
    snils = StringField(u"СНИЛС", validators=[Optional()])
    inn = StringField(u"ИНН", validators=[Optional()])
    reg_address = TextAreaField(u"Адрес регистрации", validators=[Optional()])
    live_address = TextAreaField(u"Адрес проживания", validators=[Optional()])
    phone = StringField(u"Телефон", validators=[Optional()])
    email = StringField(u"Email: ", validators=[InputRequired()])
    education = TextAreaField(u"Образование", validators=[Optional()])
    check_work_place = TextAreaField(u"Проверка по месту работы", validators=[InputRequired()])
    check_passport = TextAreaField(u"Проверка паспорта", validators=[InputRequired()])
    check_debt = TextAreaField(u"Проверка задолженностей", validators=[InputRequired()])
    check_bankruptcy = TextAreaField(u"Проверка банкротства", validators=[InputRequired()])
    check_bki = TextAreaField(u"Проверка кредитной истории", validators=[InputRequired()])
    check_affiliation = TextAreaField(u"Проверка аффилированности", validators=[InputRequired()])
    check_internet = TextAreaField(u"Проверка по открытым источникам", validators=[InputRequired()])
    check_cronos = TextAreaField(u"Проверка Кронос", validators=[InputRequired()])
    check_cross = TextAreaField(u"Проверка Крос", validators=[InputRequired()])
    resume = SelectField(u'Решение', choices=['Без замечаний', 'С комментарием', 'Отказ'])
    officer = StringField(u"Сотрудник СБ", validators=[InputRequired()])
    submit = SubmitField(u"Принять ввод")


class ResumeForm(FlaskForm):
    """ Create form for edit resume page"""

    staff = StringField("Должность", validators=[InputRequired()])
    department = StringField("Кластер/Блок", validators=[InputRequired()])
    full_name = StringField("Фамилия Имя Отчество", validators=[InputRequired()])
    last_name = StringField("Предыдущие ФИО", validators=[Optional()])
    birthday = StringField("Дата рождения", validators=[InputRequired()])
    birth_place = StringField("Место рождения", validators=[Optional()])
    country = StringField("Гражданство", validators=[Optional()])
    series_passport = StringField("Серия паспорта", validators=[InputRequired()])
    number_passport = StringField("Номер паспорта", validators=[InputRequired()])
    date_given = StringField("Дата выдачи", validators=[InputRequired()])
    snils = StringField("СНИЛС", validators=[Optional()])
    inn = StringField("ИНН", validators=[Optional()])
    reg_address = TextAreaField("Адрес регистрации", validators=[Optional()])
    live_address = TextAreaField("Адрес проживания", validators=[Optional()])
    phone = StringField("Телефон", validators=[Optional()])
    email = StringField("Email: ", validators=[InputRequired()])
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
    resume = SelectField('Programming Language', choices=[('Без замечаний', 'Без замечаний'),
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
    submit = SubmitField("Войти")
