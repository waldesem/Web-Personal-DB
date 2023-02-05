import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField, SelectField, DateField, \
    FileField
from wtforms.validators import DataRequired, Length, InputRequired, Optional

current_year = datetime.date.today().year


class LoginForm(FlaskForm):  # форма для входа в систему
    """ Create form for login page"""

    username = StringField("Логин: ", validators=[InputRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=8, max=20)])
    remember = BooleanField("Запомнить ", default=False)
    submit = SubmitField("Войти")


class SearchForm(FlaskForm):  # форма для поиска на главной странице
    """ Create form for search"""

    full_name = StringField("Полное ФИО: ", validators=[InputRequired()])
    birthday = DateField("Дата рождения: ", validators=[Optional()])
    submit = SubmitField("Найти")


class FileForm(FlaskForm):  # форма для загрузки файла
    """ Create form for file upload"""
    file = FileField("Загрузить файл", validators=[FileAllowed(['xlsx', 'xlsm'])])


class ResumeForm(FlaskForm):  # форма для анкетных данных и служебных отметок
    """ Create form for create/edit resume page"""

    region = SelectField('Регион', choices=['Главный офис', 'Томск', 'РЦ Запад', 'РЦ Юг', 'РЦ Запад', 'РЦ Урал'])
    full_name = StringField("Фамилия Имя Отчество", validators=[InputRequired()])
    last_name = StringField("Предыдущие ФИО", validators=[Optional()])
    birthday = StringField("Дата рождения", validators=[InputRequired()])
    birth_place = StringField("Место рождения", validators=[Optional()])
    country = StringField("Гражданство", validators=[Optional()])
    series_passport = StringField("Серия паспорта", validators=[Optional()])
    number_passport = StringField("Номер паспорта", validators=[Optional()])
    agency = StringField("Орган выдавший", validators=[Optional()])
    date_given = StringField("Дата выдачи", validators=[Optional()])
    snils = StringField("СНИЛС", validators=[Optional()])
    inn = StringField("ИНН", validators=[Optional()])
    reg_address = TextAreaField("Адрес регистрации", validators=[Optional()])
    live_address = TextAreaField("Адрес проживания", validators=[Optional()])
    phone = StringField("Телефон", validators=[Optional()])
    email = StringField("Email: ", validators=[Optional()])
    education = TextAreaField("Образование", validators=[Optional()])
    workplace_1 = TextAreaField("Место работы #1", validators=[Optional()])
    workplace_2 = TextAreaField("Место работы #2", validators=[Optional()])
    workplace_3 = TextAreaField("Место работы #3", validators=[Optional()])
    addition = TextAreaField("Дополнительная информация", validators=[Optional()])
    submit = SubmitField("Принять")


class CheckForm(FlaskForm):  # форма для проверки
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
    check_mvd = TextAreaField("Проверка учетам МВД", validators=[Optional()])
    check_internet = TextAreaField("Проверка по открытым источникам", validators=[Optional()])
    check_cronos = TextAreaField("Проверка Кронос", validators=[Optional()])
    check_cross = TextAreaField("Проверка Крос", validators=[Optional()])
    check_addition = TextAreaField("Дополнительная информация", validators=[Optional()])
    pfo = BooleanField("Полиграф", default=False)
    resume = SelectField('Результат', choices=['Без замечаний', 'С комментарием', 'Негатив',
                                               'Снят с проверки', 'Сохранить'])
    comment = StringField("Комментарий", validators=[Optional()])
    submit = SubmitField("Принять")


class PoligrafForm(FlaskForm):  # форма для результатов ПФО
    """ Create form for page adding poligraf"""

    theme = StringField("Тема проверки", validators=[Optional()])
    results = TextAreaField("Информация", validators=[Optional()])
    officer = StringField("Сотрудник СБ", validators=[Optional()])
    date_pfo = DateField("Дата проведения", validators=[Optional()])
    submit = SubmitField("Принять")


class RegistrForm(FlaskForm):  # форма для согласования кандидата
    """ Create form for page registry"""

    supervisor = StringField("Руководитель", validators=[Optional()])
    marks = TextAreaField("Комментарий", validators=[Optional()])
    decision = SelectField('Решение', choices=['СОГЛАСОВАНО', 'СОГЛАСОВАНО С КОММЕНТАРИЕМ',
                                               'ОТКАЗАНО В СОГЛАСОВАНИИ', 'СНЯТ С ПРОВЕРКИ'])
    submit = SubmitField("Принять")


class InvestigationForm(FlaskForm):  # форма для результатов служебных проверок
    """ Create form for page adding investigation"""

    theme = StringField("Тема проверки", validators=[Optional()])
    info = TextAreaField("Информация", validators=[Optional()])
    date_inv = DateField("Дата окончания проверки", validators=[Optional()])
    submit = SubmitField("Принять")


class InquiryForm(FlaskForm):  # форма для запросов из других организаций
    """ Create form for page adding inquiry"""

    info = TextAreaField("Информация", validators=[Optional()])
    initiator = StringField("Инициатор", validators=[Optional()])
    date_inq = DateField("Дата запроса", validators=[Optional()])
    submit = SubmitField("Принять")


class InfoForm(FlaskForm):  # форма для формирования статинформации
    """ Create form for statistic information"""

    year = SelectField('Год', choices=[current_year - 2,
                                       current_year - 1,
                                       current_year])
    month = SelectField('Месяц', choices=[('Январь', 1),
                                          ('Февраль', 2),
                                          ('Март', 3),
                                          ('Апрель', 4),
                                          ('Май', 5),
                                          ('Июнь', 6),
                                          ('Июль', 7),
                                          ('Август', 8),
                                          ('Сентябрь', 9),
                                          ('Октбярь', 10),
                                          ('Ноябрь', 11),
                                          ('Декабрь', 12)])
    submit = SubmitField("Применить")
