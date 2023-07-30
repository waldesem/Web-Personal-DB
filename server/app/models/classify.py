from enum import Enum
import os

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Persons'))
print(BASE_PATH)
class Role(Enum):

    admin = 'admin'
    superuser = 'superuser'
    user = 'user'
    api = 'api'


class Status(Enum):

    new = 'Новый'
    update = 'Обновлен'
    manual = 'Проверка'
    save = "Сохранен"
    robot = 'Робот'
    reply = 'Обработан'
    poligraf = 'ПФО'
    result = 'Результат'
    finish = 'Окончено'
    cancel = 'Отмена'
    error = 'Ошибка'


class Conclusions(Enum):

    agreed = 'СОГЛАСОВАНО'
    with_comment = 'СОГЛАСОВАНО С КОММЕНТАРИЕМ'
    denied = 'ОТКАЗАНО В СОГЛАСОВАНИИ'


class Decisions(Enum):
    agreed = 'СОГЛАСОВАНО'
    with_comment = 'СОГЛАСОВАНО С КОММЕНТАРИЕМ'
    denied = 'ОТКАЗАНО В СОГЛАСОВАНИИ'
    saved = "СОХРАНЕН"
    canceled = 'ОТМЕНЕНО'


class Category(Enum):

    candidate = 'Кандидат'
    other = 'Проверяемый'