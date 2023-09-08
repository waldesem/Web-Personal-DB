from enum import Enum


class Regions(Enum):
    """ Regions """
    MAIN_OFFICE = 'Главный офис'
    SOUTH_REGION = 'Региональный центр Юг'
    WEST_REGION = 'Региональный центр Запад'
    URAL_REGION = 'Региональный центр Урал'
    EAST_REGION = 'Региональный центр Восток'


class Groups(Enum):
    """ Groups """
    staffsec = 'Центр кадровой безопасности'
    

class Roles(Enum):
    """ Roles """

    admin = 'admin'
    superuser = 'superuser'
    user = 'user'
    api = 'api'


class Category(Enum):
    """ Category """

    candidate = 'Кандидат'
    other = 'Проверяемый'


class Status(Enum):
    """ Status """

    new = 'Новый'
    repeat = "Повторный"
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
