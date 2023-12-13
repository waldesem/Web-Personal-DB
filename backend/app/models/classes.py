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
    admins = 'Администратор системы'
    staffsec = 'Центр кадровой безопасности'
    api = 'Application programming interface'
    

class Roles(Enum):
    """ Roles """

    superadmin = 'superadmin'
    admin = 'admin'
    user = 'user'
    api = 'api'


class Categories(Enum):
    """ Category """

    candidate = 'Кандидат'
    staff = 'Сотрудник'
    vip = 'ВИП'


class Statuses(Enum):
    """ Status """

    new = 'Новый'
    repeat = "Повторный"
    update = 'Обновлен'
    manual = 'Проверка'
    save = "Сохранен"
    robot = 'Робот'
    reply = 'Обработан'
    poligraf = 'ПФО'
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
