import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField, SelectField, DateField, \
    FileField
from wtforms.validators import DataRequired, InputRequired, Optional

from app.utils.extensions import STATUS

current_year = datetime.date.today().year


class LoginForm(FlaskForm):  # форма для входа в систему
    """ Create form for login page"""

    username = StringField("Логин: ", validators=[InputRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired()])
    remember = BooleanField("Запомнить ", default=False, validators=None)
    submit = SubmitField("Войти")


class SearchForm(FlaskForm):  # форма для поиска на главной странице
    """ Create form for search"""

    full_name = StringField("Поиск", validators=[InputRequired()])
    submit = SubmitField("Найти")


class FileForm(FlaskForm):  # форма для загрузки файла
    """ Create form for file upload"""
    file = FileField("Загрузить файл", validators=[FileAllowed(['xlsx', 'xlsm'])])
    upload = SubmitField("Загрузить")


class StaffForm(FlaskForm):
    """ Create form for staff"""

    staff = StringField("Должность", validators=[InputRequired()])
    department = StringField("Организация", validators=[Optional()])
    submit = SubmitField("Сохранить")


class PassportForm(FlaskForm):  # создаем общий класс паспорта
    """ Create form for passports"""

    series_passport = StringField("Серия паспорта", validators=[Optional()])
    number_passport = StringField("Номер паспорта", validators=[InputRequired()])
    agency = StringField("Орган выдавший", validators=[Optional()])
    date_given = DateField("Дата выдачи", validators=[Optional()])
    submit = SubmitField("Сохранить")


class AddressForm(FlaskForm):  # создаем общий класс адреса
    """ Create form for address"""

    type = SelectField("Выбрать", choices=['Адрес регистрации', 'Адрес проживания', 'Другое'])
    address = StringField("Полный", validators=[InputRequired()])
    submit = SubmitField("Сохранить")


class ContactForm(FlaskForm):  # создаем общий класс контактов
    """ Create form for contact"""

    type = SelectField("Выбрать", choices=['Телефон', 'E-mail', 'Другое'])
    contact = StringField("Контакт", validators=[InputRequired()])
    submit = SubmitField("Сохранить")


class WorkplaceForm(FlaskForm):  # создаем общий класс рабочих мест
    """ Create model for workplaces"""

    period = StringField("Период работы", validators=[Optional()])
    work_place = StringField("Место работы", validators=[InputRequired()])
    address = StringField("Адрес организации", validators=[Optional()])
    staff = StringField("Должность", validators=[Optional()])
    submit = SubmitField("Сохранить")


class RelationshipForm(FlaskForm):
    """ Create model for relationships"""

    relation = SelectField('Вид связи', choices=['Отец/Мать', 'Брат/Сестра', 'Супруг', 'Дети', 'Другое'])
    full_name = StringField("Полное ФИО", validators=[InputRequired()])
    birthday = StringField("Дата рождения", validators=[Optional()])
    address = StringField("Адрес", validators=[Optional()])
    workplace = StringField("Место работы", validators=[Optional()])
    contact = StringField("Контакт", validators=[Optional()])
    submit = SubmitField("Сохранить")


class ResumeForm(FlaskForm):  # форма для анкетных данных и служебных отметок
    """ Create form for create/edit resume page"""

    region = SelectField('Регион', choices=['Главный офис', 'Томск', 'РЦ Запад', 'РЦ Юг', 'РЦ Запад', 'РЦ Урал'])
    full_name = StringField("Фамилия Имя Отчество", validators=[InputRequired()])
    last_name = StringField("Изменение имени", validators=[Optional()])
    birthday = StringField("Дата рождения", validators=[InputRequired()])
    birth_place = StringField("Место рождения", validators=[Optional()])
    country = StringField("Гражданство", validators=[Optional()])
    snils = StringField("СНИЛС", validators=[Optional()])
    inn = StringField("ИНН", validators=[Optional()])
    education = TextAreaField("Образование", validators=[Optional()])
    addition = TextAreaField("Дополнительная информация", validators=[Optional()])
    status = SelectField("Статус", choices=[v for _, v in STATUS.items()])
    submit = SubmitField("Принять")


class CheckForm(FlaskForm):  # форма для проверки
    """ Create form for page adding check """

    former_employee = TextAreaField("Проверка по 1С", validators=[Optional()])
    check_work_place = TextAreaField("Проверка по месту работы", validators=[Optional()])
    check_passport = TextAreaField("Проверка паспорта", validators=[Optional()])
    check_inn = TextAreaField("Проверка паспорта", validators=[Optional()])
    check_debt = TextAreaField("Проверка задолженностей", validators=[Optional()])
    check_bankruptcy = TextAreaField("Проверка банкротства", validators=[Optional()])
    check_bki = TextAreaField("Проверка кредитной истории", validators=[Optional()])
    check_court = TextAreaField("Проверка по решениям судов", validators=[Optional()])
    check_affiliation = TextAreaField("Проверка аффилированности", validators=[Optional()])
    check_terrorist = TextAreaField("Проверка списка террористов", validators=[Optional()])
    check_mvd = TextAreaField("Проверка учетам МВД", validators=[Optional()])
    check_internet = TextAreaField("Проверка по открытым источникам", validators=[Optional()])
    check_cronos = TextAreaField("Проверка Кронос", validators=[Optional()])
    check_cross = TextAreaField("Проверка Крос", validators=[Optional()])
    check_addition = TextAreaField("Дополнительная информация", validators=[Optional()])
    pfo = BooleanField("Полиграф", default=False, validators=None)
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
