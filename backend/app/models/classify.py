from enum import Enum


class Location(Enum):
    MAIN_OFFICE = 'Главный офис'
    SOUTH_REGION = 'Региональный центр Юг'
    NORTHWEST_REGION = 'Региональный центр Северо-Запад'
    URAL_REGION = 'Региональный центр Урал'
    SIBERIA_REGION = 'Региональный центр Сибирь'
    EAST_REGION = 'Региональный центр Восток'
    SALES_CENTER = 'Центр Агентских продаж'


class Role(Enum):
    """ Roles """

    admin = 'admin'
    superuser = 'superuser'
    user = 'user'
    api = 'api'


class Status(Enum):
    """ Status """

    new = 'Новый'
    update = 'Обновлен'
    manual = 'Проверка'
    save = "Сохранен"
    robot = 'Робот'
    reply = 'Обработан'
    poligraf = 'ПФО'
    result = 'Результат'
    finish = 'Окончено'
    cancel = 'Отменено'
    error = 'Ошибка'


class Conclusions(Enum):
    """ Conclusions """
    
    agreed = 'СОГЛАСОВАНО'
    with_comment = 'СОГЛАСОВАНО С КОММЕНТАРИЕМ'
    denied = 'ОТКАЗАНО В СОГЛАСОВАНИИ'
    saved = "СОХРАНЕН"
    canceled = 'ОТМЕНЕНО'
   

class Decisions(Enum):
    """ Decisions """

    agreed = 'СОГЛАСОВАНО'
    with_comment = 'СОГЛАСОВАНО С КОММЕНТАРИЕМ'
    denied = 'ОТКАЗАНО В СОГЛАСОВАНИИ'


class Category(Enum):
    """ Category """

    candidate = 'Кандидат'
    other = 'Проверяемый'