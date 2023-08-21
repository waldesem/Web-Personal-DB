from enum import Enum

regions = ['Главный офис', 
           'Региональный центр Юг', 
           'Региональный центр Северо-Запад', 
           'Региональный центр Урал', 
           'Региональный центр Сибирь', 
           'Региональный центр Восток', 
           'Центр Агентских продаж']

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